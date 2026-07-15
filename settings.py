"""Application settings models for the Jarvis assistant.

This file defines typed configuration objects. Keeping settings in a dedicated
module makes future modules easier to configure without hardcoding values.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

EnvironmentName = Literal["development", "testing", "production"]
LogLevelName = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


@dataclass(frozen=True, slots=True)
class JarvisSettings:
    """Typed settings loaded from environment variables and safe defaults."""

    # The public assistant name used in logs, UI, and future conversations.
    app_name: str = "Jarvis"

    # The current runtime environment controls debugging and logging behavior.
    environment: EnvironmentName = "development"

    # The log level can be changed without modifying source code.
    log_level: LogLevelName = "INFO"

    # Debug mode enables more verbose diagnostics during local development.
    debug: bool = True

    # The project root is used to build stable paths for assets, logs, and plugins.
    project_root: Path = Path(__file__).resolve().parent

    # Logs are written below the repository's logs folder by default.
    log_directory: Path | None = None

    @property
    def resolved_log_directory(self) -> Path:
        """Return the configured log directory or the default project log folder."""

        # A property keeps path resolution centralized for every future module.
        return self.log_directory or self.project_root / "logs"
