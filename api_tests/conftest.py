import os
import uuid
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_API_BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="session")
def api_base_url():
    """Returns the base API URL from environment or default."""
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


@pytest.fixture
def generate_user_data():
    """Factory fixture to generate unique user registration payload."""
    def _generator(custom_fields=None):
        unique_id = uuid.uuid4().hex[:8]
        user = {
            "name": f"QA Tester {unique_id}",
            "email": f"tester_{unique_id}@campus.edu",
            "password": "Password123!",
            "college": "Stanford University",
        }
        if custom_fields:
            user.update(custom_fields)
        return user
    return _generator


@pytest.fixture
def registered_user(api_base_url, generate_user_data):
    """Registers a brand new unique user and returns the user credentials dict."""
    user_data = generate_user_data()
    url = f"{api_base_url}/api/auth/register"
    response = requests.post(url, json=user_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 201, f"Failed to register fixture user: {response.text}"
    return user_data


@pytest.fixture
def auth_session(api_base_url, registered_user):
    """Logs in with registered user and returns a dict with token, user info, and credentials."""
    url = f"{api_base_url}/api/auth/login"
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    assert response.status_code == 200, f"Failed to login fixture user: {response.text}"
    data = response.json()
    assert data.get("success") is True, f"Login unsuccessful: {data}"
    assert "token" in data, f"Token missing from login response: {data}"
    return {
        "token": data["token"],
        "user": data.get("user", {}),
        "credentials": registered_user
    }


@pytest.fixture
def auth_token(auth_session):
    """Returns the JWT token string for an authenticated user."""
    return auth_session["token"]


@pytest.fixture
def auth_headers(auth_token):
    """Returns authorization headers containing the valid Bearer JWT."""
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def created_post(api_base_url, auth_headers):
    """Creates a post for the authenticated user and returns post response data."""
    unique_id = uuid.uuid4().hex[:6]
    payload = {
        "title": f"Test Post Title {unique_id}",
        "content": f"This is an automated test post content payload {unique_id}."
    }
    url = f"{api_base_url}/api/posts/create"
    response = requests.post(url, json=payload, headers=auth_headers)
    assert response.status_code == 201, f"Failed to create fixture post: {response.text}"
    data = response.json()
    assert data.get("success") is True, f"Post creation failed: {data}"
    return data.get("post", {})
