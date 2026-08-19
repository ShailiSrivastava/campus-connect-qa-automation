import os
import uuid
import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

DEFAULT_UI_BASE_URL = "http://localhost:5173"
DEFAULT_API_BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="session")
def ui_base_url():
    """Base URL for the frontend UI."""
    return os.getenv("UI_BASE_URL", DEFAULT_UI_BASE_URL).rstrip("/")


@pytest.fixture(scope="session")
def api_base_url():
    """Base URL for backend API."""
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


@pytest.fixture(scope="function")
def driver(request):
    """Selenium WebDriver fixture configured with Chrome."""
    chrome_options = Options()
    is_headless = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")

    if is_headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(2)

    yield driver

    # Screenshot on test failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        filename = f"{request.node.name}.png"
        filepath = os.path.join(screenshots_dir, filename)
        try:
            driver.save_screenshot(filepath)
            print(f"\n[Screenshot saved to {filepath}]")
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """PyTest hook to capture test outcome for screenshot triggers."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def generate_ui_user(api_base_url):
    """Creates a fresh registered user via API for fast, reliable UI test setup."""
    def _create():
        unique_id = uuid.uuid4().hex[:8]
        user_data = {
            "name": f"UI Student {unique_id}",
            "email": f"ui_student_{unique_id}@campus.edu",
            "password": "Password123!",
            "college": "Berkeley Engineering"
        }
        res = requests.post(f"{api_base_url}/api/auth/register", json=user_data)
        assert res.status_code == 201, f"Failed to register test user for UI test: {res.text}"
        return user_data
    return _create


@pytest.fixture
def authenticated_ui_driver(driver, ui_base_url, generate_ui_user):
    """Provides a WebDriver instance that has logged in and is on the Feed dashboard."""
    user = generate_ui_user()
    driver.get(f"{ui_base_url}/#/login")

    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button.auth-submit")

    email_input.clear()
    email_input.send_keys(user["email"])
    password_input.clear()
    password_input.send_keys(user["password"])
    submit_button.click()

    # Wait until navigated to feed
    wait.until(EC.url_contains("#/feed"))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cc-navbar")))

    return {
        "driver": driver,
        "user": user
    }
