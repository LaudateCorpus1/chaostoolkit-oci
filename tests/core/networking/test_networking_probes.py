# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

import pytest

from unittest import TestCase as T
from unittest.mock import MagicMock, patch

from chaoslib.exceptions import ActivityFailed

from chaosoci.core.networking.probes import (count_nat_gateways,
                                             filter_nat_gateways,
                                             count_route_tables,
                                             filter_route_tables)


@patch('chaosoci.core.networking.probes.filter_nat_gateways', autospec=True)
@patch('chaosoci.core.networking.probes.get_nat_gateways', autospec=True)
@patch('chaosoci.core.networking.probes.oci_client', autospec=True)
def test_count_nat_gateways(oci_client, get_nat_gateways, filter_nat_gateways):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    c_ids = [c_id, None]

    for id in c_ids:
        if id is None:
            with pytest.raises(ActivityFailed):
                count_nat_gateways(filters=filters, compartment_id=id)
            assert 'A valid compartment id is required.'
        else:
            count_nat_gateways(filters=filters, compartment_id=id)
            filter_nat_gateways.assert_called_with(
                nats=get_nat_gateways(oci_client, id), filters=filters
            )


    # for id in c_ids:
    #     if id == c_id:
    #         count_nat_gateways(filters=filters, compartment_id=id)
    #         filter_nat_gateways.assert_called_with(
    #             nats=get_nat_gateways(oci_client, id), filters=filters)
    #     else:
    #         with pytest.raises(ActivityFailed):
    #             count_nat_gateways(filters=filters, compartment_id=id)
    #         assert 'A valid compartment id is required.'


@patch('chaosoci.core.networking.probes.filter_nat_gateways', autospec=True)
@patch('chaosoci.core.networking.probes.get_nat_gateways', autospec=True)
@patch('chaosoci.core.networking.probes.oci_client', autospec=True)
def test_count_nat_gateways_ret_int(oci_client, get_nat_gateways,
                                    filter_nat_gateways):
    network_client = MagicMock()
    oci_client.return_value = network_client

    filter_nat_gateways.return_value = ['one', 'two', 'three']
    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    n = count_nat_gateways(filters=filters, compartment_id=c_id)
    T().assertEqual(n, 3)


@patch('chaosoci.core.networking.probes.filter_route_tables', autospec=True)
@patch('chaosoci.core.networking.probes.get_route_tables', autospec=True)
@patch('chaosoci.core.networking.probes.oci_client', autospec=True)
def test_count_route_tables(oci_client, get_route_tables, filter_route_tables):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    c_ids = [c_id]

    for id in c_ids:
        if id == c_id:
            count_route_tables(filters=filters, compartment_id=id)
            filter_route_tables.assert_called_with(
                route_tables=get_route_tables(
                    oci_client, id), filters=filters)
        else:
            with pytest.raises(ActivityFailed):
                count_route_tables(filters=filters, compartment_id=id)
            assert 'A valid compartment id is required.'
