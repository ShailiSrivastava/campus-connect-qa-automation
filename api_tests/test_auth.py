import uuid
import pytest
import requests

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_register_valid_user(api_base_url, generate_user_data):
    """Positive: Register a new student user with valid payload."""
    payload = generate_user_data()
    url = f"{api_base_url}/api/auth/register"
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is True
    assert "User registered successfully" in body.get("message", "")


@pytest.mark.smoke
def test_login_valid_credentials(api_base_url, registered_user):
    """Positive: Log in with valid credentials and verify JWT and user payload."""
    url = f"{api_base_url}/api/auth/login"
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is True
    assert "token" in body
    assert isinstance(body["token"], str) and len(body["token"]) > 20
    assert "user" in body
    assert body["user"]["email"] == registered_user["email"]
    assert body["user"]["name"] == registered_user["name"]
    assert body["user"]["college"] == registered_user["college"]


def test_register_duplicate_email(api_base_url, registered_user):
    """Negative: Attempting to register an already registered email should return 400."""
    url = f"{api_base_url}/api/auth/register"
    duplicate_payload = {
        "name": "Duplicate User",
        "email": registered_user["email"],
        "password": "AnotherPassword456!",
        "college": "Another University"
    }
    response = requests.post(url, json=duplicate_payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is False
    assert "User already exists" in body.get("message", "")


def test_login_invalid_password(api_base_url, registered_user):
    """Negative: Logging in with wrong password should return 400 Invalid Password."""
    url = f"{api_base_url}/api/auth/login"
    payload = {
        "email": registered_user["email"],
        "password": "WrongPassword999!"
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is False
    assert "Invalid Password" in body.get("message", "")


def test_login_nonexistent_user(api_base_url):
    """Negative: Logging in with non-existent email should return 400 User not found."""
    url = f"{api_base_url}/api/auth/login"
    non_existent_email = f"ghost_{uuid.uuid4().hex[:8]}@unregistered-campus.edu"
    payload = {
        "email": non_existent_email,
        "password": "AnyPassword123!"
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is False
    assert "User not found" in body.get("message", "")


def test_register_missing_required_fields(api_base_url):
    """Negative: Registering without email and password should fail."""
    url = f"{api_base_url}/api/auth/register"
    payload = {
        "name": "No Email User",
        "college": "Test College"
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

    # Mongoose validation fails or bcrypt hashing fails without password -> status >= 400
    assert response.status_code in [400, 500]
    body = response.json()
    assert body.get("success") is False


def test_register_with_special_characters_and_unicode(api_base_url, generate_user_data):
    """Edge Case: Register user with special characters, unicode, and accents in name/college."""
    payload = generate_user_data({
        "name": "Dr. René François-O'Connor & Co. 🎉",
        "college": "École Polytechnique Fédérale — Zürich Campus #1"
    })
    url = f"{api_base_url}/api/auth/register"
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 201
    body = response.json()
    assert body.get("success") is True


def test_register_large_string_payload(api_base_url, generate_user_data):
    """Edge Case: Registration with large text fields."""
    long_college_name = "Department of Advanced Computational Sciences and Technology - " + ("A" * 200)
    payload = generate_user_data({
        "college": long_college_name
    })
    url = f"{api_base_url}/api/auth/register"
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 201
    assert response.json().get("success") is True
