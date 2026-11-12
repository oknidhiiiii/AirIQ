from pyspark.sql.types import (
    StructType,
    StructField,
    LongType,
    StringType,
    DoubleType,
    IntegerType,
    DateType,
)

def get_raw_listings_schema() -> StructType:
    """Returns the explicit PySpark StructType schema for raw Inside Airbnb CSV datasets."""
    return StructType([
        StructField("id", LongType(), False),
        StructField("name", StringType(), True),
        StructField("host_id", LongType(), True),
        StructField("host_name", StringType(), True),
        StructField("host_since", StringType(), True),  # Read as StringType first to handle CSV date format safely
        StructField("host_location", StringType(), True),
        StructField("host_is_superhost", StringType(), True),
        StructField("host_listings_count", IntegerType(), True),
        StructField("neighbourhood", StringType(), True),
        StructField("neighbourhood_cleansed", StringType(), True),
        StructField("neighbourhood_group_cleansed", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("property_type", StringType(), True),
        StructField("room_type", StringType(), True),
        StructField("accommodates", IntegerType(), True),
        StructField("bathrooms", DoubleType(), True),
        StructField("bedrooms", IntegerType(), True),
        StructField("beds", IntegerType(), True),
        StructField("price", StringType(), True),  # Raw string format: "$150.00"
        StructField("minimum_nights", IntegerType(), True),
        StructField("maximum_nights", IntegerType(), True),
        StructField("availability_30", IntegerType(), True),
        StructField("availability_60", IntegerType(), True),
        StructField("availability_90", IntegerType(), True),
        StructField("availability_365", IntegerType(), True),
        StructField("number_of_reviews", IntegerType(), True),
        StructField("number_of_reviews_ltm", IntegerType(), True),
        StructField("reviews_per_month", DoubleType(), True),
        StructField("review_scores_rating", DoubleType(), True),
        StructField("review_scores_cleanliness", DoubleType(), True),
        StructField("review_scores_checkin", DoubleType(), True),
        StructField("review_scores_communication", DoubleType(), True),
        StructField("review_scores_location", DoubleType(), True),
        StructField("review_scores_value", DoubleType(), True),
        StructField("calculated_host_listings_count", IntegerType(), True),
    ])

REQUIRED_COLUMNS = [field.name for field in get_raw_listings_schema().fields]
