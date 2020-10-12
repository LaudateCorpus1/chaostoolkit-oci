# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["delete_nat_rollback"]

from random import choice
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosoci import oci_client
from chaosoci.types import OCIResponse

from logzero import logger

from oci.config import from_file
from oci.core import VirtualNetworkClient
from oci.core.models import CreateNatGatewayDetails

from .common import (get_nat_gateways,
                     get_route_tables)

from .filters import (filter_nat_gateways,
                      filter_route_tables)


def delete_nat_gateway_rollback(compartment_id: str, vcn_id: str,
                                force: bool = False,
                                configuration: Configuration = None,
                                secrets: Secrets = None) -> OCIResponse:
    """
    Recreates a NAT gateway in the given compartment for a VCN.

    Parameters:
                Required:
                    - compartment_id: compartment id
                    - vcn_id: id of the vcn where to create the NAT gateway
    """
    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=True)

    if not compartment_id or not vcn_id:
        raise ActivityFailed('A compartment id or a VCN id is required.')

    ret = client.create_nat_gateway(CreateNatGatewayDetails(
                                      compartment_id=compartment_id,
                                      vcn_id=vcn_id))
    logger.debug(ret.data)
    return ret.data
