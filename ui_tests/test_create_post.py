import uuid
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytestmark = [pytest.mark.ui]


@pytest.mark.smoke
def test_create_and_view_post_flow(authenticated_ui_driver):
    """E2E Flow: Create a new campus post and verify it renders in the feed list."""
    driver = authenticated_ui_driver["driver"]
    wait = WebDriverWait(driver, 10)

    unique_id = uuid.uuid4().hex[:6]
    test_title = f"AI Research Symposium 2026 ({unique_id})"
    test_content = f"Looking for collaborators on our deep learning benchmark project! ID: {unique_id}"

    # Step 1: Locate CreatePost form elements
    title_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Post title']")))
    content_area = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='What are you working on?']")
    submit_btn = driver.find_element(By.CSS_SELECTOR, ".cc-create-actions button")

    # Step 2: Fill and submit post
    title_input.clear()
    title_input.send_keys(test_title)
    content_area.clear()
    content_area.send_keys(test_content)
    submit_btn.click()

    # Step 3: Verify confirmation status
    status_msg = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cc-status")))
    assert "Your post is live!" in status_msg.text or "live" in status_msg.text.lower()

    # Step 4: Verify the new post card appears in the feed
    post_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cc-postcard")))
    found_post = False
    for card in post_cards:
        if test_title in card.text:
            found_post = True
            break

    assert found_post, f"Newly created post '{test_title}' was not found in the feed cards"


def test_like_post_interactive_flow(authenticated_ui_driver):
    """UI Flow: Create a post and click the Like button to verify like count increments."""
    driver = authenticated_ui_driver["driver"]
    wait = WebDriverWait(driver, 10)

    # First ensure at least one post exists
    unique_id = uuid.uuid4().hex[:6]
    test_title = f"Like Flow Post #{unique_id}"
    title_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Post title']")))
    content_area = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='What are you working on?']")
    submit_btn = driver.find_element(By.CSS_SELECTOR, ".cc-create-actions button")

    title_input.send_keys(test_title)
    content_area.send_keys("Testing interactive like counter reaction.")
    submit_btn.click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cc-status")))

    # Find the newly created post's like button
    post_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cc-postcard")))
    target_card = None
    for card in post_cards:
        if test_title in card.text:
            target_card = card
            break

    assert target_card is not None, f"Could not find card with title '{test_title}'"

    like_button = target_card.find_element(By.CSS_SELECTOR, "button.cc-like")
    initial_text = like_button.text

    # Click like button
    like_button.click()

    # Verify text updated
    updated_text = like_button.text
    assert updated_text != initial_text or "1" in updated_text
