import sys
from airiq.spark.session import get_spark_session, stop_spark_session
from airiq.utils.logging_utils import setup_logger

logger = setup_logger("airiq.spark.smoke_test")

def run_smoke_test() -> bool:
    """Executes a PySpark environment smoke test.
    
    Returns True if smoke test passes, False otherwise.
    """
    logger.info("Starting PySpark Environment Smoke Test...")
    
    try:
        # 1. Verify Imports & Session Creation
        spark = get_spark_session()
        logger.info("Step 1 PASSED: PySpark imports and SparkSession initialized.")
        
        # 2. Verify DataFrame Creation & Action
        test_data = [(1, "Listing A", 100.0), (2, "Listing B", 250.0)]
        df = spark.createDataFrame(test_data, ["id", "name", "price"])
        count = df.count()
        if count != 2:
            raise ValueError(f"Expected DataFrame count 2, got {count}")
        logger.info(f"Step 2 PASSED: Spark DataFrame created (count = {count}).")
        
        # 3. Verify Spark SQL Query
        df.createOrReplaceTempView("smoke_test_listings")
        sql_df = spark.sql("SELECT avg(price) as avg_price FROM smoke_test_listings")
        avg_price = sql_df.collect()[0]["avg_price"]
        if avg_price != 175.0:
            raise ValueError(f"Expected average price 175.0, got {avg_price}")
        logger.info(f"Step 3 PASSED: Spark SQL execution verified (avg_price = ${avg_price:.2f}).")
        
        # 4. Clean Shutdown
        stop_spark_session()
        logger.info("Step 4 PASSED: SparkSession shut down cleanly.")
        
        logger.info("==========================================")
        logger.info("  SPARK SMOKE TEST STATUS: PASSED!")
        logger.info("==========================================")
        return True

    except Exception as e:
        logger.error(f"SPARK SMOKE TEST FAILED! Error: {e}", exc_info=True)
        try:
            stop_spark_session()
        except Exception:
            pass
        return False

if __name__ == "__main__":
    success = run_smoke_test()
    sys.exit(0 if success else 1)
