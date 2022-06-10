from pathlib import Path
from typing import Iterable
import pandas as pd
from flask import Flask
from flask.ctx import AppContext
import pytest
from planefinder.data import AircraftSaleEntry
from planefinder.webapp import create_app
from planefinder.webapp import db

@pytest.fixture
def app() -> Iterable[Flask]:
    app = create_app("testing")
    yield app

def test_home_page_has_table_of_planes(app):
    client = app.test_client()
    response = client.get("/")
    assert "basic-listing-table" in response.get_data(as_text=True)


def test_get_listings_from_database_in_app(app: Flask):
    with app.app_context():
        listings = db.get_db().get_all_listings()

def test_test_aircraft_sales_entries(aircraft_sales_entries):
    assert len(aircraft_sales_entries) == 10
    for entry in aircraft_sales_entries:
        test_entry: AircraftSaleEntry = entry
        break
    assert test_entry.seller_id == 100
    assert test_entry.make_model == "C182"
    assert test_entry.price == 150000
    assert test_entry.registration == "N12345"

@pytest.fixture
def aircraft_sales_entries() -> Iterable[AircraftSaleEntry]:
    FILE: Path = Path(__file__).parent.joinpath("test-aircraft-sales-entries.xlsx")
    df: pd.DataFrame = pd.read_excel(FILE)
    return AircraftSaleEntry.from_dataframe(df) 
