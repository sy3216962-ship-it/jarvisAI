"""Application entry point for the Jarvis desktop assistant.

The main file stays intentionally small. Its job is to initialize configuration,
logging, and the first safe startup flow. Future assistant features should live
inside dedicated modules rather than being added directly here.
"""

from __future__ import annotations

import logging
import sys

from config import configure_logging, load_settings

logger = logging.getLogger(__name__)


def run() -> int:
    """Start the Jarvis application foundation and return a process exit code."""

    # Settings and logging are initialized before any future assistant modules run.
    settings = load_settings()
    configure_logging(settings)

    logger.info("Starting %s in %s mode.", settings.app_name, settings.environment)
    logger.info("Project root: %s", settings.project_root)
    logger.info("Log directory: %s", settings.resolved_log_directory)
    logger.info("Foundation startup completed successfully.")

    # Returning an exit code keeps the entry point testable and automation-friendly.
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Exception:
        # Any unexpected startup failure is logged with a full traceback.
        logger.exception("Jarvis failed during startup.")
        sys.exit(1)
