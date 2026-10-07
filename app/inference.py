import json
import logging
from pathlib import Path
from io import BytesIO

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

try:
    import tensorflow as tf
except ImportError:
    tf = None

LOGGER = logging.getLogger(__name__)
IMAGE_SIZE = (160, 160)
MAX_IMAGE_PIXELS = 25_000_000


class DiseaseModel:
    def __init__(self, model_path: Path, names_path: Path):
        self.ready = False
        self.model = None
        self.class_names = []
        self.image_size = IMAGE_SIZE
        self.version = "unavailable"
        self.status_message = "Model files are missing. Add the trained model and class list to models/."

        if not model_path.is_file() or not names_path.is_file():
            return
        if tf is None:
            self.status_message = "TensorFlow is not installed. Install the project requirements."
            return
        try:
            names = json.loads(names_path.read_text(encoding="utf-8"))
            if not isinstance(names, list) or not names or not all(isinstance(x, str) for x in names):
                raise ValueError("Class names must be a non-empty JSON array of strings.")
            model = tf.keras.models.load_model(model_path, compile=False)
            input_shape = model.input_shape
            if isinstance(input_shape, list) or len(input_shape) != 4:
                raise ValueError("The model must accept one RGB image input.")
            self.image_size = tuple(
                int(input_shape[index]) if input_shape[index] is not None else IMAGE_SIZE[index - 1]
                for index in (1, 2)
            )
            output_size = int(model.output_shape[-1])
            if output_size != len(names):
                raise ValueError("The model output count does not match the number of class names.")
            self.model = model
            self.class_names = names
            self.version = model_path.stem
            self.status_message = "Model ready"
            self.ready = True
        except Exception as exc:
            LOGGER.exception("Could not load the trained model")
            self.status_message = "Model could not be loaded: " + str(exc)

    def predict(self, image_bytes: bytes):
        if not self.ready:
            raise RuntimeError(self.status_message)
        try:
            with Image.open(BytesIO(image_bytes)) as source:
                if source.width * source.height > MAX_IMAGE_PIXELS:
                    raise ValueError("The image resolution is too large. Resize it and try again.")
                source.verify()
            with Image.open(BytesIO(image_bytes)) as source:
                oriented = ImageOps.exif_transpose(source)
                pixels = np.asarray(
                    oriented.convert("RGB").resize(self.image_size, resample=Image.Resampling.BILINEAR),
                    dtype=np.float32,
                )
        except ValueError:
            raise
        except (UnidentifiedImageError, OSError) as exc:
            raise ValueError("The file is not a valid image. Try a clear JPG, PNG, or WebP leaf photo.") from exc

        scores = np.asarray(self.model.predict(np.expand_dims(pixels, axis=0), verbose=0))[0]
        index = int(np.argmax(scores))
        label = self.class_names[index]
        crop, disease = split_label(label)
        return {
            "crop": crop,
            "disease": disease,
            "label": label,
            "confidence": float(scores[index]),
        }


def split_label(label: str):
    cleaned = label.replace("___", " - ").replace("__", " - ").replace("_", " ").strip()
    if " - " in cleaned:
        crop, disease = cleaned.split(" - ", 1)
        return crop.strip().title(), disease.strip().title()
    if " " in cleaned:
        crop, disease = cleaned.split(" ", 1)
        return crop.strip().title(), disease.strip().title()
    return "Crop", cleaned.title()
