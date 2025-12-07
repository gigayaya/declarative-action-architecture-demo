import pytest
from lib.api.physical_layer import APIClient
from lib.web.playwright_physical_layer import PlaywrightDriver


@pytest.fixture(scope="class")
def generate_api_client():
    return APIClient()

@pytest.fixture
def amazon_web_client(page):
    driver = PlaywrightDriver(page)
    return driver
