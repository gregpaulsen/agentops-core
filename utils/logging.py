import logging, os, sys
from typing import Optional

def _level_from_env() -> int:
    lvl = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, lvl, logging.INFO)

def setup_logging(level: Optional[int] = None) -> None:
    level = level or _level_from_env()
    root = logging.getLogger()
    if root.handlers:
        # already configured
        for h in root.handlers:
            h.setLevel(level)
        root.setLevel(level)
        return
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt))
    handler.setLevel(level)
    root.addHandler(handler)
    root.setLevel(level)

def get_logger(name: Optional[str] = None) -> logging.Logger:
    if not logging.getLogger().handlers:
        setup_logging()
    return logging.getLogger(name or "app")
