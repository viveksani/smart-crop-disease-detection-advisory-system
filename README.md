# Smart Crop Disease Detection & Advisory System

An AI-assisted crop leaf screening application built as a college project submission. A user uploads a leaf photo, the application runs a trained image classifier, then presents a structured crop and disease assessment with typical signs to compare, immediate steps, treatment options, prevention advice, and trusted references.

## Project status

This repository contains the application, PlantVillage data pipeline, an expanded and fine-tuned MobileNetV2 model, AWS infrastructure, and deployment guide. The supplied progress-review deck describes the project as under development. The updated model scores 94.14% accuracy, 93.99% macro precision, and 91.28% macro recall on 10,709 held-out PlantVillage images. AWS deployment and field-photo validation have not been completed. Individual class results vary; see `models/model_report.json` and `docs/model-evaluation.md`.

The classifier is decision support. It does not localize lesions or verify each symptom. The disease-specific advisory is a curated rules-based guide, not an AI-generated diagnosis or a prescription. Confirm the cause and any pesticide choice with a local agricultural extension officer; use only products registered for that crop and disease in your location.

## What the application does

1. Accepts JPG, PNG, or WebP leaf images up to 10 MB.
2. Validates and resizes the image before inference.
3. Loads a MobileNetV2-based Keras classifier from models/crop_disease_model.keras.
4. Displays the predicted crop/disease, confidence, typical signs to compare, immediate steps, condition-specific treatment options, prevention guidance, escalation cues, and expert references.
5. Stores the image privately in S3 and prediction history in DynamoDB when AWS settings are present.
6. Uses a local file store when AWS settings are absent, for development.
7. Sends application logs to CloudWatch on the AWS deployment.

## AWS design

~~~text
Browser
  │ HTTP upload (demo deployment)
  ▼
Amazon EC2 ── Dockerized Flask app + model inference
  ├── Amazon S3 ── private uploaded images
  ├── Amazon DynamoDB ── anonymous session prediction history
  ├── AWS IAM ── EC2 instance role with scoped access
  └── Amazon CloudWatch ── container logs
~~~

The CloudFormation stack also creates the VPC, public subnet, route, internet gateway, security group, and log group needed to run the EC2 app. Those are EC2 networking resources, not additional application services.

## Repository layout

~~~text
app/                  Flask routes, inference, advisory and persistence
app/templates/        Upload and result page
app/static/           Responsive UI
infra/template.yaml   AWS CloudFormation stack
models/               Trained Keras model, labels, and evaluation report
scripts/               Dataset download/preparation, training, and evaluation
scripts/deploy.ps1    Package and deploy from Windows PowerShell
docs/                 Architecture and submission report
docs/advisory-guide.md Disease-specific advisory scope, safety limits, and references
~~~

## Local setup

Use Python 3.11. Create a virtual environment and install `requirements.txt`. The project model files are included:

~~~text
models/crop_disease_model.keras
models/class_names.json
~~~

class_names.json must be a JSON array in the same order as the model output, for example:

~~~json
["Tomato___Early_blight", "Tomato___healthy", "Tomato___Late_blight"]
~~~

Run the app:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:FLASK_SECRET_KEY = "replace-with-a-random-local-development-value"
python -m app
~~~

Open http://127.0.0.1:8000. The home page reports when the model is ready; uploads are disabled if the model files or TensorFlow are unavailable.

## Train the model

This project uses the unaugmented color images from the PlantVillage dataset mirror. The downloaded image archive is about 2.2 GB and is kept under the ignored `data/` directory; it is not included in the source bundle. Download the image archive and published split lists, then prepare the folders:

~~~powershell
python scripts/download_plantvillage.py
python scripts/prepare_plantvillage.py
~~~

The preparation step uses the published training and test lists, and reserves 10% of the published training images for validation. It creates separate folders with one subfolder per class:

~~~text
data/plant_disease/
  train/
    Tomato___Early_blight/
    Tomato___healthy/
  val/
    Tomato___Early_blight/
    Tomato___healthy/
  test/
    Tomato___Early_blight/
    Tomato___healthy/
~~~

Install the training add-on and run the held-out evaluation:

~~~powershell
python -m pip install -r requirements-train.txt
python scripts/train.py --data-dir data/plant_disease --epochs 8
~~~

The training pipeline starts with ImageNet-pretrained MobileNetV2, trains a disease-classification head, then fine-tunes the last backbone layers at a lower learning rate. It saves the model, class names, test metrics, and per-class evaluation report under `models/`. The submitted model uses global average and max pooling with a 256-unit head, two head-training epochs, and three fine-tuning epochs. It scores 94.14% accuracy on the held-out test split. To evaluate the included model without training it again:

~~~powershell
python scripts/evaluate_model.py --data-dir data/plant_disease --model models/crop_disease_model.keras --output-dir work/evaluation
~~~

The training data source is the [PlantVillage dataset mirror](https://huggingface.co/datasets/mohanty/PlantVillage), linked to the [Mendeley Data release](https://data.mendeley.com/datasets/tywbtsjrjv/1). The Mendeley record lists CC0 1.0; the Hugging Face mirror metadata lists CC BY-SA 3.0 and its loader notes that this license label is assumed. Cite J. Arun Pandian and Geetharamani Gopal (2019), DOI [10.17632/tywbtsjrjv.1](https://doi.org/10.17632/tywbtsjrjv.1), and the original PlantVillage work by Hughes and Salathé. Check institutional requirements before redistributing dataset images or derived materials. The dataset uses controlled-background leaf images; held-out accuracy on it does not establish field-photo performance.

## AWS deployment

The deployment targets EC2, S3, DynamoDB, IAM, and CloudWatch. It creates a small EC2 instance and a restricted HTTP endpoint for a project demo. The app has no user authentication; the security group therefore requires an explicit IPv4 CIDR allowlist and rejects `0.0.0.0/0`. Use an office/reviewer IP range and do not upload sensitive images. Add HTTPS and authentication before any broader release.

Prerequisites:

- An AWS account with permission to create EC2/VPC, IAM, S3, DynamoDB, CloudWatch Logs, and CloudFormation resources.
- AWS CLI v2 installed using the [official AWS installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and configured with a profile. Verify access with aws sts get-caller-identity.
- A trained model and models/class_names.json in the paths above.
- A region selected for deployment. The script defaults to ap-south-1; pass another region if needed. It finds the current Amazon Linux 2023 x86_64 image for that region.

Deploy from this repository:

~~~powershell
.\scripts\deploy.ps1 -Region ap-south-1 -PublicAccessCidr "YOUR_PUBLIC_IP/32"
~~~

Set the CIDR to the network that should be allowed to reach the app, such as a current public IP with `/32`. The script deploys the stack, uploads the application release to the private S3 bucket, and waits for `/healthz` to report that the model is ready.

The stack creates billable AWS resources. When the review is complete, remove the stack with:

~~~powershell
aws cloudformation delete-stack --stack-name smart-crop-disease --region ap-south-1
~~~

S3 buckets must be empty before CloudFormation can remove them. The cleanup helper in scripts/destroy.ps1 empties only this stack's image bucket and then deletes the stack. Review the stack name and bucket output before running it.

## Submission evidence

- docs/architecture.md — component roles and request/data flow.
- docs/submission-report.md — submission draft with measured model metrics and placeholders for AWS deployment screenshots.
- docs/model-evaluation.md — dataset, training method, test metrics, per-class caveats, and limitations.
- infra/template.yaml — infrastructure-as-code.
- scripts/train.py — reproducible transfer learning and fine-tuning pipeline.
- scripts/evaluate_model.py — held-out test evaluation for an existing model.
- scripts/download_plantvillage.py and scripts/prepare_plantvillage.py — dataset retrieval and split preparation.
- scripts/deploy.ps1 — repeatable deployment procedure.

Add your registration details and screenshots from your own AWS account before submitting. The included evaluation report records the measured model results; no AWS deployment is claimed until the stack is created and the end-to-end flow is verified.
