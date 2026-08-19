import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytestmark = [pytest.mark.ui]


@pytest.mark.smoke
def test_update_profile_flow(authenticated_ui_driver, ui_base_url):
    """E2E Flow: Navigate to Profile, edit profile details (bio, branch, year), and save changes."""
    driver = authenticated_ui_driver["driver"]
    wait = WebDriverWait(driver, 10)

    # Navigate to Profile page via navbar link
    profile_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#/profile']")))
    profile_link.click()

    wait.until(EC.url_contains("#/profile"))
    edit_toggle_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ghost-button")))

    # Click "Edit" to open edit form
    edit_toggle_btn.click()

    # Locate edit form fields
    edit_form = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "form.profile-edit-form")))
    inputs = edit_form.find_elements(By.CSS_SELECTOR, "input")
    bio_textarea = edit_form.find_element(By.CSS_SELECTOR, "textarea")
    save_btn = edit_form.find_element(By.CSS_SELECTOR, "button.auth-submit")

    # Inputs in form: Name (index 0), College (index 1), Branch (index 2), Year (index 3)
    new_branch = "Artificial Intelligence & Data Science"
    new_year = "Senior 2026"
    new_bio = "Automation testing enthusiast passionate about CI/CD pipelines and high-quality software."

    if len(inputs) >= 4:
        inputs[2].clear()
        inputs[2].send_keys(new_branch)
        inputs[3].clear()
        inputs[3].send_keys(new_year)

    bio_textarea.clear()
    bio_textarea.send_keys(new_bio)

    # Click "Save changes"
    save_btn.click()

    # Wait for the updated bio to appear in the profile-bio element
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".profile-bio"), new_bio))

    # Verify updated bio appears on the profile page
    profile_bio = driver.find_element(By.CSS_SELECTOR, ".profile-bio")
    assert new_bio in profile_bio.text


def test_protected_route_unauthenticated_redirect(driver, ui_base_url):
    """Security UI: Unauthenticated access to /#/feed or /#/profile must redirect to /#/login."""
    wait = WebDriverWait(driver, 10)

    # Attempt to directly access feed without token
    driver.get(f"{ui_base_url}/#/feed")
    wait.until(EC.url_contains("#/login"))
    assert "login" in driver.current_url

    # Attempt to directly access profile without token
    driver.get(f"{ui_base_url}/#/profile")
    wait.until(EC.url_contains("#/login"))
    assert "login" in driver.current_url
