# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["filter_instance_pools"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaosoci.util.constants import FILTER_ERR

from logzero import logger

from oci.core import ComputeManagementClient
from oci.core.models import (InstancePool)


def filter_instance_pools(instance_pools: List[InstancePool] = None,
                          filters: Dict[str, Any] = None
                          ) -> List[InstancePool]:
    """
    Return only those instance pools that match the filters provided.
    """
    instance_pools = instance_pools or None

    if instance_pools is None:
        raise ActivityFailed('No instance pools were found.')

    filters_set = {x for x in filters}

    available_filters_set = {x for x in instance_pools[0].attribute_map}

    # Partial filtering may return instance pools we do not want. We avoid it.
    if not filters_set.issubset(available_filters_set):
        raise ActivityFailed(FILTER_ERR)

    # Walk the instance pools and find those that match the given filters.
    filtered = []
    for instance_pool in instance_pools:
        sentinel = True
        for attr, val in filters.items():
            if val != getattr(instance_pool, attr, None):
                sentinel = False
                break

        if sentinel:
            filtered.append(instance_pool)

    return filtered
