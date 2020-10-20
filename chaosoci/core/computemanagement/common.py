# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["get_instance_pools"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed

from logzero import logger

from oci.core import ComputeManagementClient
from oci.core.models import (InstancePool)


def get_instance_pools(client: ComputeManagementClient = None,
                       compartment_id: str = None) -> List[InstancePool]:
    """
    Returns a complete, unfiltered list of instance pools in the
    compartment.
    """

    instance_pools = []
    instance_pools_raw = client.list_instance_pools(
                                  compartment_id=compartment_id)
    instance_pools.extend(instance_pools_raw.data)
    while instance_pools_raw.has_next_page:
        instance_pools_raw = client.list_instance_pools(
            compartment_id=compartment_id,
            page=instance_pools_raw.next_page)
        instance_pools.extend(instance_pools_raw.data)

    return instance_pools
