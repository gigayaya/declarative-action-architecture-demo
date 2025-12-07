from lib.web.amazon_action_layer import AmazonActionLayer

class TestAmazonPlaywright(AmazonActionLayer):
    """
    Test Layer: E2E tests for Amazon.com using DAA.
    Inherits from AmazonActionLayer to allow direct self.action() calls.
    """

    def test_search_for_existing_product(self):
        self.navigate_to_home_and_verify_title()
        self.search_for_product_and_verify_result_list_not_empty("iPhone 15")

    def test_search_for_non_existent_product(self):
        self.navigate_to_home_and_verify_title()
        self.search_for_product_and_expect_no_results("xyz_non_existent_random_string_123_456")

    def test_search_with_special_characters(self):
        self.navigate_to_home_and_verify_title()
        self.search_for_product_and_verify_result_count("@#$%^&*")

    def test_add_single_item_to_cart(self):
        self.navigate_to_home_and_verify_title()
        self.search_for_product_and_verify_result_list_not_empty("Basics")
        self.add_first_result_to_cart_and_verify_toast()

    def test_delete_item_from_cart(self):
        self.navigate_to_home_and_verify_title()
        self.search_for_product_and_verify_result_list_not_empty("Pen")
        self.add_first_result_to_cart_and_verify_toast()
        self.navigate_to_cart_and_verify_page()
        self.delete_item_from_cart_and_verify_empty()

    def test_proceed_to_checkout_with_empty_cart(self):
        self.navigate_to_home_and_verify_title()
        self.navigate_to_cart_and_verify_page()
        self.click_checkout_and_verify_login_prompt_or_empty_msg()

    def test_navigate_to_todays_deals(self):
        self.navigate_to_home_and_verify_title()
        self.navigate_to_navbar_link_and_verify_title("Today's Deals")

    def test_filter_results_by_brand(self):
        self.navigate_to_home_and_verify_title()
        self.search_for_product_and_verify_result_list_not_empty("Laptop")
        self.apply_brand_filter_and_verify_results("HP")

    def test_product_detail_consistency(self):
        self.navigate_to_home_and_verify_title()
        self.search_for_product_and_verify_result_list_not_empty("Apple MacBook Air 13")
        title, price = self.get_first_result_title_and_price()
        self.click_first_result_and_verify_detail_page_matches(expected_title=title, expected_price=price)

    def test_extremely_long_search_query(self):
        self.navigate_to_home_and_verify_title()
        long_query = "A" * 500
        self.search_for_product_and_verify_handling(long_query)
