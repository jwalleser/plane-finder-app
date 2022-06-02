import pytest
from planefinder.webapp import create_app

@pytest.fixture
def app():
    return create_app("testing")

@pytest.fixture
def app_context(app):
    return app.app_context()

def test_home_page_has_table_of_planes(app):
    client = app.test_client()
    response = client.get("/")
    assert "basic-listing-table" in response.get_data(as_text=True)
