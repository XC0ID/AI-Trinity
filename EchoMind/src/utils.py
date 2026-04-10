# =============================================
# EchoMind — Utility Functions
# =============================================

import yaml
import os
from loguru import logger
from datetime import datetime


def load_config(path: str = "config.yaml") -> dict:
    """Load YAML config file."""
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    logger.info(f"Config loaded from {path}")
    return config


def setup_logger(log_level: str = "INFO"):
    """Setup loguru logger."""
    logger.remove()
    logger.add(
        "logs/echomind.log",
        rotation="1 day",
        retention="7 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level=log_level,
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}"
    )
    return logger


def format_timestamp() -> str:
    """Return formatted current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate long text for display."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def clean_message(text: str) -> str:
    """Clean and normalize user input."""
    return text.strip()


def format_chat_history(history: list) -> str:
    """Format chat history as readable string."""
    formatted = []
    for msg in history:
        role = "You" if msg["role"] == "user" else "EchoMind"
        formatted.append(f"{role}: {msg['content']}")
    return "\n".join(formatted)
