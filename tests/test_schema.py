from airiq.ingestion.schema import get_raw_listings_schema, REQUIRED_COLUMNS

def test_schema_field_count():
    """Verify raw schema contains expected 36 fields."""
    schema = get_raw_listings_schema()
    assert len(schema.fields) == 36
    assert len(REQUIRED_COLUMNS) == 36

def test_schema_critical_columns_presence():
    """Verify presence of critical required columns in schema."""
    critical_cols = [
        "id", "name", "host_id", "neighbourhood_cleansed", 
        "latitude", "longitude", "room_type", "accommodates", "price"
    ]
    for col in critical_cols:
        assert col in REQUIRED_COLUMNS, f"Critical column '{col}' missing from schema."
