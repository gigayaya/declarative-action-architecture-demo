# E2E Automation Testing Design Pattern Demo - Declarative Action Architecture (DAA)

This project demonstrates a scalable and maintainable design pattern for End-to-End (E2E) automation testing, known as the **Declarative Action Architecture (DAA)**.

## The Declarative Action Architecture (DAA)

The DAA is an **advanced evolution of the traditional Layered Architecture**. It refines the separation of concerns by enforcing strict rules on logic and verification, resulting in tests that are both declarative and self-verifying.

The core philosophy is to divide the test automation into three distinct layers: **Test**, **Action**, and **Physical**.

### 1. Test Layer (The "What")
*   **Responsibility**: Defines the test scenarios and steps in a declarative, human-readable format.
*   **Rule**: **No logic allowed.** This layer must not contain conditional logic, loops, or direct calls to the system under test. It simply orchestrates the test using helper functions from the Action Layer.
*   **Goal**: To serve as "Living Documentation" that anyone (even non-coders) can understand.

### 2. Action Layer (The "How" + Verification)
*   **Responsibility**: Implements the high-level actions (helper functions) used by the Test Layer.
*   **Rule 1**: **Must verify itself.** Every action method must include an assertion to verify that the action was completed successfully. This prevents "false positives" where steps execute but achieve nothing.
*   **Rule 2**: **No direct system access.** It must interact with the System Under Test (SUT) *only* through the Physical Layer.
*   **Rule 3**: **Compose, Don't Repeat.** Complex business logic should be built by composing smaller, reusable "Atomic Actions" (Level 1) into "Composite Actions" (Level 2). This maximizes code reuse and ensures that if a low-level mechanism changes, you only need to update one Atomic Action.

#### The Power of Composite Actions (Building Blocks)
The Action Layer follows a "Building Block" philosophy:
1.  **Atomic Actions (Level 1)**: Small, single-purpose actions (e.g., `create_object`, `delete_object`). These are the fundamental bricks.
2.  **Composite Actions (Level 2)**: High-level business flows (e.g., `perform_device_upgrade`) built by assembling Atomic Actions.

**Advantages:**
*   **Scalability**: You can build infinitely complex scenarios from a finite set of Atomic Actions.
*   **Resilience**: Business logic is decoupled from implementation details.
*   **Readability**: Composite Actions read like a summary of the business process.

### 3. Physical Layer (The Mechanism)
*   **Responsibility**: Handles the direct interaction with the System Under Test (e.g., HTTP requests, Selenium WebDriver calls).
*   **Rule**: **Pure execution.** This layer contains no business logic or assertions. It faithfully transmits the request to the system and returns the raw response.

## Key Benefits

*   **📖 Extreme Readability**: The Test Layer is designed to be 100% declarative and logic-free. It reads like plain English, allowing anyone (PMs, manual testers, stakeholders) to instantly understand what is being tested without needing coding knowledge.
*   **⚡ Rapid Test Creation**: Writing new tests is incredibly fast and easy. By leveraging a vast library of pre-built, self-verifying actions from the Action Layer, you can compose complex test scenarios in seconds just by assembling existing blocks.
*   **🚫 Eliminate False Positives**: By enforcing assertions within the Action Layer, every step is guaranteed to verify its own success. No more "green tests" that actually failed to perform the action.
*   **🔧 High Maintainability**: The strict separation of concerns ensures that changes in the UI/API (Physical), business logic (Action), or scenarios (Test) are isolated and easy to manage.

## Example Walkthrough

### 1. API Example

**Test Layer** (`tests/api/test_demo.py`):
```python
def test_get_request_success(self):
    # Step 1: Perform action (Get request and verify success)
    self.request_by_get_and_success(self.DEMO_URL)
```

**Action Layer** (`lib/api/action_layer.py`):
```python
def request_by_get_and_success(self, url, params=None, headers=None):
    # Call Physical Layer
    response = self.api_client.get(url, params=params, headers=headers)
    
    # Self-Verification
    http_status = response.status_code
    assert http_status == 200, f"Expected status code 200, got {http_status}"
    
    return response
```

**Physical Layer** (`lib/api/physical_layer.py`):
```python
def get(self, url, params=None, headers=None):
    return self.requester.get(url, params=params, headers=headers)
```

### 2. Web Example (Playwright)

**Test Layer** (`tests/web/test_amazon_playwright.py`):
```python
def test_search_for_existing_product(self):
    self.navigate_to_home_and_verify_title()
    self.search_for_product_and_verify_result_list_not_empty("iPhone 15")
```

**Action Layer** (`lib/web/amazon_action_layer.py`):
```python
def search_for_product_and_verify_result_list_not_empty(self, keyword):
    # Call Physical Layer
    self.web.fill(AmazonSelectors.SEARCH_INPUT, keyword)
    self.web.click(AmazonSelectors.SEARCH_SUBMIT_BUTTON)
    
    # Self-Verification
    self.web.wait_for_selector(AmazonSelectors.SEARCH_RESULT_SLOT)
    count = self.web.get_count(AmazonSelectors.SEARCH_RESULT_ITEM)
    assert count > 0, f"Expected >0 results for '{keyword}', got {count}"
```

**Physical Layer** (`lib/web/playwright_physical_layer.py`):
```python
def fill(self, selector: str, text: str):
    self.page.fill(selector, text)
```

## Project Structure

```
demo/
├── lib/
│   ├── api/
│   │   ├── action_layer.py              # API Action Layer
│   │   └── physical_layer.py            # API Physical Layer
│   └── web/
│       ├── amazon_action_layer.py       # Web Action Layer (Amazon)
│       └── playwright_physical_layer.py # Web Physical Layer (Playwright)
├── tests/
│   ├── api/
│   │   ├── test_demo.py
│   │   └── test_composite_action.py
│   ├── web/
│   │   └── test_amazon_playwright.py
│   └── conftest.py
└── README.md
```

## Getting Started

### Prerequisites
*   Python 3.x
*   Install dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

### Running Tests

#### 1. Run API Tests
```bash
pytest tests/api/test_demo.py
```

#### 2. Run Web Tests (Amazon Demo)
```bash
pytest tests/web/test_amazon_playwright.py --headed
```
