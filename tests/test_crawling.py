import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import pytest
from planefinder import utils
from planefinder.crawler import ListingDetail, ListingsPage
from planefinder.data import PageGetter


def test_navigation_from_multiple_listing_page_to_detail_page():
    listings_page = ListingsPage(multiple_listing_page())
    first_listing = next(listings_page.entries)
    assert first_listing
    known_listing_id = "2403772"
    assert first_listing.id == known_listing_id
    known_seller_id = "46072"
    assert first_listing.seller == known_seller_id
    known_last_update = datetime.date(2022, 4, 1)
    assert first_listing.last_update == known_last_update
    known_detail_url_part = "/search?category_level1=Single+Engine+Piston&make=CESSNA&model=182T+SKYLANE&listing_id=2403772&s-type=aircraft"
    assert first_listing.detail_url == str(listings_page.url) + known_detail_url_part


def test_page_getter():
    getter = PageGetter()
    test_url = "https://www.google.com"
    html = getter.get(test_url)
    assert html.lower().startswith("<!doctype html>")


def test_aircraft_detail_parsing():
    detail = ListingDetail(test_detail_page())
    assert detail.make_model == "CESSNA 182Q SKYLANE"
    assert detail.registration == "N7574S"
    assert detail.ttaf == 3388
    assert detail.smoh == "271 SMOH"


def multiple_listing_page() -> Path:
    return _test_file("listings-page.html")


def test_detail_page() -> str:
    return _test_file("aircraft-detail.html")


def _test_file(name: str) -> str:
    this_dir = Path(__file__).parent
    return this_dir.joinpath(name)
