from datetime import datetime
from urllib.parse import urlparse, urljoin
from planefinder.trade_a_plane import ListingsPage, ListingEntry, ListingDetail
from planefinder.crawler import Crawler
from planefinder.data import Database, PageGetter


def test_navigation_from_multiple_listing_page_to_detail_page(
    listings_page: ListingsPage,
):
    first_listing = next(listings_page.entries)
    assert first_listing
    known_listing_id = "2403772"
    assert first_listing.id == known_listing_id
    known_seller_id = "46072"
    assert first_listing.seller == known_seller_id
    known_last_update = datetime(2022, 4, 1)
    assert first_listing.last_update == known_last_update
    known_detail_url_part = "aircraft-detail.html"
    assert first_listing.detail_url == urljoin(listings_page.url, known_detail_url_part)


def test_listing_page_detail_url(listing_entry: ListingEntry):
    assert listing_entry.detail_url == urljoin(
        listing_entry.listings_page.url, "aircraft-detail.html"
    )


def test_navigation_to_next_listing_page(listings_page: ListingsPage):
    next_listings_page = next(listings_page)
    assert next_listings_page.url == listings_page.url


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


def test_aircraft_detail_parsing(listing_detail: ListingDetail):
    assert listing_detail.make_model == "CESSNA 182Q SKYLANE"
    assert listing_detail.registration == "N7574S"
    assert listing_detail.ttaf == 3388
    assert listing_detail.smoh == "271 SMOH"


def test_crawl_webpage_from_entry_url():
    cessna_182_trade_a_plane = "https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make=CESSNA&model_group=CESSNA+182+SERIES&s-type=aircraft"
    test_database = Database.mongodb("planefinder_test_crawl")
    crawler = Crawler(cessna_182_trade_a_plane, test_database)
    crawler.crawl()
