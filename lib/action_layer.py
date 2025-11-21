import pytest

@pytest.mark.usefixtures("generate_api_client")
class BaseAPITest:
    """
    Action Layer: Base class for API tests providing common utility methods.
    This layer contains helper functions that perform actions and include assertions.
    """

    @pytest.fixture(autouse=True)
    def setup_api_client(self, generate_api_client):
        """
        Automatically injects the api_client fixture into the class instance.
        This makes self.api_client available to all test methods and helpers.
        """
        self.api_client = generate_api_client

    def request_by_get_and_success(self, url, params=None, headers=None):
        """
        Sends a GET request and asserts that the response status code is 200.

        Args:
            url (str): The URL to send the request to.
            params (dict, optional): Query parameters to include in the request.
            headers (dict, optional): Headers to include in the request.

        Returns:
            Response: The response object.
        """
        response = self.api_client.get(url, params=params, headers=headers)
        http_status = response.status_code
        assert http_status == 200, f"Expected status code 200, got {http_status}"
        return response
    
    def request_by_get_and_failure(self, url, params=None, headers=None):
        """
        Sends a GET request and asserts that the response status code is NOT 200.

        Args:
            url (str): The URL to send the request to.
            params (dict, optional): Query parameters to include in the request.
            headers (dict, optional): Headers to include in the request.

        Returns:
            Response: The response object.
        """
        response = self.api_client.get(url, params=params, headers=headers)
        http_status = response.status_code
        assert http_status != 200, f"Expected non-200 status code, got {http_status}"
        return response

    def check_response_with_id(self, response, expected_ids: list):
        """
        Verifies that the response contains the expected list of IDs.

        Args:
            response (Response): The response object containing JSON data.
            expected_ids (list): A list of expected IDs to verify against the response.

        Raises:
            AssertionError: If the IDs in the response do not match the expected IDs.
        """
        data = response.json()
        data = data if data is not None else []
        returned_ids = {item.get("id") for item in data if isinstance(item, dict)}
        assert returned_ids == set(expected_ids), f"Unexpected ids returned: {returned_ids}"

