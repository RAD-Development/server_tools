"""Validate Jeeves."""

import logging
import sys
from re import search

from server_tools.common import bash_wrapper, configure_logger
from server_tools.zfs import Zpool

ZPOOL_CAPACITY_THRESHOLD = 90


def zpool_tests() -> list[str] | None:
    """Test zpool."""
    logging.info("Testing zpool")
    errors: list[str] = []
    for pool_name in ("media", "storage", "torrenting"):
        pool = Zpool(pool_name)
        if pool.health != "ONLINE":
            errors.append(f"{pool.name} is {pool.health}")
        if pool.capacity >= ZPOOL_CAPACITY_THRESHOLD:
            errors.append(f"{pool.name} is low on space")

    upgrade_status = bash_wrapper("zpool upgrade")
    if not search(r"Every feature flags pool has all supported and requested features enabled.", upgrade_status):
        errors.append("ZPool out of date")

    return errors


def main() -> None:
    """Main."""
    configure_logger(level="DEBUG")
    logging.info("Starting jeeves validation")

    errors = zpool_tests()

    if errors:
        logging.error("Jeeves validation failed")
        for error in errors:
            logging.error(error)
        sys.exit(1)

    logging.info("Jeeves validation passed")


if __name__ == "__main__":
    main()
