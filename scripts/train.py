import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 64
SEED = 42


def load_split(directory: Path, class_names: list[str], shuffle: bool):
    if not directory.is_dir():
        raise FileNotFoundError("Dataset split not found: " + str(directory))
    dataset = tf.keras.utils.image_dataset_from_directory(
        directory,
        labels="inferred",
        label_mode="int",
        class_names=class_names,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
        seed=SEED,
    )
    return dataset.prefetch(tf.data.AUTOTUNE)


def main():
    parser = argparse.ArgumentParser(description="Train and evaluate a crop-leaf disease classifier.")
    parser.add_argument("--data-dir", type=Path, default=Path("data/plant_disease"))
    parser.add_argument("--output-dir", type=Path, default=Path("models"))
    parser.add_argument("--epochs", type=int, default=6, help="Maximum total epochs across both training phases.")
    parser.add_argument("--fine-tune-epochs", type=int, default=3)
    parser.add_argument("--initial-model", type=Path, help="Optional saved model whose pretrained MobileNetV2 weights seed the new head.")
    args = parser.parse_args()

    train_dir = args.data_dir / "train"
    class_names = sorted(path.name for path in train_dir.iterdir() if path.is_dir())
    if len(class_names) < 2:
        raise ValueError("The training split must contain at least two class folders.")
    train_ds = load_split(train_dir, class_names, shuffle=True)
    val_ds = load_split(args.data_dir / "val", class_names, shuffle=False)
    test_ds = load_split(args.data_dir / "test", class_names, shuffle=False)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.08),
            tf.keras.layers.RandomZoom(0.10),
        ],
        name="augmentation",
    )
    backbone = tf.keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights=None if args.initial_model else "imagenet",
    )
    if args.initial_model:
        initial_model = tf.keras.models.load_model(args.initial_model, compile=False)
        source_backbone = next(
            layer for layer in initial_model.layers
            if isinstance(layer, tf.keras.Model) and layer.name.startswith("mobilenetv2")
        )
        backbone.set_weights(source_backbone.get_weights())
        del initial_model
    backbone.trainable = False
    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3), name="leaf_rgb")
    x = augmentation(inputs)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = backbone(x, training=False)
    average_features = tf.keras.layers.GlobalAveragePooling2D(name="average_pool")(x)
    peak_features = tf.keras.layers.GlobalMaxPooling2D(name="peak_pool")(x)
    x = tf.keras.layers.Concatenate(name="pooled_features")([average_features, peak_features])
    x = tf.keras.layers.Dense(256, activation="relu", name="feature_head")(x)
    x = tf.keras.layers.BatchNormalization(name="head_normalization")(x)
    x = tf.keras.layers.Dropout(0.35, name="head_dropout")(x)
    outputs = tf.keras.layers.Dense(len(class_names), activation="softmax", name="class_probabilities")(x)
    model = tf.keras.Model(inputs, outputs, name="crop_disease_mobilenetv2")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    checkpoint_path = args.output_dir / "crop_disease_model.keras"
    head_epochs = max(1, args.epochs - min(args.fine_tune_epochs, args.epochs - 1))
    head_epochs = min(head_epochs, args.epochs)
    head_history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=head_epochs,
        shuffle=False,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=2, restore_best_weights=True),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=checkpoint_path,
                monitor="val_loss",
                save_best_only=True,
            ),
        ],
    )
    best_val_loss = min(head_history.history["val_loss"])

    fine_tune_epochs = max(0, args.epochs - head_epochs)
    fine_tuned_layer_count = 0
    fine_history = None
    if fine_tune_epochs:
        backbone.trainable = True
        for layer in backbone.layers[:-30]:
            layer.trainable = False
        for layer in backbone.layers:
            if isinstance(layer, tf.keras.layers.BatchNormalization):
                layer.trainable = False
        fine_tuned_layer_count = sum(layer.trainable for layer in backbone.layers)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        fine_history = model.fit(
            train_ds,
            validation_data=val_ds,
            initial_epoch=head_epochs,
            epochs=args.epochs,
            shuffle=False,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=2, restore_best_weights=True),
                tf.keras.callbacks.ModelCheckpoint(
                    filepath=checkpoint_path,
                    monitor="val_loss",
                    save_best_only=True,
                    initial_value_threshold=best_val_loss,
                ),
            ],
        )

    best_model = tf.keras.models.load_model(args.output_dir / "crop_disease_model.keras")

    def evaluate_split(dataset):
        loss, accuracy = best_model.evaluate(dataset, verbose=0)
        y_true = np.concatenate([labels.numpy() for _, labels in dataset])
        probabilities = best_model.predict(dataset, verbose=0)
        y_pred = np.argmax(probabilities, axis=1)
        report = classification_report(
            y_true,
            y_pred,
            labels=list(range(len(class_names))),
            target_names=class_names,
            output_dict=True,
            zero_division=0,
        )
        return loss, accuracy, report, y_true, y_pred

    val_loss, val_accuracy, val_report, val_true, _ = evaluate_split(val_ds)
    test_loss, test_accuracy, report, y_true, y_pred = evaluate_split(test_ds)
    summary = {
        "architecture": "MobileNetV2 ImageNet transfer learning with global average/max pooling, a 256-unit head, and final-layer fine-tuning",
        "initialized_from": str(args.initial_model) if args.initial_model else "ImageNet weights from Keras",
        "image_size": list(IMAGE_SIZE),
        "batch_size": BATCH_SIZE,
        "head_training_epochs": len(head_history.history["loss"]),
        "fine_tuning_epochs": len(fine_history.history["loss"]) if fine_history else 0,
        "fine_tuned_backbone_layers": fine_tuned_layer_count,
        "class_names": class_names,
        "validation_examples": int(len(val_true)),
        "validation_loss": float(val_loss),
        "validation_accuracy": float(val_accuracy),
        "validation_macro_precision": float(val_report["macro avg"]["precision"]),
        "validation_macro_recall": float(val_report["macro avg"]["recall"]),
        "validation_macro_f1": float(val_report["macro avg"]["f1-score"]),
        "validation_classification_report": val_report,
        "test_examples": int(len(y_true)),
        "test_loss": float(test_loss),
        "test_accuracy": float(test_accuracy),
        "macro_precision": float(report["macro avg"]["precision"]),
        "macro_recall": float(report["macro avg"]["recall"]),
        "macro_f1": float(report["macro avg"]["f1-score"]),
        "weighted_precision": float(report["weighted avg"]["precision"]),
        "weighted_recall": float(report["weighted avg"]["recall"]),
        "weighted_f1": float(report["weighted avg"]["f1-score"]),
        "classification_report": report,
        "confusion_matrix": confusion_matrix(
            y_true, y_pred, labels=list(range(len(class_names)))
        ).tolist(),
        "note": "Metrics are from the held-out test folder; validate on field images before real use.",
    }
    (args.output_dir / "class_names.json").write_text(json.dumps(class_names, indent=2), encoding="utf-8")
    (args.output_dir / "model_report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("test_examples", "test_loss", "test_accuracy")}, indent=2))
    print("Saved model and class list under " + str(args.output_dir.resolve()))


if __name__ == "__main__":
    main()
