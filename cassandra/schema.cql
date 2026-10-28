-- Cassandra Schema for AirIQ
-- Keyspace Definition
CREATE KEYSPACE IF NOT EXISTS airbnb_intelligence
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE airbnb_intelligence;

-- Table 1: Listings Partitioned by City and Country
-- Primary query pattern: Get listings by city and country, ordered by listing_id
CREATE TABLE IF NOT EXISTS airbnb_intelligence.listings_by_city (
    country text,
    city text,
    listing_id bigint,
    name text,
    neighbourhood text,
    latitude double,
    longitude double,
    room_type text,
    property_type text,
    accommodates int,
    bedrooms double,
    bathrooms double,
    price double,
    currency text,
    min_nights int,
    number_of_reviews int,
    review_scores_rating double,
    PRIMARY KEY ((country, city), listing_id)
);

-- Table 2: Listings Partitioned by City and Room Type
-- Query pattern: Filter listings by city and room type, ordered by price descending
CREATE TABLE IF NOT EXISTS airbnb_intelligence.listings_by_room_type (
    country text,
    city text,
    room_type text,
    price double,
    listing_id bigint,
    neighbourhood text,
    accommodates int,
    bedrooms double,
    bathrooms double,
    review_scores_rating double,
    PRIMARY KEY ((country, city, room_type), price, listing_id)
) WITH CLUSTERING ORDER BY (price DESC, listing_id ASC);

-- Table 3: Summary aggregates precomputed by Spark batch jobs
CREATE TABLE IF NOT EXISTS airbnb_intelligence.city_summary_metrics (
    country text,
    city text,
    total_listings bigint,
    avg_price double,
    median_price double,
    min_price double,
    max_price double,
    avg_rating double,
    updated_at timestamp,
    PRIMARY KEY (country, city)
);
