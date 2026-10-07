import logging
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session

from .advisory import advisory_for
from .inference import DiseaseModel
from .storage import PredictionStorage


ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "local-only-change-this-secret")
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_MB", "10")) * 1024 * 1024
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.getenv("COOKIE_SECURE", "false").lower() == "true"

    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logger = logging.getLogger("crop_app")

    model_path = Path(os.getenv("MODEL_PATH", "models/crop_disease_model.keras"))
    names_path = Path(os.getenv("CLASS_NAMES_PATH", "models/class_names.json"))
    disease_model = DiseaseModel(model_path, names_path)
    storage = PredictionStorage(
        upload_dir=Path(os.getenv("UPLOAD_DIR", "data/uploads")),
        bucket=os.getenv("S3_BUCKET", ""),
        table_name=os.getenv("DYNAMODB_TABLE", ""),
        region=os.getenv("AWS_REGION", "ap-south-1"),
    )
    app.extensions["disease_model"] = disease_model
    app.extensions["prediction_storage"] = storage

    def get_session_id():
        if "session_id" not in session:
            session["session_id"] = storage.new_id()
        return session["session_id"]

    def safe_history(session_id):
        try:
            return storage.history(session_id)
        except Exception:
            logger.exception("Could not load prediction history")
            return []

    def page_error(message, status):
        return (
            render_template(
                "index.html",
                model_ready=disease_model.ready,
                model_message=disease_model.status_message,
                history=safe_history(get_session_id()),
                result=None,
                error=message,
            ),
            status,
        )

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            model_ready=disease_model.ready,
            model_message=disease_model.status_message,
            history=safe_history(get_session_id()),
            result=None,
            error=None,
        )

    @app.post("/predict")
    def predict():
        if not disease_model.ready:
            return page_error(disease_model.status_message, 503)

        uploaded = request.files.get("leaf_image")
        if not uploaded or not uploaded.filename:
            return page_error("Choose a leaf image before submitting.", 400)
        if uploaded.mimetype not in ALLOWED_CONTENT_TYPES:
            return page_error("Upload a JPG, PNG, or WebP image.", 415)

        try:
            image_bytes = uploaded.read()
            if not image_bytes:
                return page_error("The selected file is empty.", 400)
            prediction = disease_model.predict(image_bytes)
        except ValueError as exc:
            return page_error(str(exc), 400)
        except Exception:
            logger.exception("Inference failed")
            return page_error("The image could not be analyzed. Try a clear leaf photo.", 500)

        session_id = get_session_id()
        result = {
            "prediction_id": storage.new_id(),
            "session_id": session_id,
            "created_at": storage.now_iso(),
            "crop": prediction["crop"],
            "disease": prediction["disease"],
            "label": prediction["label"],
            "confidence": prediction["confidence"],
            "certain": prediction["confidence"] >= 0.60,
            "advisory": advisory_for(prediction["disease"], prediction["crop"]),
            "model_version": disease_model.version,
            "image_key": "",
        }

        try:
            storage.save(image_bytes, uploaded.mimetype, result)
        except Exception:
            logger.exception("Prediction completed, but saving its record failed")
            result["save_warning"] = "The result was generated, but storage failed. It may not appear in history."

        logger.info(
            "prediction_complete id=%s class=%s confidence=%.4f",
            result["prediction_id"],
            result["label"],
            result["confidence"],
        )
        return render_template(
            "index.html",
            model_ready=True,
            model_message="Model ready",
            history=safe_history(session_id),
            result=result,
            error=None,
        )

    @app.get("/healthz")
    def healthz():
        if not disease_model.ready:
            return jsonify({"status": "not_ready", "model": disease_model.status_message}), 503
        return jsonify({"status": "ok", "model": "ready"}), 200

    @app.errorhandler(413)
    def file_too_large(_error):
        return page_error("That image is larger than the 10 MB upload limit.", 413)

    return app
