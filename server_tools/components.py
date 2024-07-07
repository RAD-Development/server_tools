"""Validate Jeeves."""

from __future__ import annotations

import logging
from re import search
from typing import TYPE_CHECKING

from server_tools.common import bash_wrapper
from server_tools.zfs import Zpool

if TYPE_CHECKING:
    from collections.abc import Sequence


def zpool_tests(pool_names: Sequence[str], zpool_capacity_threshold: int = 90) -> list[str] | None:
    """Check the zpool health and capacity.

    Args:
        pool_names (Sequence[str]): A list of pool names to test.
        zpool_capacity_threshold (int, optional): The threshold for the zpool capacity. Defaults to 90.

    Returns:
        list[str] | None: A list of errors if any.
    """
    logging.info("Testing zpool")

    errors: list[str] = []
    for pool_name in pool_names:
        pool = Zpool(pool_name)
        if pool.health != "ONLINE":
            errors.append(f"{pool.name} is {pool.health}")
        if pool.capacity >= zpool_capacity_threshold:
            errors.append(f"{pool.name} is low on space")

    upgrade_status = bash_wrapper("zpool upgrade")
    if not search(r"Every feature flags pool has all supported and requested features enabled.", upgrade_status):
        errors.append("ZPool out of date")

    return errors
