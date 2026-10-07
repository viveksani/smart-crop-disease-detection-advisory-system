# Model Training and Evaluation

## Model and training

The submitted model uses MobileNetV2 with ImageNet-pretrained features and a larger project-specific classification head. The input is an RGB leaf image resized to 160 × 160 pixels. The head concatenates global average and max pooled features, then uses a 256-unit dense layer, batch normalization, dropout, and a 38-class softmax output. Training started from the existing transfer-learning model, trained the expanded head for two epochs, then fine-tuned the final 19 non-batch-normalization backbone layers for three epochs at a lower learning rate. The best checkpoint was selected by validation loss.

- Dataset: PlantVillage color-image dataset
- Training images: 39,234
- Validation images: 4,362
- Held-out test images: 10,709
- Classes: 38
- Saved model: `models/crop_disease_model.keras` (about 29.7 MB)
- Labels: `models/class_names.json`
- Detailed per-class results and confusion matrix: `models/model_report.json`

## Held-out test results

| Metric | Earlier baseline | Expanded and fine-tuned model |
| --- | ---: | ---: |
| Accuracy | 90.76% | **94.14%** |
| Macro precision | 89.55% | **93.99%** |
| Macro recall | 87.53% | **91.28%** |
| Macro F1 | 87.78% | **92.04%** |
| Weighted precision | 91.60% | **94.62%** |
| Weighted recall | 90.76% | **94.14%** |
| Weighted F1 | 90.57% | **93.98%** |
| Test loss | 0.302 | **0.173** |

The two lowest-recall test classes in the updated run were Tomato Early blight (precision 92.7%, recall 41.4%, F1 57.2%) and Potato healthy (precision 81.0%, recall 53.1%, F1 64.2%). Their recall improved from 31.6% and 40.6% in the baseline, but both remain below 60%. The overall metrics therefore do not mean that every class meets a 60% precision/recall threshold.

On the validation split, the updated model reached 94.96% accuracy, 94.39% macro precision, 92.90% macro recall, and 93.22% macro F1 (loss 0.148). The baseline validation macro F1 was 88.11% (loss 0.294). These validation results informed checkpoint selection; the table above reports the separate held-out test split.

## Dataset and limitations

The images were downloaded from the [PlantVillage Hugging Face mirror](https://huggingface.co/datasets/mohanty/PlantVillage). The dataset loader links them to the [Mendeley Data release](https://data.mendeley.com/datasets/tywbtsjrjv/1) (DOI [10.17632/tywbtsjrjv.1](https://doi.org/10.17632/tywbtsjrjv.1)). The Mendeley record lists CC0 1.0. The Hugging Face mirror metadata lists CC BY-SA 3.0, while its loader says that license label is assumed; cite both records and check institutional requirements before redistributing images or derived materials.

PlantVillage images were collected in controlled settings and do not represent the full range of field lighting, backgrounds, varieties, or disease stages. Field-photo validation for this project has not been performed. The original PlantVillage study reports a large performance drop for its own model on images from different conditions; that result is a warning about dataset shift, not an estimate of this project's field accuracy ([Mohanty et al., 2016](https://arxiv.org/abs/1604.03169)). A displayed softmax confidence is the model's relative score for its predicted class, not a calibrated probability of diagnosis. Treat predictions and advisory text as preliminary screening only.
