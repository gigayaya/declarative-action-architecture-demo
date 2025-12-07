from lib.api.action_layer import BaseAPITest


class TestDeviceUpgrade(BaseAPITest):
    """
    Test Layer: Demonstrates the Composite Action Pattern.
    """
    DEMO_URL = "https://api.restful-api.dev/objects"
    OLD_PHONE_NAME = "iPhone 12"
    OLD_PHONE_DATA = {"color": "Blue", "storage": "64GB"}
    NEW_PHONE_NAME = "iPhone 15"

    def test_upgrade_old_phone_to_new_phone(self):
        """
        Scenario: User upgrades their old phone to a new phone.
        The 'perform_device_upgrade' Composite Action handles the entire business logic:
        - Migrating data
        - Creating new device
        - Recycling old device
        - Verifying the upgrade result
        """
        old_phone = self.create_object_and_verify(url=self.DEMO_URL, name=self.OLD_PHONE_NAME, data=self.OLD_PHONE_DATA)
        old_phone_id = self.get_object_id(object_data=old_phone)
        self.perform_device_upgrade(url=self.DEMO_URL, old_device_id=old_phone_id, new_device_name=self.NEW_PHONE_NAME)
