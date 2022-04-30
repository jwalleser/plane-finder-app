import datetime
from urllib.parse import urlparse
from planefinder.crawler import ListingDetail, ListingsPage
from planefinder.data import PageGetter
from tests.data import test_detail_page, multiple_listing_page


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


def test_navigation_to_next_listing_page():
    entry_listings_page = ListingsPage(multiple_listing_page())
    next_listings_page = next(entry_listings_page)
    assert next_listings_page.url == entry_listings_page.url


def test_url_parts():
    url = "https://www.trade-a-plane.com/search?make=CESSNA&model_group=CESSNA+182+SERIES&s-type=aircraft"
    parts = urlparse(url)
    assert parts.scheme == "https"
    assert parts.netloc == "www.trade-a-plane.com"
    assert parts.path == "/search"
    assert parts.query == "make=CESSNA&model_group=CESSNA+182+SERIES&s-type=aircraft"


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
