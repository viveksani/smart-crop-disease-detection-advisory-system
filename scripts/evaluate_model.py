"""Evaluate an existing model on the prepared held-out PlantVillage test split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix


IMAGE_SIZE = (160, 160)
BATCH_SIZE = 64


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the trained model on the held-out test split.")
    parser.add_argument("--data-dir", type=Path, default=Path("data/plant_disease"))
    parser.add_argument("--model", type=Path, default=Path("models/crop_disease_model.keras"))
    parser.add_argument("--output-dir", type=Path, default=Path("models"))
    parser.add_argument("--head-epochs", type=int, default=1)
    parser.add_argument("--fine-tune-epochs", type=int, default=0)
    args = parser.parse_args()

    train_dir = args.data_dir / "train"
    class_names = sorted(path.name for path in train_dir.iterdir() if path.is_dir())
    if len(class_names) < 2:
        raise ValueError("The prepared training split must contain at least two class folders.")
    test_ds = tf.keras.utils.image_dataset_from_directory(
        args.data_dir / "test",
        labels="inferred",
        label_mode="int",
        class_names=class_names,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
    ).prefetch(tf.data.AUTOTUNE)

    model = tf.keras.models.load_model(args.model, compile=False)
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    test_loss, test_accuracy = model.evaluate(test_ds, verbose=0)
    y_true = np.concatenate([labels.numpy() for _, labels in test_ds])
    probabilities = model.predict(test_ds, verbose=0)
    y_pred = np.argmax(probabilities, axis=1)
    report = classification_report(
        y_true,
        y_pred,
        labels=list(range(len(class_names))),
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )
    summary = {
        "dataset": "PlantVillage color images",
        "dataset_source": "https://huggingface.co/datasets/mohanty/PlantVillage",
        "original_dataset_record": "https://data.mendeley.com/datasets/tywbtsjrjv/1",
        "architecture": "MobileNetV2 ImageNet transfer learning; frozen-backbone classifier head",
        "image_size": list(IMAGE_SIZE),
        "batch_size": BATCH_SIZE,
        "head_training_epochs": args.head_epochs,
        "fine_tuning_epochs": args.fine_tune_epochs,
        "fine_tuned_backbone_layers": 0,
        "number_of_classes": len(class_names),
        "class_names": class_names,
        "test_examples": int(len(y_true)),
        "test_loss": float(test_loss),
        "test_accuracy": float(test_accuracy),
        "classification_report": report,
        "macro_precision": float(report["macro avg"]["precision"]),
        "macro_recall": float(report["macro avg"]["recall"]),
        "macro_f1": float(report["macro avg"]["f1-score"]),
        "weighted_precision": float(report["weighted avg"]["precision"]),
        "weighted_recall": float(report["weighted avg"]["recall"]),
        "weighted_f1": float(report["weighted avg"]["f1-score"]),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=list(range(len(class_names)))).tolist(),
        "field_image_validation": "not performed",
        "limitation": "PlantVillage images were collected under controlled conditions; these scores do not establish field-photo performance.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "class_names.json").write_text(json.dumps(class_names, indent=2), encoding="utf-8")
    (args.output_dir / "model_report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({key: summary[key] for key in (
        "number_of_classes", "test_examples", "test_accuracy", "macro_precision", "macro_recall", "macro_f1",
        "weighted_precision", "weighted_recall", "weighted_f1",
    )}, indent=2))


if __name__ == "__main__":
    main()
