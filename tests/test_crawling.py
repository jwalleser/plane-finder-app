import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import pytest
from planefinder import utils
from planefinder.crawler import ListingsPage


def test_navigation_from_multiple_listing_page_to_detail_page():
    listings_page = ListingsPage(multiple_listing_page())
    for aircraft_listing in listings_page.entries:
        detail = aircraft_listing.listing_detail
        assert detail
    first_listing = next(listings_page.entries)
    assert first_listing
    known_listing_id = "2403772"
    assert first_listing.id == known_listing_id
    known_seller_id = "46072"
    assert first_listing.seller == known_seller_id
    known_last_update = datetime.date(2022, 4, 1)
    assert first_listing.last_update == known_last_update
    known_detail_url_part = "/search?category_level1=Single+Engine+Piston&make=CESSNA&model=182T+SKYLANE&listing_id=2403772&s-type=aircraft"
    assert first_listing.detail_url == known_detail_url_part


def multiple_listing_page() -> BeautifulSoup:
    this_dir = Path(__file__).parent
    return this_dir.joinpath("listings-page.html")
