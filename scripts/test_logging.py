import sys
from pathlib import Path

# Add project root to PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.logging_config import setup_logging

logger = setup_logging()

def main():
    logger.info("Logging system initialized")
    logger.debug("This is a debug message")
    logger.warning("This is a warning")
    logger.error("This is an error example")

if __name__ == "__main__":
    main()
