"""Project logging setup."""
from __future__ import annotations

import logging
import sys


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Return an idempotently configured stdout logger."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        logger.addHandler(handler)
    return logger
