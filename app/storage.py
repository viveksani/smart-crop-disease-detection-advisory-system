import json
import logging
import mimetypes
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import boto3
from boto3.dynamodb.conditions import Key

LOGGER = logging.getLogger(__name__)


class PredictionStorage:
    def __init__(self, upload_dir: Path, bucket: str, table_name: str, region: str):
        self.upload_dir = upload_dir
        self.bucket = bucket.strip()
        self.table_name = table_name.strip()
        self.region = region
        self.aws_enabled = bool(self.bucket and self.table_name)
        if bool(self.bucket) != bool(self.table_name):
            raise ValueError("Set both S3_BUCKET and DYNAMODB_TABLE, or leave both empty.")
        self.s3 = None
        self.table = None
        if self.aws_enabled:
            self.s3 = boto3.client("s3", region_name=region)
            self.table = boto3.resource("dynamodb", region_name=region).Table(self.table_name)
        else:
            self.upload_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def new_id():
        return str(uuid.uuid4())

    @staticmethod
    def now_iso():
        return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")

    def save(self, image_bytes: bytes, content_type: str, record: dict):
        extension = mimetypes.guess_extension(content_type) or ".img"
        image_key = "uploads/" + record["session_id"] + "/" + record["prediction_id"] + extension
        record["image_key"] = image_key
        if self.aws_enabled:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=image_key,
                Body=image_bytes,
                ContentType=content_type,
                ServerSideEncryption="AES256",
            )
            try:
                item = dict(record)
                item["confidence"] = Decimal(str(record["confidence"]))
                item["prediction_key"] = record["created_at"] + "#" + record["prediction_id"]
                self.table.put_item(Item=item)
            except Exception:
                try:
                    self.s3.delete_object(Bucket=self.bucket, Key=image_key)
                except Exception:
                    LOGGER.exception("Could not remove an unindexed uploaded image")
                raise
            return
        image_path = self.upload_dir / (record["prediction_id"] + extension)
        image_path.write_bytes(image_bytes)
        line = json.dumps(record, ensure_ascii=False)
        with (self.upload_dir / "predictions.jsonl").open("a", encoding="utf-8") as history_file:
            history_file.write(line + "\n")

    def history(self, session_id: str, limit: int = 8):
        if self.aws_enabled:
            response = self.table.query(
                KeyConditionExpression=Key("session_id").eq(session_id),
                ScanIndexForward=False,
                Limit=limit,
            )
            return [_history_item(item) for item in response.get("Items", [])]
        history_path = self.upload_dir / "predictions.jsonl"
        if not history_path.exists():
            return []
        entries = []
        with history_path.open("r", encoding="utf-8") as history_file:
            for line in history_file:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    LOGGER.warning("Ignoring an unreadable local history line")
                    continue
                if record.get("session_id") == session_id:
                    entries.append(_history_item(record))
        return list(reversed(entries[-limit:]))


def _history_item(record):
    return {
        "created_at": record.get("created_at", ""),
        "crop": record.get("crop", "Crop"),
        "disease": record.get("disease", "Unknown"),
        "confidence": float(record.get("confidence", 0)),
    }
