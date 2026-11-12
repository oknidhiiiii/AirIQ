import pytest
from airiq.spark.session import get_spark_session, stop_spark_session
from airiq.ingestion.schema import get_raw_listings_schema
from airiq.ingestion.validator import validate_raw_data

@pytest.fixture(scope="module")
def spark():
    session = get_spark_session()
    yield session
    stop_spark_session()

def test_validation_quality_checks(spark):
    """Test data validation metrics calculation on synthetic DataFrame."""
    schema = get_raw_listings_schema()
    
    # Row 1: Valid
    # Row 2: Duplicate ID, invalid price, invalid coordinates
    sample_data = [
        (101, "Apt 1", 201, "Alice", "2020-01-01", "NY", "t", 2, "East Village", "Manhattan", "Manhattan", 40.72, -73.98, "Apartment", "Entire home/apt", 2, 1.0, 1, 1, "$150.00", 2, 30, 10, 20, 30, 100, 50, 10, 2.5, 4.8, 4.9, 4.8, 4.9, 4.7, 4.8, 1),
        (101, "Apt 1 Dup", 201, "Alice", "2020-01-01", "NY", "t", 2, "East Village", "Manhattan", "Manhattan", 10.0, -10.0, "Apartment", "Entire home/apt", 0, 1.0, 1, 1, "INVALID", 2, 30, 10, 20, 30, 100, 50, 10, 2.5, 4.8, 4.9, 4.8, 4.9, 4.7, 4.8, 1),
    ]
    
    df = spark.createDataFrame(sample_data, schema)
    report = validate_raw_data(df)
    
    assert report["summary"]["total_rows"] == 2
    assert report["summary"]["distinct_listing_ids"] == 1
    assert report["summary"]["duplicate_listing_ids"] == 1
    assert report["quality_checks"]["invalid_price_records"] == 1
    assert report["quality_checks"]["invalid_coordinates_records"] == 1
    assert report["quality_checks"]["invalid_accommodates_records"] == 1
