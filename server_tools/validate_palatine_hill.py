"""Validate palatine_hill."""

import logging
import sys
from os import environ

from server_tools.common import configure_logger
from server_tools.components import discord_notification, systemd_tests, zpool_tests


def main() -> None:
    """Main."""
    configure_logger(level=environ.get("LOG_LEVEL", "INFO"))
    logging.info("Starting palatine_hill validation")

    errors: list[str] = []
    try:
        if zpool_errors := zpool_tests(("ZFS-primary",)):
            errors.extend(zpool_errors)

        services = ("docker",)
        if systemd_errors := systemd_tests(services):
            errors.extend(systemd_errors)

    except Exception as error:
        logging.exception("palatine_hill validation failed")
        errors.append(f"palatine_hill validation failed: {error}")

    if errors:
        logging.error(f"palatine_hill validation failed: \n{"\n".join(errors)}")
        discord_notification("palatine_hill", errors)

        sys.exit(1)

    logging.info("palatine_hill validation passed")


if __name__ == "__main__":
    main()
