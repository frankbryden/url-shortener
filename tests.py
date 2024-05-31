from main import app
import pytest

TEST_URL = "https://www.stoik.com/en-us"

@pytest.fixture
def test_client():
    return app.test_client()

def extract_slug_from_url(url):
    return url.split("/")[-1]

def test_url_shorten(test_client):
    response = test_client.get(f"/shorten?url={TEST_URL}")
    slug = extract_slug_from_url(response.text)
    expanded = test_client.get(f"/{slug}")

    assert TEST_URL == expanded.headers["Location"]

def test_url_shorten_not_expired(test_client):
    response = test_client.get(f"/shorten?url={TEST_URL}&expiry=202505311000")
    slug = extract_slug_from_url(response.text)
    expanded = test_client.get(f"{slug}")

    assert TEST_URL == expanded.headers["Location"]

def test_url_shorten_expired(test_client):
    response = test_client.get(f"/shorten?url={TEST_URL}&expiry=202205311000")
    slug = response.text
    expanded = test_client.get(f"/{slug}")

    assert expanded.status_code == 404
