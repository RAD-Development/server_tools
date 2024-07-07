"""Validate Jeevesjr."""

import logging
import sys

from server_tools.common import configure_logger
from server_tools.components import discord_notification, zpool_tests


def main() -> None:
    """Main."""
    configure_logger(level="DEBUG")
    logging.info("Starting Jeevesjr validation")

    errors: list[str] = []
    try:
        if zpool_errors := zpool_tests(("Main",)):
            errors.extend(zpool_errors)

    except Exception as error:
        logging.exception("Jeevesjr validation failed")
        errors.append(f"Jeevesjr validation failed: {error}")

    if errors:
        logging.error(f"Jeevesjr validation failed: \n{'\n'.join(errors)}")
        discord_notification("Jeevesjr validation", errors)

        sys.exit(1)

    logging.info("Jeevesjr validation passed")


if __name__ == "__main__":
    main()
