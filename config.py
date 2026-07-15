"""Configuration and logging bootstrap utilities for Jarvis.

This module owns application startup configuration so the rest of the codebase
can depend on one consistent settings object and one consistent logging setup.
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from settings import EnvironmentName, JarvisSettings, LogLevelName


LOG_FILE_NAME = "jarvis.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
VALID_ENVIRONMENTS: set[str] = {"development", "testing", "production"}
VALID_LOG_LEVELS: set[str] = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def _read_env_file(env_file_path: Path) -> dict[str, str]:
    """Read simple KEY=VALUE pairs from a local .env file if it exists."""

    # The parser intentionally supports the common .env subset needed for setup.
    if not env_file_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in env_file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _get_config_value(key: str, env_values: dict[str, str], default: str) -> str:
    """Return an environment value with process variables taking priority."""

    # Real environment variables should override local .env defaults.
    return os.getenv(key, env_values.get(key, default))


def _parse_bool(value: str) -> bool:
    """Convert a string configuration value into a boolean."""

    # This accepts common true values while keeping every other value false.
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_environment(value: str) -> EnvironmentName:
    """Validate the configured runtime environment name."""

    # Invalid values fall back safely to development mode.
    normalized_value = value.strip().lower()
    if normalized_value in VALID_ENVIRONMENTS:
        return normalized_value  # type: ignore[return-value]
    return "development"


def _parse_log_level(value: str) -> LogLevelName:
    """Validate the configured logging level name."""

    # Invalid values fall back safely to INFO logging.
    normalized_value = value.strip().upper()
    if normalized_value in VALID_LOG_LEVELS:
        return normalized_value  # type: ignore[return-value]
    return "INFO"


def load_settings() -> JarvisSettings:
    """Load environment variables and return validated application settings."""

    # Reading .env allows local development overrides without real secrets in Git.
    project_root = Path(__file__).resolve().parent
    env_values = _read_env_file(project_root / ".env")
    log_directory_value = _get_config_value("JARVIS_LOG_DIRECTORY", env_values, "")

    return JarvisSettings(
        app_name=_get_config_value("JARVIS_APP_NAME", env_values, "Jarvis"),
        environment=_parse_environment(
            _get_config_value("JARVIS_ENVIRONMENT", env_values, "development")
        ),
        log_level=_parse_log_level(_get_config_value("JARVIS_LOG_LEVEL", env_values, "INFO")),
        debug=_parse_bool(_get_config_value("JARVIS_DEBUG", env_values, "true")),
        project_root=project_root,
        log_directory=Path(log_directory_value) if log_directory_value else None,
    )


def configure_logging(settings: JarvisSettings) -> None:
    """Configure console and rotating file logging for the application."""

    # Ensure the log folder exists before creating the file handler.
    log_directory = settings.resolved_log_directory
    log_directory.mkdir(parents=True, exist_ok=True)

    # The root logger is configured once at application startup.
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)
    root_logger.handlers.clear()

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(settings.log_level)

    file_handler = RotatingFileHandler(
        filename=Path(log_directory) / LOG_FILE_NAME,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(settings.log_level)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
