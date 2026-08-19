import pytest
import requests

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_backend_root_health(api_base_url):
    """Positive: Root endpoint '/' returns health indicator."""
    url = f"{api_base_url}/"
    response = requests.get(url)

    assert response.status_code == 200
    assert "CampusConnect Backend Running" in response.text


def test_auth_test_endpoint(api_base_url):
    """Positive: /api/auth/test returns test indicator string."""
    url = f"{api_base_url}/api/auth/test"
    response = requests.get(url)

    assert response.status_code == 200
    assert "Auth Route Working" in response.text


def test_nonexistent_endpoint_returns_404(api_base_url):
    """Negative: Requesting a route that does not exist returns 404."""
    url = f"{api_base_url}/api/nonexistent_resource_endpoint_xyz"
    response = requests.get(url)

    assert response.status_code == 404


def test_invalid_http_method_on_login(api_base_url):
    """Negative: Sending GET to /api/auth/login should return 404."""
    url = f"{api_base_url}/api/auth/login"
    response = requests.get(url)

    assert response.status_code in [404, 405]


def test_malformed_json_body(api_base_url):
    """Negative: Sending malformed raw string instead of valid JSON returns 400."""
    url = f"{api_base_url}/api/auth/login"
    raw_bad_data = "{ email: 'missing_quotes', invalid_json, "
    response = requests.post(url, data=raw_bad_data, headers={"Content-Type": "application/json"})

    assert response.status_code in [400, 500]
