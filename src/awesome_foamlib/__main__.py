"""Main entry point for awesome-foamlib package."""

import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Print a greeting message from awesome-foamlib."""
    logger.info("Hello from awesome-foamlib!")


if __name__ == "__main__":
    main()
