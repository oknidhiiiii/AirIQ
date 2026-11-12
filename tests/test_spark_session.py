import pytest
from pyspark.sql import SparkSession
from airiq.spark.session import get_spark_session, stop_spark_session
from airiq.spark.smoke_test import run_smoke_test

def test_spark_session_creation():
    """Test that SparkSession initializes correctly."""
    spark = get_spark_session()
    assert isinstance(spark, SparkSession)
    assert not spark._jsc.sc().isStopped()

def test_spark_smoke_test_function():
    """Test that the mandatory smoke test executes successfully."""
    result = run_smoke_test()
    assert result is True

def test_spark_session_cleanup():
    """Test clean shutdown of SparkSession."""
    spark = get_spark_session()
    stop_spark_session()
    assert spark._jsc.sc().isStopped()
