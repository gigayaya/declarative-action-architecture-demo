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

    def get_object_id(self, object_data):
        """
        Helper to extract ID from object data.

        Args:
            object_data (dict): The object data dictionary.

        Returns:
            str: The ID of the object.
        """
        return object_data["id"]

    def get_object_name(self, object_data):
        """
        Helper to extract Name from object data.

        Args:
            object_data (dict): The object data dictionary.

        Returns:
            str: The name of the object.
        """
        return object_data["name"]

    def get_object_data(self, object_data):
        """
        Helper to extract Data from object data.

        Args:
            object_data (dict): The object data dictionary.

        Returns:
            dict: The data of the object.
        """
        return object_data.get("data")

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
        response = self.api_client.get(url=url, params=params, headers=headers)
        http_status = response.status_code
        assert http_status == 200, (
            f"GET {url} expected 200, got {http_status}. "
            f"params={params}, headers={headers}, response={response.text}"
        )
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
        response = self.api_client.get(url=url, params=params, headers=headers)
        http_status = response.status_code
        assert http_status != 200, (
            f"GET {url} expected non-200 status, got {http_status}. "
            f"params={params}, headers={headers}, response={response.text}"
        )
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

    def request_by_post_and_success(self, url, data=None, headers=None):
        """
        Sends a POST request and asserts that the response status code is 200 or 201.

        Args:
            url (str): The URL to send the request to.
            data (dict, optional): JSON data to include in the request body.
            headers (dict, optional): Headers to include in the request.

        Returns:
            Response: The response object.
        """
        response = self.api_client.post(url=url, data=data, headers=headers)
        http_status = response.status_code
        assert http_status in [200, 201], (
            f"POST {url} expected 200/201, got {http_status}. "
            f"payload={data}, headers={headers}, response={response.text}"
        )
        return response

    def request_by_delete_and_success(self, url, headers=None):
        """
        Sends a DELETE request and asserts that the response status code is 200 or 204.

        Args:
            url (str): The URL to send the request to.
            headers (dict, optional): Headers to include in the request.

        Returns:
            Response: The response object.
        """
        response = self.api_client.delete(url=url, headers=headers)
        http_status = response.status_code
        assert http_status in [200, 204], (
            f"DELETE {url} expected 200/204, got {http_status}. "
            f"headers={headers}, response={response.text}"
        )
        return response

    def create_object_and_verify(self, url, name, data):
        """
        Atomic Action: Creates an object and verifies the response.

        Args:
            url (str): The URL to send the request to.
            name (str): The name of the object to create.
            data (dict): The data of the object to create.

        Returns:
            dict: The created object data.
        """
        payload = {"name": name, "data": data}
        response = self.request_by_post_and_success(url=url, data=payload)
        
        resp_data = response.json()
        assert resp_data["name"] == name
        assert resp_data["data"] == data
        assert "id" in resp_data
        return resp_data

    def get_object_and_verify(self, url, obj_id, expected_name=None, expected_data=None):
        """
        Atomic Action: Gets an object and verifies its content.

        Args:
            url (str): The URL to send the request to.
            obj_id (str): The ID of the object to retrieve.
            expected_name (str, optional): The expected name of the object.
            expected_data (dict, optional): The expected data of the object.

        Returns:
            dict: The retrieved object data.
        """
        target_url = f"{url}/{obj_id}"
        response = self.request_by_get_and_success(url=target_url)
        
        resp_data = response.json()
        assert resp_data["id"] == obj_id
        if expected_name:
            assert resp_data["name"] == expected_name
        if expected_data:
            assert resp_data["data"] == expected_data
        return resp_data

    def delete_object_and_verify(self, url, obj_id):
        """
        Atomic Action: Deletes an object and verifies the response.

        Args:
            url (str): The URL to send the request to.
            obj_id (str): The ID of the object to delete.

        Returns:
            Response: The response object.
        """
        target_url = f"{url}/{obj_id}"
        response = self.request_by_delete_and_success(url=target_url)
        return response

    def get_object_and_expect_not_found(self, url, obj_id):
        """
        Atomic Action: Gets an object and expects a 404 Not Found.

        Args:
            url (str): The URL to send the request to.
            obj_id (str): The ID of the object to retrieve.

        Returns:
            Response: The response object.
        """
        target_url = f"{url}/{obj_id}"
        response = self.api_client.get(url=target_url)
        assert response.status_code == 404, (
            f"GET {target_url} expected 404, got {response.status_code}. "
            f"response={response.text}"
        )

    def perform_device_upgrade(self, url, old_device_id, new_device_name):
        """
        Composite Action: Simulates a device upgrade flow.
        
        Logic:
        1. Read old device data (Preferences).
        2. Create new device with old data (Migration).
        3. Delete old device (Recycle).
        4. Verify old device is gone.
        5. Verify new device has correct name and migrated data.

        Args:
            url (str): The URL to send the request to.
            old_device_id (str): The ID of the old device to upgrade from.
            new_device_name (str): The name of the new device device.

        Returns:
            dict: The new device object.
        """
        old_device = self.get_object_and_verify(url=url, obj_id=old_device_id)
        old_device_data = self.get_object_data(object_data=old_device)
        new_device = self.create_object_and_verify(url=url, name=new_device_name, data=old_device_data)
        self.delete_object_and_verify(url=url, obj_id=old_device_id)
        self.get_object_and_expect_not_found(url=url, obj_id=old_device_id)
        assert self.get_object_name(object_data=new_device) == new_device_name
        assert self.get_object_data(object_data=new_device) == old_device_data
        return new_device
