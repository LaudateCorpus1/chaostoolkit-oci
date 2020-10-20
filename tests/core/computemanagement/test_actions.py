# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

import pytest

from unittest.mock import MagicMock, patch

from chaoslib.exceptions import ActivityFailed

from chaosoci.core.computemanagement.actions import (stop_instance_pool_by_id,
                                                     stop_instance_pool_by_filters)
from chaosoci.util.constants import FILTER_ERR

@patch('chaosoci.core.computemanagement.actions.oci_client', autospec=True)
def test_stop_instance_pool_by_id(oci_client):
    compute_management_client = MagicMock()
    oci_client.return_value = compute_management_client
    instance_pool_id = "ocid1.instancepool.oc1.phx.aawnm2cdxq3naniep5dsiixtchqjuypcx7l7"
    instance_pool_ids = [instance_pool_id, ""]
    for id in instance_pool_ids:
        if id == instance_pool_id:
            stop_instance_pool_by_id(id)
            compute_management_client.stop_instance_pool.assert_called_with(instance_pool_id=id)
        else:
            with pytest.raises(ActivityFailed) as f:
                stop_instance_pool_by_id(id)
            assert 'An instance pool id is required.'

@patch('chaosoci.core.computemanagement.actions.filter_instance_pools', autospec=True)
@patch('chaosoci.core.computemanagement.actions.get_instance_pools', autospec=True)
@patch('chaosoci.core.computemanagement.actions.oci_client', autospec=True)
def test_stop_instance_pool_by_filters(oci_client, get_instance_pools,
                                       filter_instance_pools):
    compute_management_client = MagicMock()
    oci_client.return_value = compute_management_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"

    c_ids = [c_id, None]
    filters = [[{'display_name': 'random_name', 'region': 'uk-london-1'}],
               None]

    for c in c_ids:
        for f in filters:
            if c is None :
                with pytest.raises(ActivityFailed) as c_failed:
                    stop_instance_pool_by_filters(c, f)
                assert 'A compartment id or vcn id is required.'
            elif f is None:
                with pytest.raises(ActivityFailed) as f_failed:
                    stop_instance_pool_by_filters(c, f)
                assert FILTER_ERR
            else:
                with pytest.raises(ActivityFailed) as rt_failed:
                    stop_instance_pool_by_filters(c, f)
                    cdcdcompute_management_client.stop_instance_pool.assert_called_with(
                            filter_instance_pools(route_tables=get_instance_pools(
                                oci_client, c), filters=f)[0].id)
