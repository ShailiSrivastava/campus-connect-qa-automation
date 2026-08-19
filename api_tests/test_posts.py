import uuid
import pytest
import requests

pytestmark = [pytest.mark.api]


@pytest.mark.smoke
def test_create_post_success(api_base_url, auth_headers):
    """Positive: Create a new post with title and content."""
    unique_tag = uuid.uuid4().hex[:6]
    payload = {
        "title": f"Automated QA Test Post #{unique_tag}",
        "content": f"Exploring continuous integration and automated test suites on Campus Connect ({unique_tag})."
    }
    url = f"{api_base_url}/api/posts/create"
    response = requests.post(url, json=payload, headers=auth_headers)

    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is True
    assert "post" in body
    post = body["post"]
    assert post["title"] == payload["title"]
    assert post["content"] == payload["content"]
    assert "_id" in post
    assert "author" in post


@pytest.mark.smoke
def test_get_posts_public(api_base_url, created_post):
    """Positive: Retrieve all posts publicly without authorization header."""
    url = f"{api_base_url}/api/posts"
    response = requests.get(url)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    body = response.json()
    assert body.get("success") is True
    assert "posts" in body
    assert isinstance(body["posts"], list)

    # Verify that the created fixture post exists in the returned list
    post_ids = [p.get("_id") for p in body["posts"]]
    assert created_post.get("_id") in post_ids


def test_create_post_unauthorized(api_base_url):
    """Negative: Creating a post without token should return 401."""
    url = f"{api_base_url}/api/posts/create"
    payload = {
        "title": "Unauthorized Post",
        "content": "Should not be created."
    }
    response = requests.post(url, json=payload)

    assert response.status_code == 401
    body = response.json()
    assert body.get("success") is False
    assert "No token provided" in body.get("message", "")


def test_create_post_missing_fields(api_base_url, auth_headers):
    """Negative: Creating a post with missing title/content should return error."""
    url = f"{api_base_url}/api/posts/create"
    payload = {
        "title": "Post With No Content"
    }
    response = requests.post(url, json=payload, headers=auth_headers)

    assert response.status_code in [400, 500]
    body = response.json()
    assert body.get("success") is False


def test_like_post_endpoint(api_base_url, auth_headers, created_post):
    """Positive: Like a post by its ID."""
    post_id = created_post["_id"]
    url = f"{api_base_url}/api/posts/like/{post_id}"
    response = requests.post(url, headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    assert "Like route working" in body.get("message", "")


def test_like_post_unauthorized(api_base_url, created_post):
    """Negative: Like post without token should return 401."""
    post_id = created_post["_id"]
    url = f"{api_base_url}/api/posts/like/{post_id}"
    response = requests.post(url)

    assert response.status_code == 401


def test_comment_post_endpoint(api_base_url, auth_headers, created_post):
    """Positive: Add comment to a post by ID."""
    post_id = created_post["_id"]
    url = f"{api_base_url}/api/posts/comment/{post_id}"
    payload = {"text": "Great campus update! Kudos to the team."}
    response = requests.post(url, json=payload, headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    assert "Comment route working" in body.get("message", "")


def test_delete_post_endpoint(api_base_url, auth_headers, created_post):
    """Positive: Delete post endpoint test."""
    post_id = created_post["_id"]
    url = f"{api_base_url}/api/posts/{post_id}"
    response = requests.delete(url, headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is True
    assert "Delete route working" in body.get("message", "")


def test_create_post_large_payload_and_unicode(api_base_url, auth_headers):
    """Edge Case: Create a post with long text and markdown/code syntax."""
    url = f"{api_base_url}/api/posts/create"
    large_content = (
        "## Release Notes v2.4.0\n\n"
        "We are excited to announce new campus features:\n"
        "- Enhanced JWT token security 🔒\n"
        "- Fast API endpoints ⚡\n"
        "- Beautiful UI gradients 🎨\n\n"
        "```javascript\nconsole.log('CampusConnect Ready!');\n```\n"
        + ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 30)
    )
    payload = {
        "title": "🎉 Big Campus Update — Engineering Hackathon 2026",
        "content": large_content
    }
    response = requests.post(url, json=payload, headers=auth_headers)

    assert response.status_code == 201
    body = response.json()
    assert body.get("success") is True
    assert body["post"]["title"] == payload["title"]
