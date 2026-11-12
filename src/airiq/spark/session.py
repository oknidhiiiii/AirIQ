from typing import Dict, Any, Optional
from pyspark.sql import SparkSession
from airiq.utils.config_loader import load_config
from airiq.utils.logging_utils import setup_logger

logger = setup_logger("airiq.spark.session")

_spark_session: Optional[SparkSession] = None

def get_spark_session(config: Optional[Dict[str, Any]] = None) -> SparkSession:
    """Returns an active SparkSession instance configured according to settings.
    
    Uses singleton pattern to avoid multiple JVM initializations.
    """
    global _spark_session
    
    if _spark_session is not None and not _spark_session._jsc.sc().isStopped():
        return _spark_session
        
    if config is None:
        config = load_config()
        
    spark_cfg = config.get("spark", {})
    app_name = spark_cfg.get("app_name", "AirIQ-Engine")
    master = spark_cfg.get("master", "local[8]")
    driver_mem = spark_cfg.get("driver_memory", "4g")
    executor_mem = spark_cfg.get("executor_memory", "4g")
    shuffle_partitions = str(spark_cfg.get("shuffle_partitions", 8))
    spark_log_level = spark_cfg.get("log_level", "WARN")
    
    logger.info(f"Initializing SparkSession [App: {app_name}, Master: {master}]")
    
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.driver.memory", driver_mem)
        .config("spark.executor.memory", executor_mem)
        .config("spark.sql.shuffle.partitions", shuffle_partitions)
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
    )
    
    _spark_session = builder.getOrCreate()
    _spark_session.sparkContext.setLogLevel(spark_log_level)
    
    logger.info(f"SparkSession created successfully (PySpark v{_spark_session.version})")
    return _spark_session

def stop_spark_session() -> None:
    """Stops active SparkSession safely if running."""
    global _spark_session
    if _spark_session is not None and not _spark_session._jsc.sc().isStopped():
        logger.info("Stopping active SparkSession...")
        _spark_session.stop()
        _spark_session = None
        logger.info("SparkSession stopped successfully.")
