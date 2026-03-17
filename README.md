# Playwright Python Example

This repository provides an example implementation of automated testing using Playwright with Python. The example demonstrates how to use the provided template to create and execute test cases for a sample web application.

## Purpose

The purpose of this example is to show how the Playwright template can be used to:
- Create Page Object classes for different pages of the application
- Write test cases that interact with these Page Objects using pytest
- Utilize common utility classes for consistent setup and teardown of test cases
- Use global setup and teardown to handle authentication via session storage
- Implement both public (non-authenticated) and authenticated test scenarios

## Built With

* [Python](https://www.python.org/) - Programming Language
* [Playwright](https://playwright.dev/python/docs/intro) - Framework for automated control of a web browser
* [pytest](https://docs.pytest.org/) - Testing framework for Python
* [pytest-playwright](https://github.com/microsoft/playwright-pytest) - Playwright plugin for pytest
* [HTML Reporter, JUnit Reporter](https://github.com/pytest-dev/pytest-html) - Reporting frameworks
* [python-dotenv](https://pypi.org/project/python-dotenv/) - For managing environment variables

## Tested Versions of Used Components

The version numbers of the used components are documented in the `requirements.txt` file within the repository.

## Getting Started

### Clone the Repository

Start by cloning the project:
```bash
git clone https://git.lab.proficom.de/templates/test-automation-getting-started-playwright
cd test-automation-getting-started-playwright/playwright-python/example
```

### Requirements

* Python 3.8 or higher must be set up on the respective execution environment
* pip package manager
* Playwright manages all necessary browsers (Chromium, Firefox, WebKit) automatically, so no manual installation is required

### Installation

To download all necessary dependencies, please navigate to the example folder and run the following commands:

```bash
pip install -r requirements.txt
playwright install
```

This will install:
- Playwright and pytest
- All required plugins (pytest-playwright, pytest-html, pytest-xdist, etc.)
- Browser binaries (Chromium, Firefox, WebKit)

### Updating Playwright (if needed)

To update Playwright to the latest version:

```bash
pip install --upgrade playwright pytest-playwright
playwright install
```

## Project Structure

```
example/
├── .auth/                          # Authentication state storage
│   └── user.json                   # Stored session data
├── e2e/
│   ├── common/                     # Common utilities and fixtures
│   │   ├── base_page.py           # Base class for all page objects
│   │   ├── browser_sync_utils.py  # Browser synchronization utilities
│   │   └── page_objects_fixture.py # pytest fixtures for page objects
│   ├── pageobjects/               # Page Object Model classes
│   │   ├── sign_in_page.py
│   │   ├── side_menu_page.py
│   │   ├── top_menu_page.py
│   │   ├── new_transaction_page.py
│   │   ├── personal_page.py
│   │   └── transaction_detail_page.py
│   ├── tests/
│   │   ├── authenticated/         # Tests requiring authentication
│   │   │   ├── global/            # Global setup and teardown
│   │   │   │   ├── global_setup.py    # Authentication setup
│   │   │   │   └── global_teardown.py # Authentication cleanup
│   │   │   └── test_new_and_check_transaction_suite.py
│   │   └── public/                # Public tests (no auth required)
│   │       ├── test_login_and_logout.py
│   │       └── test_login_and_logout_without_page_objects.py
│   └── reports/                   # Test execution reports
├── conftest.py                    # pytest configuration and fixtures
├── pytest.ini                     # pytest settings
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## Configuration

The example is configured in `conftest.py` to match the TypeScript `playwright.config.ts` settings:

### Browser Settings
- **Headless Mode**: `False` - Browser is visible by default
- **Browser Arguments**: `--start-maximized` - Browser starts maximized
- **Viewport**: `1440x900` - Default viewport size

### Timeouts
- **Action Timeout**: `10000ms` - Default timeout for all actions (clicks, fills, etc.)

### Test Execution
- **Base URL**: Set via environment variable `BASE_URL` (defaults to RealWorldApp URL)
- **Screenshots**: `only-on-failure` - Captured automatically when tests fail
- **Videos**: `retain-on-failure` - Recorded and kept only for failed tests
- **Tracing**: `retain-on-failure` - Debug traces saved for failed tests

### Authentication
- **Storage State**: `.auth/user.json` - Session data for authenticated tests
- **Markers**: `@pytest.mark.authenticated` - Tests requiring pre-authentication
- **Markers**: `@pytest.mark.public` - Tests without authentication

## Test Execution from Command Line

### Basic Test Execution

```bash
# Run all tests (default: chromium browser)
pytest e2e/tests/

# Run tests with verbose output
pytest e2e/tests/ -v

# Note: Browser is visible by default (headless: False in conftest.py)
# To run in headless mode, you can override with --headed=false
pytest e2e/tests/ --headed=false

# Run specific test file
pytest e2e/tests/public/test_login_and_logout.py -v
```

### Multi-Browser Testing

```bash
# Run tests in Firefox
pytest e2e/tests/ --browser firefox

# Run tests in WebKit (Safari)
pytest e2e/tests/ --browser webkit

# Run tests in all browsers
pytest e2e/tests/ --browser chromium --browser firefox --browser webkit
```

### Parallel Execution

```bash
# Run tests in parallel with 2 workers
pytest e2e/tests/ -n 2

# Run tests in parallel with auto-detection of CPU cores
pytest e2e/tests/ -n auto
```

### Test Markers

```bash
# Run only public tests (no authentication required)
pytest e2e/tests/ -m public

# Run only authenticated tests
pytest e2e/tests/ -m authenticated

# Run specific test class
pytest e2e/tests/public/test_login_and_logout.py::TestLoginAndLogout -v
```

### Advanced Options

```bash
# Run with HTML report
pytest e2e/tests/ --html=e2e/reports/report.html --self-contained-html

# Run with specific timeout
pytest e2e/tests/ --timeout=120

# Run with retries on failure
pytest e2e/tests/ --retries=2

# Run in slow-mo mode (useful for debugging, browser already visible by default)
pytest e2e/tests/ --slowmo=1000
```

## Running Tests in Visual Studio Code

### 1. Prepare .env file

Create a `.env` file in the example root with the necessary environment variables:

```env
BASE_URL=http://frontend-ta-realworldapp.apps.os-prod.lab.proficom.de
TEST_USER_NAME=your_username
TEST_PASSWORD=your_password
```

The python-dotenv package automatically loads these variables, making them accessible via `os.getenv()`.

### 2. Run the Application

The AUT (Application Under Test) is the RealWorldApp reachable in the Accompio-Network under:
`http://frontend-ta-realworldapp.apps.os-prod.lab.proficom.de`

If you have a local version of [RealWorldApp](https://github.com/cypress-io/cypress-realworld-app), start it and adjust the `BASE_URL` in your `.env` file accordingly.

### 3. Setup Authentication (for Authenticated Tests)

Before running authenticated tests, you need to create authentication state:

```bash
python e2e/tests/authenticated/global/global_setup.py
```

This will:
1. Launch a browser
2. Navigate to the sign-in page
3. Login with your credentials from .env
4. Save the authentication state to `.auth/user.json`

### 4. Running Tests

#### From Command Line:
```bash
# Run all tests
pytest e2e/tests/ -v

# Run only public tests
pytest e2e/tests/public/ -v

# Run only authenticated tests (requires setup first)
pytest e2e/tests/authenticated/ -v
```

#### From VS Code:
1. Install the Python extension
2. Open the Testing panel (beaker icon)
3. Click "Configure Python Tests" and select pytest
4. Tests will appear in the Testing panel
5. Click the play button next to any test to run it

## Test Scenarios

### Public Tests (No Authentication Required)

1. **test_login_and_logout.py** - Demonstrates login/logout with Page Objects
   - Navigate to sign-in page
   - Login with valid credentials
   - Verify username is displayed
   - Logout successfully
   - Verify return to sign-in page

2. **test_login_and_logout_without_page_objects.py** - Same functionality using direct Playwright API
   - Shows alternative approach without Page Object abstraction
   - Direct locator usage for comparison

### Authenticated Tests (Requires Pre-Authentication)

1. **test_new_and_check_transaction_suite.py** - Sequential transaction workflow
   - **Test 1**: Create new transaction
     - Select contact
     - Set payment amount and note
     - Submit transaction
     - Verify submission success
   - **Test 2**: Verify transaction details
     - Navigate to personal transactions
     - Open first transaction
     - Verify amount matches

## Reports and Artifacts

After test execution, you'll find:

- **HTML Report**: `e2e/reports/pytest_report.html`
- **JUnit XML**: `test-results/results.xml`
- **Screenshots**: `e2e/reports/*.png` (on failure or where explicitly captured)
- **Videos**: Generated for failed tests (if configured)
- **Traces**: Available for debugging (on first retry)

## Troubleshooting

### Authentication Issues

If authenticated tests fail with timeout or are on `/signin`:
1. Ensure `.auth/user.json` exists and is not empty
2. Run `python e2e/tests/authenticated/global/global_setup.py` to generate auth state
3. Check your credentials in `.env` file

### Browser Not Found

If you get "Browser not found" error:
```bash
playwright install
```

### Import Errors

If you get import errors, ensure you're in the correct directory:
```bash
cd example
pytest e2e/tests/ -v
```

### Parallel Execution Issues

If tests fail in parallel but pass sequentially:
- Some tests may have dependencies on shared state
- Try running with `-n 1` or mark tests with `@pytest.mark.dependency()`
