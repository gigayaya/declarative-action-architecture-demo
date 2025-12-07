import pytest
from lib.web.playwright_physical_layer import PlaywrightDriver
from lib.web.amazon_constants import AmazonSelectors

class AmazonActionLayer:
    """
    Action Layer: Business logic for Amazon.com tests.
    """

    @pytest.fixture(autouse=True)
    def setup_driver(self, amazon_web_client):
        self.web = amazon_web_client

    def navigate_to_home_and_verify_title(self):
        """
        Navigates to the Amazon homepage and verifies the title.

        Raises:
            AssertionError: If "Amazon" is not in the page title.
        """
        self.web.goto(AmazonSelectors.BASE_URL)
        title = self.web.get_title()
        assert "Amazon" in title, f"Expected title to contain 'Amazon', got '{title}'"

    def search_for_product_and_verify_result_list_not_empty(self, keyword):
        """
        Searches for a product and verifies that results are displayed.

        Args:
            keyword (str): The product name to search for.

        Raises:
            AssertionError: If no search results are found.
        """
        self.web.fill(AmazonSelectors.SEARCH_INPUT, keyword)
        self.web.click(AmazonSelectors.SEARCH_SUBMIT_BUTTON)
        self.web.wait_for_selector(AmazonSelectors.SEARCH_RESULT_SLOT)
        count = self.web.get_count(AmazonSelectors.SEARCH_RESULT_ITEM)
        assert count > 0, f"Expected >0 results for '{keyword}', got {count}"
    
    def search_for_product_and_expect_no_results(self, keyword):
        """
        Searches for a product and verifies that "No results" message is shown.

        Args:
            keyword (str): The non-existent product name to search for.

        Raises:
            AssertionError: If the "No results" message is not visible.
        """
        self.web.fill(AmazonSelectors.SEARCH_INPUT, keyword)
        self.web.click(AmazonSelectors.SEARCH_SUBMIT_BUTTON)
        no_result_english = self.web.is_visible(AmazonSelectors.NO_RESULTS_TEXT)

        assert no_result_english, f"Expected 'No results' message for '{keyword}'"

    def search_for_product_and_verify_result_count(self, keyword):
        """
        Searches for a product and verifies the page structure handles it gracefully.
        This is primarily for robustness testing of edge cases (e.g., special characters).

        Args:
            keyword (str): The search query, potentially containing special characters.

        Raises:
            AssertionError: If the search bar is no longer visible (implying a crash or blank page).
        """
        self.web.fill(AmazonSelectors.SEARCH_INPUT, keyword)
        self.web.click(AmazonSelectors.SEARCH_SUBMIT_BUTTON)
        assert self.web.is_visible(AmazonSelectors.SEARCH_INPUT), "Search bar missing, page might have crashed"

    def add_first_result_to_cart_and_verify_toast(self):
        """
        Adds the first item from the search results to the shopping cart and verifies the success toast.

        Raises:
            AssertionError: If the "Added to Cart" confirmation is not visible.
        """
        self.web.page.locator(AmazonSelectors.SEARCH_RESULT_LINK).first.click()
        self.web.wait_for_selector(AmazonSelectors.ADD_TO_CART_BUTTON)
        self.web.click(AmazonSelectors.ADD_TO_CART_BUTTON)
        self.web.wait_for_selector(AmazonSelectors.ADDED_TO_CART_CONFIRM_SELECTORS)
        is_visible = (self.web.is_visible(AmazonSelectors.ADDED_TO_CART_TEXT) or 
                      self.web.is_visible(AmazonSelectors.ADDED_TO_CART_SUCCESS_ID))
                      
        assert is_visible, "Expected 'Added to Cart' confirmation"

    def verify_cart_count(self, expected_count):
        """
        Verifies that the cart count indicator matches the expected number.

        Args:
            expected_count (int): The expected number of items in the cart.

        Raises:
            AssertionError: If the cart count does not match the expected value.
        """
        count_text = self.web.get_text(AmazonSelectors.CART_COUNT_BADGE)
        assert int(count_text) == expected_count, f"Expected cart count {expected_count}, got {count_text}"

    def navigate_to_cart_and_verify_page(self):
        """
        Navigates to the shopping cart page and verifies the page title.

        Raises:
            AssertionError: If "Cart" is not in the page title.
        """
        self.web.click(AmazonSelectors.NAV_CART)
        title = self.web.get_title()
        assert "Cart" in title, f"Expected 'Cart' in title, got '{title}'"

    def delete_item_from_cart_and_verify_empty(self):
        """
        Deletes the first item from the cart and verifies the empty cart message.

        Raises:
            AssertionError: If the "Your Amazon Cart is empty" message is not visible.
        """
        self.web.click(AmazonSelectors.CART_DELETE_BUTTON)
        self.web.wait_for_selector(AmazonSelectors.CART_EMPTY_MSG)
        assert self.web.is_visible(AmazonSelectors.CART_EMPTY_MSG), "Cart should be empty"

    def click_checkout_and_verify_login_prompt_or_empty_msg(self):
        """
        Clicks the 'Proceed to Checkout' button and expects a login prompt (since we are not logged in).

        Raises:
            AssertionError: If the page title does not indicate a Sign-In page.
        """
        self.web.click(AmazonSelectors.CHECKOUT_BUTTON)
        title = self.web.get_title()
        assert "Sign-In" in title or "Sign in" in title, f"Expected Sign-In page, got '{title}'"

    def navigate_to_navbar_link_and_verify_title(self, link_text):
        """
        Navigates to a specific link in the top navigation bar and verifies the page title.

        Args:
            link_text (str): The exact text of the link to click.

        Raises:
            AssertionError: If the link_text is not found in the new page title.
        """
        self.web.click(AmazonSelectors.NAV_BAR_LINK_TEMPLATE.format(link_text))
        title = self.web.get_title()
        assert link_text in title or link_text in title.replace("'", "&#39;"), f"Expected '{link_text}' in title, got '{title}'"

    def apply_brand_filter_and_verify_results(self, brand_name):
        """
        Applies a brand filter from the sidebar and verifies the results.
        
        Args:
            brand_name (str): The brand name to select and verify.

        Raises:
            AssertionError: If the first result's title does not contain the brand name.
        """
        self.web.click(AmazonSelectors.BRAND_FILTER_TEMPLATE.format(brand_name))
        first_result_text = self.web.get_text(AmazonSelectors.SEARCH_RESULT_TITLE)
        assert brand_name.lower() in first_result_text.lower(), f"Expected '{brand_name}' in first result '{first_result_text}'"

    def get_first_result_title_and_price(self):
        """
        Extracts the title and price of the first product in the search results.

        Returns:
            tuple: A tuple containing (title, price) as strings.
        """
        title = self.web.get_text(AmazonSelectors.SEARCH_RESULT_TITLE).strip()
        price_whole = self.web.get_text(AmazonSelectors.SEARCH_RESULT_PRICE_WHOLE).strip()
        price_fraction = self.web.get_text(AmazonSelectors.SEARCH_RESULT_PRICE_FRACTION).strip()
        price = f"{price_whole}.{price_fraction}"
        return title, price

    def click_first_result_and_verify_detail_page_matches(self, expected_title, expected_price):
        """
        Clicks the first search result and verifies that the detail page content matches expected values.

        Args:
            expected_title (str): The expected title (partial match).
            expected_price (str): The expected price string.

        Raises:
            AssertionError: If title or price do not match.
        """
        self.web.page.locator(AmazonSelectors.SEARCH_RESULT_LINK).first.click()
        detail_title = self.web.get_text(AmazonSelectors.PRODUCT_TITLE).strip()
        detail_price_whole = self.web.get_text(AmazonSelectors.DETAIL_PRICE_WHOLE).strip()
        detail_price_fraction = self.web.get_text(AmazonSelectors.DETAIL_PRICE_FRACTION).strip()
        detail_price = f"{detail_price_whole}.{detail_price_fraction}"
        assert expected_title[:20] in detail_title or detail_title[:20] in expected_title, "Title mismatch"
        assert expected_price == detail_price, f"Price mismatch: {expected_price} vs {detail_price}"

    def search_for_product_and_verify_handling(self, query):
        """
        Searches using a provided query (usually malformed or long) and verifies the application handles it (no crash).

        Args:
            query (str): The search query to test.

        Raises:
            AssertionError: If the page body is not visible.
        """
        self.web.fill(AmazonSelectors.SEARCH_INPUT, query)
        self.web.click(AmazonSelectors.SEARCH_SUBMIT_BUTTON)
        assert self.web.is_visible(AmazonSelectors.PAGE_BODY), "Page body missing"
