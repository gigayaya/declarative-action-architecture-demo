import requests


class APIClient:
    """
    Physical Layer: Client for making API requests.
    This layer handles the direct interaction with the system under test.
    """
    def __init__(self):
        """
        Initializes the APIClient.
        """
        self.requester = requests

    def get(self, url, params=None, headers=None):
        """
        Sends a GET request.

        Args:
            url (str): The URL to send the request to.
            params (dict, optional): Query parameters to include in the request.
            headers (dict, optional): Headers to include in the request.

        Returns:
            Response: The response object.
        """
        return self.requester.get(url, params=params, headers=headers)
    
    def post(self, url, data=None, headers=None):
        """
        Sends a POST request.

        Args:
            url (str): The URL to send the request to.
            data (dict, optional): JSON data to include in the request body.
            headers (dict, optional): Headers to include in the request.

        Returns:
            Response: The response object.
        """
        return self.requester.post(url, json=data, headers=headers)

    def put(self, url, data=None, headers=None):
        """
        Sends a PUT request.

        Args:
            url (str): The URL to send the request to.
            data (dict, optional): JSON data to include in the request body.
            headers (dict, optional): Headers to include in the request.

        Returns:
            Response: The response object.
        """
        return self.requester.put(url, json=data, headers=headers)

    def delete(self, url, headers=None):
        """
        Sends a DELETE request.

        Args:
            url (str): The URL to send the request to.
            headers (dict, optional): Headers to include in the request.

        Returns:
            Response: The response object.
        """
        return self.requester.delete(url, headers=headers)
