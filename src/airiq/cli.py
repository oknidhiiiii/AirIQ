import sys
import argparse
from typing import List, Optional

from airiq.utils.config_loader import load_config
from airiq.utils.logging_utils import setup_logger
from airiq.spark.smoke_test import run_smoke_test
from airiq.spark.session import stop_spark_session
from airiq.ingestion.downloader import download_dataset
from airiq.ingestion.reader import read_raw_listings
from airiq.ingestion.validator import validate_raw_data
from airiq.ingestion.profiler import profile_raw_data

logger = setup_logger("airiq.cli")

def main(args: Optional[List[str]] = None) -> int:
    """Main CLI entry point for AirIQ Phase 1 commands."""
    parser = argparse.ArgumentParser(
        prog="airiq",
        description="AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark (Phase 1 CLI)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Command: smoke-test
    subparsers.add_parser("smoke-test", help="Run mandatory PySpark environment pre-flight smoke test")
    
    # Command: download-data
    dl_parser = subparsers.add_parser("download-data", help="Download raw dataset from configured URL")
    dl_parser.add_argument("--force", action="store_true", help="Force re-download even if file exists")
    
    # Command: validate-raw
    subparsers.add_parser("validate-raw", help="Validate raw dataset quality non-destructively")
    
    # Command: profile-raw
    subparsers.add_parser("profile-raw", help="Generate machine-readable JSON raw dataset profile report")
    
    # Command: run-phase1
    p1_parser = subparsers.add_parser("run-phase1", help="Execute complete Phase 1 pipeline end-to-end")
    p1_parser.add_argument("--force", action="store_true", help="Force dataset re-download")

    parsed_args = parser.parse_args(args)
    if not parsed_args.command:
        parser.print_help()
        return 1

    try:
        config = load_config()

        if parsed_args.command == "smoke-test":
            success = run_smoke_test()
            return 0 if success else 1

        elif parsed_args.command == "download-data":
            download_dataset(force=parsed_args.force, config=config)
            return 0

        elif parsed_args.command == "validate-raw":
            logger.info("Executing raw dataset validation command...")
            df = read_raw_listings(config=config)
            report = validate_raw_data(df, config=config)
            stop_spark_session()
            logger.info("Validation completed cleanly.")
            return 0

        elif parsed_args.command == "profile-raw":
            logger.info("Executing raw dataset profiling command...")
            df = read_raw_listings(config=config)
            profile_raw_data(df, config=config)
            stop_spark_session()
            logger.info("Profiling completed cleanly.")
            return 0

        elif parsed_args.command == "run-phase1":
            logger.info("==========================================")
            logger.info("  EXECUTING AIRIQ PHASE 1 PIPELINE")
            logger.info("==========================================")
            
            # Step 1: Smoke Test
            logger.info("[Stage 1/4] Running PySpark Smoke Test...")
            if not run_smoke_test():
                logger.error("PySpark Smoke Test FAILED! Aborting Phase 1 pipeline.")
                return 1

            # Step 2: Download Dataset
            logger.info("[Stage 2/4] Downloading Dataset...")
            raw_path = download_dataset(force=parsed_args.force, config=config)

            # Step 3: Read & Validate Dataset
            logger.info("[Stage 3/4] Reading & Validating Raw Dataset...")
            df = read_raw_listings(file_path=str(raw_path), config=config)
            validate_raw_data(df, config=config)

            # Step 4: Generate Profiling Report
            logger.info("[Stage 4/4] Profiling Dataset & Generating Profile JSON...")
            profile_raw_data(df, config=config)

            stop_spark_session()
            logger.info("==========================================")
            logger.info("  AIRIQ PHASE 1 PIPELINE EXECUTED SUCCESSFULLY!")
            logger.info("==========================================")
            return 0

    except Exception as e:
        logger.error(f"Command '{parsed_args.command}' FAILED with error: {e}", exc_info=True)
        try:
            stop_spark_session()
        except Exception:
            pass
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
