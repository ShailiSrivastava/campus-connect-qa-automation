import pytest
import requests

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_get_profile_valid_token(api_base_url, auth_headers, registered_user):
    """Positive: Fetch current user profile with valid Bearer token."""
    url = f"{api_base_url}/api/user/profile"
    response = requests.get(url, headers=auth_headers)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is True
    assert "user" in body
    user_data = body["user"]
    assert user_data["email"] == registered_user["email"]
    assert user_data["name"] == registered_user["name"]
    assert "password" not in user_data, "Password must not be returned in profile response"


def test_get_profile_missing_token(api_base_url):
    """Negative: Accessing profile without authorization token should return 401."""
    url = f"{api_base_url}/api/user/profile"
    response = requests.get(url)

    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is False
    assert "No token provided" in body.get("message", "")


def test_get_profile_invalid_token(api_base_url):
    """Negative: Accessing profile with an invalid/malformed token should return 401."""
    url = f"{api_base_url}/api/user/profile"
    invalid_headers = {
        "Authorization": "Bearer invalid_gibberish_token_12345",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=invalid_headers)

    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is False
    assert "Invalid token" in body.get("message", "")


@pytest.mark.smoke
def test_update_profile_valid_data(api_base_url, auth_headers):
    """Positive: Update user profile bio, branch, and year."""
    url = f"{api_base_url}/api/user/update"
    payload = {
        "bio": "Building scalable QA automation frameworks & distributed systems.",
        "branch": "Computer Science & Engineering",
        "year": "Final Year 2026"
    }
    response = requests.put(url, json=payload, headers=auth_headers)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is True
    assert "Profile updated successfully" in body.get("message", "")
    assert "user" in body
    user = body["user"]
    assert user["bio"] == payload["bio"]
    assert user["branch"] == payload["branch"]
    assert user["year"] == payload["year"]


def test_update_profile_unauthorized(api_base_url):
    """Negative: Updating profile without token should return 401."""
    url = f"{api_base_url}/api/user/update"
    payload = {
        "bio": "Unauthorized update attempt",
        "branch": "IT",
        "year": "3rd"
    }
    response = requests.put(url, json=payload)

    assert response.status_code == 401
    body = response.json()
    assert body.get("success") is False


def test_update_profile_special_characters_and_emojis(api_base_url, auth_headers):
    """Edge Case: Update bio with multi-line text, emojis, markdown, and unicode."""
    url = f"{api_base_url}/api/user/update"
    payload = {
        "bio": "🚀 Full-Stack AI Engineer | Python 🐍 & React ⚛️ | Building @ CampusConnect ✨\nLine 2: <script>alert(1)</script>",
        "branch": "AI & Robotics",
        "year": "4th Year"
    }
    response = requests.put(url, json=payload, headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    assert body["user"]["bio"] == payload["bio"]


def test_update_profile_empty_payload(api_base_url, auth_headers):
    """Edge Case: Send empty update body without crashing the server."""
    url = f"{api_base_url}/api/user/update"
    response = requests.put(url, json={}, headers=auth_headers)

    assert response.status_code == 200
    assert response.json().get("success") is True
