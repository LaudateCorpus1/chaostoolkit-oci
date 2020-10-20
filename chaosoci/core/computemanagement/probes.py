# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ['count_instance_pools']

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosoci import oci_client

from logzero import logger

from oci.config import from_file
from oci.core import ComputeManagementClient

from .common import (get_instance_pools)

from .filters import (filter_instance_pools)


def count_instance_pools(filters: List[Dict[str, Any]],
                         compartment_id: str = None,
                         configuration: Configuration = None,
                         secrets: Secrets = None) -> int:
    """
    Returns the number of Instance Pools in the compartment 'compartment_id'
    and according to the given filters.

    Please refer to:https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.InstancePool

    for details on the available filters under the 'parameters' section.
    """  # noqa: E501
    compartment_id = compartment_id or from_file().get('compartment')

    if compartment_id is None:
        raise ActivityFailed('A valid compartment id is required.')

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=False)

    filters = filters or None
    instance_pools = get_instance_pools(client, compartment_id)
    if filters is not None:
        return len(filter_instance_pools(instance_pools, filters=filters))
    else:
        return len(instance_pools)
