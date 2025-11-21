import pytest

from lib.physical_layer import APIClient


@pytest.fixture(scope="class")
def generate_api_client():
    return APIClient()
