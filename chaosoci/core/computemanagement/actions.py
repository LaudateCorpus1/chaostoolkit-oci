# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["stop_instance_pool_by_id", "stop_instance_pool_by_filters"]

from random import choice
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosoci import oci_client
from chaosoci.types import OCIResponse
from chaosoci.util.constants import FILTER_ERR

from logzero import logger

from oci.config import from_file
from oci.core import ComputeManagementClient

from .common import (get_instance_pools)

from .filters import (filter_instance_pools)


def stop_instance_pool_by_id(instance_pool_id: str, force: bool = False,
                             configuration: Configuration = None,
                             secrets: Secrets = None) -> OCIResponse:
    """
    Stops an instance pool using the instance pool id.

    Parameters:
                Required:
                    - instance_pool_id: the id of the route table
    """

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)
    if not instance_pool_id:
        raise ActivityFailed('An instance pool id is required.')

    ret = client.stop_instance_pool(instance_pool_id=instance_pool_id).data
    logger.debug("Instance pool %s stopped", instance_pool_id)
    return ret


def stop_instance_pool_by_filters(compartment_id: str,
                                  filters: Dict[str, Any], force: bool = False,
                                  configuration: Configuration = None,
                                  secrets: Secrets = None) -> OCIResponse:
    """
    Search for an instance pool using the specified filters and
    then stops it.

    Parameters:
                Required:
                    - compartment_id: the compartment id of the instance pool
                    - filters: the set of filters for the route table.
    Please refer to
    https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.InstancePool
    for the route table filters.
    """

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=False)

    if compartment_id is None:
        raise ActivityFailed('A compartment id is required.')
    else:
        unfiltered = get_instance_pools(client, compartment_id)

        if filters is None:
            raise ActivityFailed(FILTER_ERR)
        else:
            filtered = filter_instance_pools(unfiltered, filters)

            if (len(filtered) == 0):
                raise ActivityFailed(FILTER_ERR)
            else:
                ret = client.stop_instance_pool(filtered[0].id).data
                logger.debug("Instance pool %s stopped",
                             filtered[0].display_name)
                return ret
