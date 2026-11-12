from pathlib import Path
from typing import Optional, Dict, Any
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from airiq.spark.session import get_spark_session
from airiq.ingestion.schema import get_raw_listings_schema, REQUIRED_COLUMNS
from airiq.utils.config_loader import load_config
from airiq.utils.logging_utils import setup_logger

logger = setup_logger("airiq.ingestion.reader")

class SchemaValidationError(Exception):
    """Raised when CSV input schema fails validation against expected schema."""
    pass

def read_raw_listings(
    file_path: Optional[str] = None,
    spark: Optional[SparkSession] = None,
    config: Optional[Dict[str, Any]] = None
) -> DataFrame:
    """Reads raw Airbnb CSV/GZ dataset into a PySpark DataFrame using column-name matching."""
    if config is None:
        config = load_config()

    if spark is None:
        spark = get_spark_session(config)

    if file_path is None:
        paths_cfg = config.get("paths", {})
        dataset_cfg = config.get("dataset", {})
        raw_dir = Path(paths_cfg.get("raw_dir", "data/raw")).resolve()
        filename = dataset_cfg.get("raw_filename", "listings.csv.gz")
        file_path = str(raw_dir / filename)

    path_obj = Path(file_path).resolve()
    if not path_obj.exists():
        raise FileNotFoundError(f"Raw dataset file not found at: {path_obj}. Run 'airiq download-data' first.")

    file_uri = path_obj.as_uri()
    logger.info(f"Reading raw listings dataset from URI: {file_uri}")
    expected_schema = get_raw_listings_schema()

    # Read header to align by column name
    raw_csv_df = (
        spark.read
        .option("header", "true")
        .option("multiLine", "true")
        .option("escape", '"')
        .option("quote", '"')
        .csv(file_uri)
    )

    actual_columns = set(raw_csv_df.columns)
    expected_set = set(REQUIRED_COLUMNS)

    missing_columns = expected_set - actual_columns
    if missing_columns:
        err_msg = f"Schema Validation FAILED! Missing required columns in raw dataset: {missing_columns}"
        logger.error(err_msg)
        raise SchemaValidationError(err_msg)

    # Cast and project by exact column name
    cast_exprs = []
    for field in expected_schema.fields:
        col_name = field.name
        col_type = field.dataType
        cast_exprs.append(F.expr(f"try_cast(`{col_name}` as {col_type.simpleString()})").alias(col_name))

    df_projected = raw_csv_df.select(*cast_exprs)

    logger.info(f"Raw dataset read successfully into PySpark DataFrame.")
    logger.info(f"DataFrame Schema Field Count: {len(df_projected.columns)}")
    
    return df_projected
