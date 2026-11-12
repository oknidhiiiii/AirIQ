import pytest
from pathlib import Path
from airiq.spark.session import get_spark_session, stop_spark_session
from airiq.ingestion.schema import get_raw_listings_schema
from airiq.ingestion.reader import SchemaValidationError, read_raw_listings

@pytest.fixture(scope="module")
def spark():
    session = get_spark_session()
    yield session
    stop_spark_session()

def test_reader_synthetic_csv(spark, tmp_path):
    """Test reading a synthetic CSV file conforming to the explicit schema."""
    csv_file = tmp_path / "synthetic_listings.csv"
    headers = [field.name for field in get_raw_listings_schema().fields]
    row1 = ["101", "Cozy Apt", "201", "Alice", "2020-01-01", "NY", "t", "2", "East Village", "Manhattan", "Manhattan", "40.72", "-73.98", "Apartment", "Entire home/apt", "2", "1.0", "1", "1", "$150.00", "2", "30", "10", "20", "30", "100", "50", "10", "2.5", "4.8", "4.9", "4.8", "4.9", "4.7", "4.8", "1"]
    
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write(",".join(headers) + "\n")
        f.write(",".join(row1) + "\n")
        
    df = read_raw_listings(file_path=str(csv_file), spark=spark)
    assert df.count() == 1
    assert df.columns == headers

def test_reader_missing_columns_raises_validation_error(spark, tmp_path):
    """Test reading a CSV with missing columns raises SchemaValidationError."""
    csv_file = tmp_path / "broken_listings.csv"
    headers = ["id", "name", "price"]
    row1 = ["101", "Cozy Apt", "$150.00"]
    
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write(",".join(headers) + "\n")
        f.write(",".join(row1) + "\n")
        
    with pytest.raises(SchemaValidationError):
        read_raw_listings(file_path=str(csv_file), spark=spark)
