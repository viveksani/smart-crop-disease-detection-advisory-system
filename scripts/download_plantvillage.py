"""Download the unaugmented PlantVillage color images and official split lists."""

from __future__ import annotations

import os
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


BASE_URL = "https://huggingface.co/datasets/mohanty/PlantVillage/resolve/main/"
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "plantvillage"
FILES = ("data.zip", "splits/color_train.txt", "splits/color_test.txt")


def download(relative_path: str) -> Path:
    destination = DATA_DIR / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")

    for attempt in range(1, 6):
        offset = partial.stat().st_size if partial.exists() else 0
        request = urllib.request.Request(BASE_URL + relative_path)
        if offset:
            request.add_header("Range", f"bytes={offset}-")
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                status = getattr(response, "status", 200)
                if offset and status != 206:
                    offset = 0
                    partial.unlink(missing_ok=True)
                mode = "ab" if offset else "wb"
                expected = response.headers.get("Content-Length")
                total = offset + int(expected) if expected and expected.isdigit() else 0
                received = offset
                last_report = time.monotonic()
                with partial.open(mode) as output:
                    while block := response.read(1024 * 1024):
                        output.write(block)
                        received += len(block)
                        if time.monotonic() - last_report >= 10:
                            if total:
                                print(f"{relative_path}: {received / total:.1%}", flush=True)
                            else:
                                print(f"{relative_path}: {received / (1024**2):,.0f} MiB", flush=True)
                            last_report = time.monotonic()
            partial.replace(destination)
            print(f"Downloaded {relative_path} ({destination.stat().st_size:,} bytes)", flush=True)
            return destination
        except (OSError, urllib.error.URLError) as exc:
            print(f"Download attempt {attempt}/5 failed for {relative_path}: {exc}", flush=True)
            if attempt == 5:
                raise
            time.sleep(min(5 * attempt, 20))

    raise RuntimeError(f"Could not download {relative_path}")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    archive = download("data.zip")
    for split in FILES[1:]:
        download(split)
    with zipfile.ZipFile(archive) as bundle:
        bad_member = bundle.testzip()
        if bad_member:
            raise RuntimeError(f"Archive verification failed at {bad_member}")
        color_images = sum(
            member.startswith("raw/color/") and not member.endswith("/")
            for member in bundle.namelist()
        )
    print(f"Verified archive; {color_images:,} color image files are available.")
    print(f"Dataset files are in {DATA_DIR}")


if __name__ == "__main__":
    main()
