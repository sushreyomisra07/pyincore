# Copyright (c) 2019 University of Illinois and others. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/

import ast
import json
import os

import pytest

from pyincore import FragilityService, RepairService, IncoreClient
from pyincore import globals as pyglobals
from pyincore.globals import LOGGER
from pyincore.models.mappingset import MappingSet

logger = LOGGER


@pytest.fixture
def fragilitysvc(monkeypatch):
    client = IncoreClient(service_url=pyglobals.INCORE_API_DEV_URL, token_file_name=".incrtesttoken")
    return FragilityService(client)


@pytest.fixture
def repairsvc(monkeypatch):
    client = IncoreClient(service_url=pyglobals.INCORE_API_DEV_URL, token_file_name=".incrtesttoken")
    return RepairService(client)


def test_get_fragility_sets(fragilitysvc):
    metadata = fragilitysvc.get_dfr3_sets(demand_type="PGA", creator="cwang138")

    assert 'id' in metadata[0].keys()


def test_get_fragility_set(fragilitysvc):
    id = "5b47b2d7337d4a36187c61c9"
    metadata = fragilitysvc.get_dfr3_set(id)

    assert metadata['id'] == id


def test_search_fragility_sets(fragilitysvc):
    text = "Elnashai and Jeong"
    fragility_sets = fragilitysvc.search_dfr3_sets(text)

    assert len(fragility_sets)>0 and text in fragility_sets[0]['authors']


def test_match_fragilities_single_inventory(fragilitysvc):
    inventory = {}
    with open(os.path.join(pyglobals.TEST_DATA_DIR, "single_inventory.json"), 'r') as file:
        inventory = ast.literal_eval(file.read())
    mapping_id = '5b47b2d9337d4a36187c7564'
    key = "High-Retrofit Drift-Sensitive Fragility ID Code"
    mapping = MappingSet(fragilitysvc.get_mapping(mapping_id))
    frag_set = fragilitysvc.match_inventory(mapping, [inventory], key)

    assert inventory['id'] in frag_set.keys()


def test_match_fragilities_multiple_inventory(fragilitysvc):
    inventories = []
    with open(os.path.join(pyglobals.TEST_DATA_DIR, "multiple_inventory.json"), 'r') as file:
        inventories = ast.literal_eval(file.read())
    mapping_id = '5b47b350337d4a3629076f2c'
    key = "Non-Retrofit Fragility ID Code"
    mapping = MappingSet(fragilitysvc.get_mapping(mapping_id))
    frag_set = fragilitysvc.match_inventory(mapping, inventories, key)

    assert (inventories[0]['id'] in frag_set.keys()) and (len(frag_set) == len(inventories))


def test_get_fragility_mappings(fragilitysvc):
    mappings = fragilitysvc.get_mappings(hazard_type="earthquake", creator="cwang138")

    assert len(mappings)>0 and "id" in mappings[0].keys()


def test_get_fragility_mapping(fragilitysvc):
    mapping_id = "5b47b2d9337d4a36187c7563"
    mapping = fragilitysvc.get_mapping(mapping_id)

    assert mapping["id"] == mapping_id


def test_create_fragility_set(fragilitysvc):
    with open(os.path.join(pyglobals.TEST_DATA_DIR, "fragilityset.json"), 'r') as f:
        fragility_set = json.load(f)
    created = fragilitysvc.create_dfr3_set(fragility_set)

    assert "id" in created.keys()


def test_create_fragility_mapping(fragilitysvc):
    with open(os.path.join(pyglobals.TEST_DATA_DIR, "fragility_mappingset.json"), 'r') as f:
        mapping_set = json.load(f)
    created = fragilitysvc.create_mapping(mapping_set)

    assert "id" in created.keys()


def test_create_repair_set(repairsvc):
    with open(os.path.join(pyglobals.TEST_DATA_DIR, "repairset.json"), 'r') as f:
        repair_set = json.load(f)
    created = repairsvc.create_dfr3_set(repair_set)

    assert "id" in created.keys()


def test_create_repair_mapping(repairsvc):
    with open(os.path.join(pyglobals.TEST_DATA_DIR, "repair_mappingset.json"), 'r') as f:
        mapping_set = json.load(f)
    created = repairsvc.create_mapping(mapping_set)

    assert "id" in created.keys()


def test_get_repair_sets(repairsvc):
    metadata = repairsvc.get_dfr3_sets(hazard_type="earthquake", creator="incrtest")

    assert 'id' in metadata[0].keys()
