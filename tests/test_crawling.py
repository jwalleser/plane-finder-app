from pathlib import Path
from bs4 import BeautifulSoup
import pytest
from tests import utils
from planefinder.crawler import ListingsPage

def test_navigation_from_multiple_listing_page_to_detail_page():
    listings_page = ListingsPage(multiple_listing_page())
    for aircraft_listing in listings_page.entries:
        detail = aircraft_listing.listing_detail
        assert detail

def multiple_listing_page() -> BeautifulSoup:
    this_dir = Path(__file__).parent
    listings_page = this_dir.joinpath('listings-page.html')
    return utils.read_html_into_soup(listings_page)
