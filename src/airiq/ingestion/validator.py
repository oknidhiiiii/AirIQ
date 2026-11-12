from typing import Dict, Any, Optional
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from airiq.utils.config_loader import load_config
from airiq.utils.logging_utils import setup_logger

logger = setup_logger("airiq.ingestion.validator")

def validate_raw_data(df: DataFrame, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Performs non-destructive quality validation on raw PySpark DataFrame.
    
    Identifies and reports quality anomalies without removing records in Phase 1.
    """
    if config is None:
        config = load_config()

    val_cfg = config.get("validation", {})
    bounds = val_cfg.get("bounds", {})

    lat_min = bounds.get("latitude_min", 40.4)
    lat_max = bounds.get("latitude_max", 40.9)
    lon_min = bounds.get("longitude_min", -74.3)
    lon_max = bounds.get("longitude_max", -73.6)

    logger.info("Executing Raw Data Validation Suite...")

    # 1. Total Row & Column Counts
    total_rows = df.count()
    total_cols = len(df.columns)
    logger.info(f"Total Rows: {total_rows:,}, Total Columns: {total_cols}")

    if total_rows == 0:
        raise ValueError("Raw dataset is EMPTY (0 rows). Validation cannot proceed.")

    # 2. Duplicate Listing ID Analysis
    distinct_ids = df.select("id").distinct().count()
    duplicate_ids = total_rows - distinct_ids
    null_id_count = df.filter(F.col("id").isNull()).count()

    # 3. Safe Price Convertibility Analysis using try_cast
    price_clean = F.regexp_replace(F.col("price"), r"[\$,]", "")
    price_numeric = F.expr("try_cast(regexp_replace(price, '[\\$,]', '') as double)")
    
    invalid_price_count = df.filter(
        F.col("price").isNull() | price_numeric.isNull() | (price_numeric <= 0)
    ).count()

    # 4. Coordinates Validity Analysis
    invalid_coords_count = df.filter(
        F.col("latitude").isNull() | F.col("longitude").isNull() |
        (F.col("latitude") < lat_min) | (F.col("latitude") > lat_max) |
        (F.col("longitude") < lon_min) | (F.col("longitude") > lon_max)
    ).count()

    # 5. Accommodates Validity Analysis
    invalid_accommodates_count = df.filter(
        F.col("accommodates").isNull() | (F.col("accommodates") < 1)
    ).count()

    # 6. Room Type Domain Analysis
    valid_room_types = ["Entire home/apt", "Private room", "Shared room", "Hotel room"]
    invalid_room_type_count = df.filter(
        F.col("room_type").isNull() | (~F.col("room_type").isin(valid_room_types))
    ).count()

    # 7. Null Count Aggregations across all columns
    null_exprs = [F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in df.columns]
    null_counts_row = df.select(null_exprs).collect()[0].asDict()

    null_summary = {
        col: {
            "null_count": count,
            "null_percentage": round((count / total_rows) * 100, 2)
        }
        for col, count in null_counts_row.items()
    }

    report = {
        "summary": {
            "total_rows": total_rows,
            "total_columns": total_cols,
            "distinct_listing_ids": distinct_ids,
            "duplicate_listing_ids": duplicate_ids,
            "null_id_count": null_id_count,
        },
        "quality_checks": {
            "invalid_price_records": invalid_price_count,
            "invalid_price_percentage": round((invalid_price_count / total_rows) * 100, 2),
            "invalid_coordinates_records": invalid_coords_count,
            "invalid_coordinates_percentage": round((invalid_coords_count / total_rows) * 100, 2),
            "invalid_accommodates_records": invalid_accommodates_count,
            "invalid_room_type_records": invalid_room_type_count,
        },
        "column_null_summary": null_summary
    }

    logger.info("Raw Data Validation Results:")
    logger.info(f"  - Duplicate IDs: {duplicate_ids} ({duplicate_ids/total_rows*100:.2f}%)")
    logger.info(f"  - Invalid/Non-numeric Prices: {invalid_price_count} ({invalid_price_count/total_rows*100:.2f}%)")
    logger.info(f"  - Invalid Coordinates (outside NYC bounds): {invalid_coords_count} ({invalid_coords_count/total_rows*100:.2f}%)")
    logger.info(f"  - Invalid Accommodates (< 1): {invalid_accommodates_count}")
    logger.info(f"  - Invalid Room Types: {invalid_room_type_count}")

    return report
