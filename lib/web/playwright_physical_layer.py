from playwright.sync_api import Page

class PlaywrightDriver:
    """
    Physical Layer: Wrapper around Playwright Page object.
    This layer handles direct interaction with the browser.
    """
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        """
        Navigates to the given URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.page.goto(url)

    def fill(self, selector: str, text: str):
        """
        Fills the element specified by the selector with the given text.

        Args:
            selector (str): The CSS selector of the input element.
            text (str): The text to fill into the element.
        """
        self.page.fill(selector, text)

    def click(self, selector: str):
        """
        Clicks the element specified by the selector.

        Args:
            selector (str): The CSS selector of the element to click.
        """
        self.page.click(selector)
    
    def press(self, selector: str, key: str):
        """
        Presses a specific key on the element found by the selector.

        Args:
            selector (str): The CSS selector of the element.
            key (str): The key to press (e.g., 'Enter', 'ArrowDown').
        """
        self.page.press(selector, key)

    def get_text(self, selector: str) -> str:
        """
        Retrieves the text content of the element specified by the selector.

        Args:
            selector (str): The CSS selector of the element.

        Returns:
            str: The text content of the element.
        """
        return self.page.text_content(selector)

    def is_visible(self, selector: str) -> bool:
        """
        Checks if the element specified by the selector is visible.

        Args:
            selector (str): The CSS selector of the element.

        Returns:
            bool: True if the element is visible, False otherwise.
        """
        return self.page.is_visible(selector)

    def get_count(self, selector: str) -> int:
        """
        Counts the number of elements matching the selector.

        Args:
            selector (str): The CSS selector to count elements for.

        Returns:
            int: The count of matching elements.
        """
        return self.page.locator(selector).count()

    def get_attribute(self, selector: str, attribute: str) -> str:
        """
        Retrieves the value of a specific attribute of an element.

        Args:
            selector (str): The CSS selector of the element.
            attribute (str): The name of the attribute to retrieve.

        Returns:
            str: The value of the attribute, or None if not found (behavior depends on Playwright).
        """
        return self.page.get_attribute(selector, attribute)

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: int = 5000):
        """
        Waits for an element to reach a specific state.

        Args:
            selector (str): The CSS selector of the element to wait for.
            state (str, optional): The state to wait for (e.g., 'visible', 'attached'). Defaults to "visible".
            timeout (int, optional): Maximum time to wait in milliseconds. Defaults to 5000.
        """
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
    
    def get_title(self) -> str:
        """
        Retrieves the current page title.

        Returns:
            str: The title of the page.
        """
        return self.page.title()
