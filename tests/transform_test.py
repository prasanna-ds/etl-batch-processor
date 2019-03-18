from unittest.mock import patch, MagicMock
from pathlib import Path
from nose.tools import assert_dict_equal
import pytest
import json

from batchprocessor.config.test import TestConfig as Config
from batchprocessor.transform import Transform

TEST_INPUT_DATA_DIR = Path(__file__).resolve().parent / 'inputs'

@pytest.fixture
def transform_data(path=Config.S3_FILE):
    with patch.object(Config,'S3_FILE', TEST_INPUT_DATA_DIR / 'immobilienscout24_berlin_20190113_test.json'):
        with open(Config.S3_FILE, 'r') as file:
            batchdata = []
            for line in file:
                batchdata.append(json.loads(line))
    return Transform(batchdata)

def test_transform(transform_data):
    assert len(transform_data.transform()) == 3

def test_dim_address(transform_data):
    actual_dim_address = transform_data.transform()[1]
    expected_dim_address = {
             'data.id': '56906504',
             'data.realEstate_address_city': 'Berlin',
             'data.realEstate_address_geoHierarchy_city_name': 'Berlin',
             'data.realEstate_address_geoHierarchy_country_name': 'Deutschland',
             'data.realEstate_address_geoHierarchy_quarter_name': 'Mitte (Mitte)',
             'data.realEstate_address_geoHierarchy_region_name': 'Berlin',
             'data.realEstate_address_postcode': '10115'
    }
    assert_dict_equal(expected_dim_address, actual_dim_address.to_dict(orient='records')[0], "oops, there's a bug...")
        
