import logging
import sys

def setup_logger(name: str = "airiq", level_str: str = "INFO") -> logging.Logger:
    """Configures and returns a structured application logger."""
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger is re-initialized
    if logger.hasHandlers():
        return logger
        
    level = getattr(logging, level_str.upper(), logging.INFO)
    logger.setLevel(level)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
