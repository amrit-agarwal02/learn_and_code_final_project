from loguru import logger
import os

# Ensure log directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Remove default logger
logger.remove()

# Add file logger
logger.add(
    f"{log_dir}/news_sync.log",
    rotation="5 MB",          # Rotate after 5 MB
    retention="10 days",      # Keep logs for 10 days
    compression="zip",        # Compress old logs
    level="INFO",             # Minimum level to log
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Optional: Add console logger as well
logger.add(
    sink=lambda msg: print(msg, end=""),
    level="DEBUG"
)
