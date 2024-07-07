"""Validate Jeeves."""

import logging
import sys

from server_tools.common import configure_logger
from server_tools.components import zpool_tests


def main() -> None:
    """Main."""
    configure_logger(level="DEBUG")
    logging.info("Starting jeeves validation")

    errors = zpool_tests(("Main",))

    if errors:
        logging.error("Jeeves validation failed")
        for error in errors:
            logging.error(error)
        sys.exit(1)

    logging.info("Jeeves validation passed")


if __name__ == "__main__":
    main()
