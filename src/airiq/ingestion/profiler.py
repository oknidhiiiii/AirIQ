import json
from pathlib import Path
from typing import Dict, Any, Optional
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from airiq.ingestion.validator import validate_raw_data
from airiq.utils.config_loader import load_config
from airiq.utils.logging_utils import setup_logger

logger = setup_logger("airiq.ingestion.profiler")

def profile_raw_data(
    df: DataFrame,
    output_path: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generates a comprehensive machine-readable data profiling report in JSON format."""
    if config is None:
        config = load_config()

    if output_path is None:
        paths_cfg = config.get("paths", {})
        output_dir = Path(paths_cfg.get("output_dir", "data/outputs")).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / "raw_data_profile.json")

    logger.info("Building Raw Dataset Statistical Profile...")

    # Run non-destructive validation first
    val_report = validate_raw_data(df, config)
    total_rows = val_report["summary"]["total_rows"]

    # 1. Schema & Data Types Breakdown
    schema_info = [
        {"column_name": field.name, "data_type": field.dataType.simpleString()}
        for field in df.schema.fields
    ]

    # 2. Distinct Counts for Key Categorical Features
    categorical_cols = ["room_type", "neighbourhood_group_cleansed", "property_type"]
    categorical_profiles = {}

    for cat_col in categorical_cols:
        if cat_col in df.columns:
            top_counts = (
                df.groupBy(cat_col)
                .count()
                .orderBy(F.col("count").desc())
                .limit(10)
                .collect()
            )
            categorical_profiles[cat_col] = {
                "distinct_count": df.select(cat_col).distinct().count(),
                "top_categories": [
                    {str(row[cat_col]): int(row["count"])} for row in top_counts
                ]
            }

    # 3. Numeric Summary Statistics (min, max, mean, stddev) using try_cast
    numeric_cols = ["accommodates", "bedrooms", "beds", "minimum_nights", "number_of_reviews", "review_scores_rating"]
    numeric_stats = {}

    price_numeric = F.expr("try_cast(regexp_replace(price, '[\\$,]', '') as double)")
    df_with_price = df.withColumn("price_numeric", price_numeric)
    all_numeric = ["price_numeric"] + numeric_cols

    agg_exprs = []
    for col in all_numeric:
        agg_exprs.extend([
            F.min(col).alias(f"{col}_min"),
            F.max(col).alias(f"{col}_max"),
            F.avg(col).alias(f"{col}_mean"),
            F.stddev(col).alias(f"{col}_stddev")
        ])

    stats_row = df_with_price.select(agg_exprs).collect()[0].asDict()

    for col in all_numeric:
        display_name = "price" if col == "price_numeric" else col
        numeric_stats[display_name] = {
            "min": float(stats_row[f"{col}_min"]) if stats_row[f"{col}_min"] is not None else None,
            "max": float(stats_row[f"{col}_max"]) if stats_row[f"{col}_max"] is not None else None,
            "mean": round(float(stats_row[f"{col}_mean"]), 2) if stats_row[f"{col}_mean"] is not None else None,
            "stddev": round(float(stats_row[f"{col}_stddev"]), 2) if stats_row[f"{col}_stddev"] is not None else None,
        }

    # Compile Final Machine-Readable Profile
    profile_data = {
        "metadata": {
            "dataset_city": config.get("dataset", {}).get("city", "new-york"),
            "profile_type": "Raw Airbnb Dataset Quality Profile",
            "total_rows": total_rows,
            "total_columns": len(df.columns)
        },
        "schema": schema_info,
        "validation_metrics": val_report,
        "categorical_profiles": categorical_profiles,
        "numeric_statistics": numeric_stats
    }

    # Write profile JSON
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2)

    logger.info(f"Saved raw data profile to: {output_path}")
    return profile_data
