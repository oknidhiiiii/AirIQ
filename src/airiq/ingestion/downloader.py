import os
import json
import hashlib
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

from airiq.utils.config_loader import load_config
from airiq.utils.logging_utils import setup_logger

logger = setup_logger("airiq.ingestion.downloader")

def calculate_sha256(filepath: Path) -> str:
    """Calculates SHA256 checksum of file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_dataset(force: bool = False, config: Optional[Dict[str, Any]] = None) -> Path:
    """Downloads raw dataset from configured URL with provenance tracking."""
    if config is None:
        config = load_config()

    dataset_cfg = config.get("dataset", {})
    paths_cfg = config.get("paths", {})

    url = dataset_cfg.get("url")
    city = dataset_cfg.get("city", "new-york")
    filename = dataset_cfg.get("raw_filename", "listings.csv.gz")
    metadata_filename = dataset_cfg.get("metadata_filename", "listings_metadata.json")

    raw_dir = Path(paths_cfg.get("raw_dir", "data/raw")).resolve()
    raw_dir.mkdir(parents=True, exist_ok=True)

    output_path = raw_dir / filename
    metadata_path = raw_dir / metadata_filename

    if output_path.exists() and not force:
        file_size = output_path.stat().st_size
        if file_size > 0:
            logger.info(f"Dataset already exists at {output_path} ({file_size / (1024*1024):.2f} MB). Skipping download. Use force=True to re-download.")
            return output_path

    logger.info(f"Initiating dataset download from URL: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AirIQ-Data-Ingestion/1.0"
    }

    response = requests.get(url, headers=headers, stream=True, timeout=60)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to download dataset. HTTP Status Code: {response.status_code} for URL: {url}")

    total_bytes = 0
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1048576):  # 1 MB chunk
            if chunk:
                f.write(chunk)
                total_bytes += len(chunk)

    if total_bytes == 0 or output_path.stat().st_size == 0:
        if output_path.exists():
            output_path.unlink()
        raise RuntimeError(f"Downloaded file at {output_path} is empty (0 bytes).")

    logger.info(f"Download completed successfully. Output file: {output_path} ({total_bytes / (1024*1024):.2f} MB)")

    # Record Provenance Metadata
    checksum = calculate_sha256(output_path)
    snapshot_date = "2026-06-14"  # Default derived from URL snapshot segment
    if "20" in url:
        for part in url.split("/"):
            if len(part) == 10 and part.count("-") == 2 and part.replace("-", "").isdigit():
                snapshot_date = part
                break

    metadata = {
        "source": "Inside Airbnb Open Data",
        "source_url": url,
        "download_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_date": snapshot_date,
        "city": city,
        "filename": filename,
        "file_size_bytes": total_bytes,
        "file_size_mb": round(total_bytes / (1024 * 1024), 2),
        "sha256_checksum": checksum
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Saved dataset metadata provenance to {metadata_path}")
    return output_path
