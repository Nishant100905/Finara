"""
Application Logging Configuration
"""

import logging
import logging.config
from pathlib import Path

# ==========================================================
# Log Directory
# ==========================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(
    exist_ok=True
)

LOG_FILE = LOG_DIR / "app.log"

# ==========================================================
# Logging Configuration
# ==========================================================

LOGGING_CONFIG = {

    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {

        "default": {

            "format": (
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(name)s | "
                "%(message)s"
            ),

            "datefmt": "%Y-%m-%d %H:%M:%S",
        },

    },

    "handlers": {

        "console": {

            "class": "logging.StreamHandler",

            "formatter": "default",

            "level": "INFO",

        },

        "file": {

            "class": "logging.FileHandler",

            "filename": str(LOG_FILE),

            "formatter": "default",

            "encoding": "utf-8",

            "level": "INFO",

        },

    },

    "root": {

        "handlers": [

            "console",

            "file",

        ],

        "level": "INFO",

    },

}


# ==========================================================
# Setup Function
# ==========================================================

def setup_logging():

    """
    Configure application logging.
    """

    logging.config.dictConfig(
        LOGGING_CONFIG
    )

    logger = logging.getLogger(__name__)

    logger.info(
        "=" * 60
    )

    logger.info(
        "Logging Initialized"
    )

    logger.info(
        "=" * 60
    )

    return logger