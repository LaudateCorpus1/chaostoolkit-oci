# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

import pytest

from unittest.mock import MagicMock, patch

from oci.core.models import CreateNatGatewayDetails
from oci.exceptions import ServiceError

from chaoslib.exceptions import ActivityFailed

from chaosoci.core.networking.rollbacks import (delete_nat_gateway_rollback)


@patch('chaosoci.core.networking.rollbacks.oci_client', autospec=True)
def test_delete_nat_gateway_rollback(oci_client):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    vcn_id = "ocid1.vcn.oc1.phx.amaaaaaapwxjxiqavc6zohqv4whr6y65qww"

    c_ids = [c_id, None]
    vcn_ids = [vcn_id, None]

    for c in c_ids:
        for v in vcn_ids:
            if c is None or v is None:
                with pytest.raises(ActivityFailed):
                    delete_nat_gateway_rollback(c, v)
                assert 'A compartment id or a VCN id is required.'
            else:
                delete_nat_gateway_rollback(c, v)
                network_client.create_nat_gateway.assert_called_with(
                    CreateNatGatewayDetails(
                        compartment_id=c,
                        vcn_id=v))
