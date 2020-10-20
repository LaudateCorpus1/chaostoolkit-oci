# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

import pytest

from unittest import TestCase as T
from unittest.mock import MagicMock, patch

from chaoslib.exceptions import ActivityFailed

from chaosoci.core.computemanagement.probes import (count_instance_pools,
                                                    filter_instance_pools)

@patch('chaosoci.core.computemanagement.probes.filter_instance_pools', autospec=True)
@patch('chaosoci.core.computemanagement.probes.get_instance_pools', autospec=True)
@patch('chaosoci.core.computemanagement.probes.oci_client', autospec=True)
def test_count_instance_pools(oci_client, get_instance_pools, filter_instance_pools):
    compute_management_client = MagicMock()
    oci_client.return_value = compute_management_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    c_ids = [c_id]

    for id in c_ids:
        if id == c_id:
            count_instance_pools(filters=filters, compartment_id=id)
            filter_instance_pools.assert_called_with(
                instance_pools=get_instance_pools(
                    oci_client, id), filters=filters)
        else:
            with pytest.raises(ActivityFailed) as f:
                count_instance_pools(filters=filters, compartment_id=id)
            assert 'A valid compartment id is required.'
