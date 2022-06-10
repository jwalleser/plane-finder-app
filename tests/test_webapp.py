from flask import Flask
from flask.ctx import AppContext
import pytest
from planefinder.webapp import create_app
from planefinder.webapp import db

@pytest.fixture
def app() -> Flask:
    app = create_app("testing")
    yield app

def test_home_page_has_table_of_planes(app):
    client = app.test_client()
    response = client.get("/")
    assert "basic-listing-table" in response.get_data(as_text=True)


def test_get_listings_from_database_in_app(app: Flask):
    with app.app_context():
        listings = db.get_db().get_all_listings()
