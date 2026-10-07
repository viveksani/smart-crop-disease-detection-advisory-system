"""Prepare the published PlantVillage train/test lists for scripts/train.py."""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "plantvillage"
OUTPUT = ROOT / "data" / "plant_disease"
SEED = 42


def read_split(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create train/validation/test folders from PlantVillage.")
    parser.add_argument("--validation-fraction", type=float, default=0.10)
    args = parser.parse_args()
    if not 0.05 <= args.validation_fraction <= 0.25:
        raise ValueError("validation-fraction must be between 0.05 and 0.25")

    archive_path = SOURCE / "data.zip"
    train_list_path = SOURCE / "splits" / "color_train.txt"
    test_list_path = SOURCE / "splits" / "color_test.txt"
    for path in (archive_path, train_list_path, test_list_path):
        if not path.is_file():
            raise FileNotFoundError(f"Missing {path}. Run scripts/download_plantvillage.py first.")

    train_by_class: dict[str, list[str]] = defaultdict(list)
    for member in read_split(train_list_path):
        parts = member.split("/")
        if len(parts) != 4 or parts[:2] != ["raw", "color"]:
            continue
        train_by_class[parts[2]].append(member)
    official_test = read_split(test_list_path)

    rng = random.Random(SEED)
    train_members: list[str] = []
    validation_members: list[str] = []
    for class_name in sorted(train_by_class):
        members = train_by_class[class_name]
        rng.shuffle(members)
        validation_count = max(1, round(len(members) * args.validation_fraction))
        validation_members.extend(members[:validation_count])
        train_members.extend(members[validation_count:])

    splits = {
        "train": train_members,
        "val": validation_members,
        "test": official_test,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    raw_dir = SOURCE / "extracted" / "raw" / "color"
    raw_dir.mkdir(parents=True, exist_ok=True)

    all_members = sorted({member for group in splits.values() for member in group})
    with zipfile.ZipFile(archive_path) as bundle:
        available = set(bundle.namelist())
        missing = [member for member in all_members if member not in available]
        if missing:
            raise FileNotFoundError(f"{len(missing)} split images are absent from the archive; first: {missing[0]}")
        for index, member in enumerate(all_members, start=1):
            destination = SOURCE / "extracted" / Path(*member.split("/"))
            if destination.exists():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(member) as source, destination.open("wb") as target:
                shutil.copyfileobj(source, target, length=1024 * 1024)
            if index % 5000 == 0:
                print(f"Extracted {index:,}/{len(all_members):,} images", flush=True)

    counts: dict[str, dict[str, int]] = {}
    for split_name, members in splits.items():
        split_counts: dict[str, int] = defaultdict(int)
        for member in members:
            _, _, class_name, filename = member.split("/")
            source = SOURCE / "extracted" / Path(*member.split("/"))
            destination = OUTPUT / split_name / class_name / filename
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                try:
                    os.link(source, destination)
                except OSError:
                    shutil.copy2(source, destination)
            split_counts[class_name] += 1
        counts[split_name] = dict(sorted(split_counts.items()))

    manifest = {
        "dataset": "PlantVillage color images",
        "source": "https://huggingface.co/datasets/mohanty/PlantVillage",
        "original_dataset": "https://data.mendeley.com/datasets/tywbtsjrjv/1",
        "license": "Mendeley record lists CC0 1.0; Hugging Face mirror lists CC BY-SA 3.0 and its loader calls that label assumed.",
        "seed": SEED,
        "validation_fraction_of_official_train": args.validation_fraction,
        "train": {"images": len(train_members), "classes": counts["train"]},
        "validation": {"images": len(validation_members), "classes": counts["val"]},
        "test": {"images": len(official_test), "classes": counts["test"]},
    }
    (OUTPUT / "dataset_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({name: len(members) for name, members in splits.items()}, indent=2))
    print(f"Prepared split folders in {OUTPUT}")


if __name__ == "__main__":
    main()
