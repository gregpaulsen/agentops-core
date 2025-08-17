"""Structured logging setup for PaulyOps."""

import sys
from pathlib import Path
from loguru import logger

from config.loader import config


def setup_logging():
    """Setup structured logging with loguru."""
    # Remove default handler
    logger.remove()
    
    # Add console handler with human-readable format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=config.log_level,
        colorize=True
    )
    
    # Add JSON file handler for structured logging
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "paulyops_{time:YYYY-MM-DD}.json",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level=config.log_level,
        rotation="1 day",
        retention="30 days",
        compression="zip",
        serialize=True  # JSON format
    )
    
    # Add error file handler
    logger.add(
        log_dir / "errors_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="1 day",
        retention="30 days",
        compression="zip"
    )


def log_operation_start(operation: str, **context):
    """Log the start of an operation."""
    logger.info(f"🚀 Starting {operation}", extra={"operation": operation, "context": context})


def log_operation_success(operation: str, **context):
    """Log successful completion of an operation."""
    logger.info(f"✅ Completed {operation}", extra={"operation": operation, "context": context})


def log_operation_failure(operation: str, error: Exception, **context):
    """Log failure of an operation."""
    logger.error(
        f"❌ Failed {operation}: {error}",
        extra={"operation": operation, "error": str(error), "context": context}
    )


def log_provider_operation(provider: str, operation: str, **context):
    """Log provider-specific operations."""
    logger.info(
        f"🔧 {provider} {operation}",
        extra={"provider": provider, "operation": operation, "context": context}
    )


# Initialize logging
setup_logging()
