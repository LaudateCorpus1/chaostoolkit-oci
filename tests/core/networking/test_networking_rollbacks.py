# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

import pytest

from unittest.mock import MagicMock, patch

from oci.exceptions import ServiceError

from chaoslib.exceptions import ActivityFailed

from chaosoci.core.networking.rollbacks import (delete_nat_gateway_rollback)


@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_nat_gateway_rollback(oci_client):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    vcn_id = "ocid1.vcn.oc1.phx.amaaaaaapwxjxiqavc6zohqv4whr6y65qwwjcexhexeje55v5wiarr5n24nq"

    c_ids = [c_id, ""]
    vcn_ids = [vcn_id, ""]

    for c in c_ids:
        for v in vcn_ids:
            if v == vcn_id and c == c_id:
                with pytest.raises(ServiceError) as s:
                    delete_nat_gateway_rollback(compartment_id=c, vcn_id=v)
                    network_client.create_nat_gateway.assert_called_with(compartment_id=c, vcn_id=v)
            else:
                with pytest.raises(ActivityFailed) as f:
                    delete_nat_gateway_rollback(c,v)
                assert 'A compartment id or a VCN id is required.'