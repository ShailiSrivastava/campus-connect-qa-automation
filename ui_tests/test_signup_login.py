import uuid
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytestmark = [pytest.mark.ui]


@pytest.mark.smoke
def test_signup_and_login_e2e_flow(driver, ui_base_url):
    """E2E Flow: Complete user registration followed by successful login to dashboard."""
    unique_id = uuid.uuid4().hex[:8]
    full_name = f"Alex Student {unique_id}"
    email = f"alex_{unique_id}@campus.edu"
    password = "SecurePassword123!"
    college = "MIT School of Engineering"

    # Step 1: Navigate to registration page
    driver.get(f"{ui_base_url}/#/register")
    wait = WebDriverWait(driver, 10)

    # Locate registration form inputs
    name_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Shaili']")))
    email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    college_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Jain University']")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button.auth-submit")

    # Step 2: Fill registration form
    name_input.send_keys(full_name)
    email_input.send_keys(email)
    password_input.send_keys(password)
    college_input.send_keys(college)
    submit_btn.click()

    # Step 3: Verify registration success & automatic redirect to login
    wait.until(EC.url_contains("#/login"))

    # Step 4: Perform login with newly created account
    login_email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    login_password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    login_btn = driver.find_element(By.CSS_SELECTOR, "button.auth-submit")

    login_email_input.clear()
    login_email_input.send_keys(email)
    login_password_input.clear()
    login_password_input.send_keys(password)
    login_btn.click()

    # Step 5: Verify dashboard/feed navigation
    wait.until(EC.url_contains("#/feed"))
    navbar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cc-navbar")))
    assert navbar.is_displayed(), "Navbar should be visible on Feed dashboard"


def test_invalid_login_shows_error_message(driver, ui_base_url):
    """Negative UI: Verify error message is rendered when entering invalid credentials."""
    driver.get(f"{ui_base_url}/#/login")
    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button.auth-submit")

    email_input.clear()
    email_input.send_keys(f"nonexistent_{uuid.uuid4().hex[:6]}@campus.edu")
    password_input.clear()
    password_input.send_keys("WrongPass123!")
    submit_btn.click()

    # Verify error message element appears
    error_msg = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".auth-message")))
    assert len(error_msg.text.strip()) > 0, "Error message text should not be empty"
    assert "feed" not in driver.current_url, "Should not redirect to feed on failed login"


@pytest.mark.smoke
def test_logout_flow(authenticated_ui_driver, ui_base_url):
    """E2E Flow: Logged in user clicks Logout and is returned to the login screen."""
    driver = authenticated_ui_driver["driver"]
    wait = WebDriverWait(driver, 10)

    # Click logout button in navbar
    logout_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cc-logout")))
    logout_btn.click()

    # Verify redirect back to login
    wait.until(EC.url_contains("#/login"))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.auth-submit")))

    # Verify token is cleared from localStorage
    token = driver.execute_script("return localStorage.getItem('token');")
    assert token is None, "Token must be removed from localStorage after logout"
