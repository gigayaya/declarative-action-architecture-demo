from lib.action_layer import BaseAPITest


class TestAPI(BaseAPITest):
    """
    Test Layer: Defines the test cases using declarative steps.
    """
    DEMO_URL = "https://api.restful-api.dev/objects"
    INVALID_URL = DEMO_URL + "/invalid_endpoint"

    def test_get_request_success(self):
        self.request_by_get_and_success(url=self.DEMO_URL)
    
    def test_get_request_failure(self):
        self.request_by_get_and_failure(url=self.INVALID_URL)

    def test_get_object_by_id(self):
        api_response = self.request_by_get_and_success(url=self.DEMO_URL, params={"id": "3"})
        self.check_response_with_id(response=api_response, expected_ids=["3"])

    def test_get_objects_by_ids(self):
        api_response = self.request_by_get_and_success(url=self.DEMO_URL, params=[("id", "3"), ("id", "5"), ("id", "10")])
        self.check_response_with_id(response=api_response, expected_ids=["3", "5", "10"])
