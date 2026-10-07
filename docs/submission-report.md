# Smart Crop Disease Detection & Advisory System

**Project report draft — college project submission**

**Student:** Vivek Sani  
**Registration number:** Add your registration number  
**Project period:** Add project dates  
**Review date:** Update before submission

## Abstract

Crop diseases can reduce yield and quality, while early identification and access to expert guidance may be limited. This project develops an AI-assisted web application that accepts a crop-leaf image, estimates a disease class with a deep-learning image classifier, and presents a structured, disease-specific action plan. The plan summarizes typical signs to compare, likely cause and spread, immediate care, conditional treatment options, prevention, and when to seek expert help. The application is designed for deployment on Amazon EC2. Amazon S3 stores submitted images, Amazon DynamoDB stores prediction history, AWS IAM controls application permissions, and Amazon CloudWatch collects application logs. The system is intended as preliminary decision support and does not replace local agricultural expertise.

## Problem statement

Farmers may have difficulty identifying crop diseases early, particularly when symptoms are similar and expert support is not immediately available. Manual inspection and consultation can take time. The project explores whether an image-classification model and cloud-hosted application can make a first screening step more accessible.

## Objectives

- Build a computer-vision classifier for crop leaf disease classes.
- Provide a web interface for image upload and result review.
- Return a possible class, confidence estimate, and cautious next-step advisory.
- Store submitted images and prediction history with AWS services.
- Demonstrate a complete upload, inference, storage, and response workflow.

## Proposed design

The browser uploads an image to a Flask application on EC2. The server validates the image, resizes it to the trained model's 160 × 160 RGB input, and calls the Keras model. The predicted class maps to a curated, rules-based disease profile with typical signs, first steps, treatment categories, prevention advice, and extension references. This content is not a second image analysis and does not claim that the listed signs were detected in the uploaded photo. The image is stored in a private S3 bucket, while DynamoDB stores the result and image key. An EC2 instance role grants scoped S3 and DynamoDB access. Docker logs are sent to CloudWatch.

## Implementation included

- Flask application with image validation, model inference, result presentation, and recent session history.
- MobileNetV2 training and held-out test-evaluation script.
- Disease-specific advisory profiles covering typical signs, cause/spread, immediate steps, conditional treatment options, prevention, escalation cues, and references; the UI treats predictions as preliminary and flags low-confidence results.
- CloudFormation template for EC2, private S3 storage, DynamoDB, IAM, CloudWatch Logs, and required VPC networking.
- PowerShell deployment and cleanup scripts.

## Current implementation status

| Area | Status |
| --- | --- |
| Problem statement, objectives, and AWS service selection | Described in the supplied progress-review deck |
| Dataset and model | PlantVillage prepared; expanded MobileNetV2 transfer-learning model trained and evaluated on a held-out test split |
| Web interface and inference integration | Flask app, image upload, preview, detailed crop/disease assessment, treatment precautions, references, session history, and trained-model loading are implemented |
| AWS deployment | Infrastructure and deployment scripts are prepared; the stack has not been deployed from this workspace |
| End-to-end AWS evidence | Still needed from the student's AWS account after deployment |

## Evaluation results

- Dataset: PlantVillage color-image subset, obtained from the [Hugging Face mirror](https://huggingface.co/datasets/mohanty/PlantVillage) and linked to the [Mendeley Data release](https://data.mendeley.com/datasets/tywbtsjrjv/1). The Mendeley record lists CC0 1.0; the Hugging Face mirror metadata lists CC BY-SA 3.0 and its loader describes that label as assumed. Include the source attribution and verify the terms required by the institution before redistribution.
- Split counts: 39,234 train, 4,362 validation, and 10,709 held-out test images.
- Classes: 38 across crop species and leaf conditions.
- Model: ImageNet-pretrained MobileNetV2 with global average/max pooling and a 256-unit classification head; two head-training epochs and three fine-tuning epochs on the final 19 eligible backbone layers; 160 × 160 input.
- Test accuracy: **94.14%** (test loss 0.173).
- Macro precision / recall / F1: **93.99% / 91.28% / 92.04%**.
- Weighted precision / recall / F1: **94.62% / 94.14% / 93.98%**.
- The lowest test recalls were Tomato Early blight (41.4%) and Potato healthy (53.1%); see `models/model_report.json` for all classes.
- Per-class precision/recall/F1 and confusion matrix: see `models/model_report.json`.
- Field-image validation: **not performed**.

The expanded model improved held-out dataset metrics over the earlier transfer-learning baseline, but its class results remain uneven and two recalls are below 60%. The score is useful for a college demonstration on this dataset, but should not be presented as reliable real-world diagnosis. The original PlantVillage study also reports a substantial performance drop on images from conditions different from its training images ([Mohanty et al., 2016](https://arxiv.org/abs/1604.03169)).

Do not use validation accuracy as test accuracy. Dataset performance may not represent photos taken in fields or under different lighting, backgrounds, crop varieties, or disease stages.

## Limitations and future work

The model can only predict classes represented in its training data. Backgrounds, lighting, image quality, and local disease variation may affect results. The included advice is general and should be checked against local agricultural guidance. The demo does not include login, HTTPS, multilingual support, weather information, or expert review.

Next steps are to deploy the prepared stack in the student's AWS account, verify the upload → inference → S3/DynamoDB path, capture deployment evidence, and add the student's AWS screenshots and project-specific details.

## Conclusion

This project combines an image-classification workflow with a simple cloud-hosted application and AWS storage/monitoring services. The implementation provides a reproducible route from a user image to model inference and advisory presentation. Its conclusions should remain limited to the model’s measured evaluation and the project’s demonstrated deployment state.

## References

- [MobileNetV2: Inverted Residuals and Linear Bottlenecks](https://arxiv.org/abs/1801.04381)
- [TensorFlow: Transfer learning and fine-tuning](https://www.tensorflow.org/guide/keras/transfer_learning)
- [AWS CloudFormation: DynamoDB table resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-dynamodb-table.html)
- [AWS CLI v2 installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Amazon Linux 2023 AMI names and versions](https://docs.aws.amazon.com/linux/al2023/ug/naming-and-versioning.html)

Add the exact dataset source and license used for training before submitting the final report.
