# System Architecture

## Scope

The system provides preliminary image-based crop disease screening and advisory. It is a college project demonstration, not an expert diagnosis service. This repository includes the application, a PlantVillage-trained MobileNetV2 baseline, and AWS deployment implementation. The AWS stack has not yet been deployed, and field-photo validation has not been performed. The app adds a curated, rules-based assessment for each supported disease class; it is not a second model and does not localize or verify symptoms in the uploaded photo.

## AWS components

| Component | Responsibility |
| --- | --- |
| Amazon EC2 | Runs the Dockerized Flask app and Keras inference model. |
| Amazon S3 | Stores uploaded images and the private application release bundle. Public access is blocked and uploads use server-side encryption. |
| Amazon DynamoDB | Stores prediction history, confidence, advisory, timestamp, model version, and anonymous browser-session key. |
| AWS IAM | Gives the EC2 instance only the S3, DynamoDB, and CloudWatch actions it needs. |
| Amazon CloudWatch | Receives container logs in a log group with 14-day retention. |
| VPC resources | Provide an isolated network and public route for the demo EC2 instance. |

## Request flow

1. The browser sends one JPG, PNG, or WebP image to the Flask app. The request limit is 10 MB.
2. The app checks the uploaded content and decodes it as an RGB image.
3. The model resizes to its saved input size (160 × 160 for the trained model) and returns class probabilities.
4. A disease label maps to a structured, disease-specific advisory: typical signs to compare, likely cause and spread, first actions, treatment options, prevention, escalation cues, and extension references. Results below 60% confidence are marked uncertain.
5. The app writes the image to S3 and a history item to DynamoDB using the EC2 instance role.
6. The result page displays the possible class, confidence, and full action plan. Pesticide options remain conditional on local diagnosis, registration, and product labels. Recent results appear for the same browser session.
7. Docker sends application logs to CloudWatch.

## Data model

DynamoDB uses a composite key:

- Partition key: session_id
- Sort key: prediction_key, containing the ISO timestamp plus prediction ID

Additional fields include prediction_id, created_at, crop, disease, label, confidence, advisory, model_version, and image_key. The image itself stays in S3; DynamoDB stores its object key.

The session identifier is anonymous and stored in a signed browser cookie. There is no account system or cross-device history.

## Model interface

The app loads the Keras classifier at `models/crop_disease_model.keras` and the JSON output-label array at `models/class_names.json`. The included training pipeline uses ImageNet-pretrained MobileNetV2, image augmentation, a frozen-backbone head-training phase, and optional low-rate fine-tuning. The supplied baseline completed one head-training epoch; fine-tuning remains available for later model refinement. Evaluation metrics and per-class results are recorded in `models/model_report.json`.

## Security and boundaries

- The S3 bucket blocks public access; EC2 accesses it through an IAM instance profile.
- S3 objects and the DynamoDB table use server-side encryption.
- The instance requires IMDSv2 tokens and has no inbound SSH rule.
- The demo endpoint is HTTP and has no authentication. CloudFormation requires an explicit security-group CIDR allowlist and the deploy script rejects `0.0.0.0/0`. Add HTTPS, authentication, and abuse controls before any broader release.
- The app stores uploaded images and anonymous prediction metadata. Use only images appropriate for a project demo.
- This stack intentionally keeps the application architecture to EC2, S3, DynamoDB, IAM, and CloudWatch.
