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

Let's look at `test_get_request_success` to see how the DAA works in practice:

### 1. Test Layer (`tests/test_demo.py`)
Declarative steps describing *what* to do.
```python
def test_get_request_success(self):
    # Step 1: Perform action (Get request and verify success)
    self.request_by_get_and_success(self.DEMO_URL)
```

### 2. Action Layer (`lib/action_layer.py`)
The helper function `request_by_get_and_success` handles the logic and **self-verification**.
```python
def request_by_get_and_success(self, url, params=None, headers=None):
    # Call Physical Layer
    response = self.api_client.get(url, params=params, headers=headers)
    
    # Self-Verification (The "Assert" in Action)
    http_status = response.status_code
    assert http_status == 200, f"Expected status code 200, got {http_status}"
    
    return response
```

### 3. Physical Layer (`lib/physical_layer.py`)
The `get` method purely executes the HTTP request.
```python
def get(self, url, params=None, headers=None):
    # Direct interaction with 'requests' library
    return self.requester.get(url, params=params, headers=headers)
```

## Project Structure

```
demo/
├── lib/
│   ├── action_layer.py    # Action Layer (BaseAPITest)
│   └── physical_layer.py  # Physical Layer (APIClient)
├── tests/
│   ├── test_demo.py       # Test Layer (Test Cases)
│   └── conftest.py        # Pytest fixtures
└── README.md
```

## Getting Started

### Prerequisites
*   Python 3.x
*   Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running Tests
```bash
pytest tests/test_demo.py
```
