from http.client import HTTP_PORT
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import threading
import pytest
from planefinder import logging

from planefinder.crawler import ListingDetail, ListingEntry, ListingsPage

HTTP_PORT = 8000


@pytest.fixture(scope="session", autouse=True)
def http_server():
    server_address = ("localhost", HTTP_PORT)
    handler_class = TestHTTPRequestHandler
    httpd = HTTPServer(server_address, handler_class)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    log = logging.get_logger(__name__)
    log.info("started test server")
    yield
    log.info("shutting down test server")
    httpd.shutdown()


class TestHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(
            request, client_address, server, directory=Path(__file__).parent
        )


@pytest.fixture
def listing_entry(listings_page: ListingsPage) -> ListingEntry:
    return next(listings_page.entries)


@pytest.fixture
def listings_page(multiple_listing_page) -> ListingsPage:
    return ListingsPage(multiple_listing_page)


@pytest.fixture
def listing_detail(test_detail_uri) -> ListingDetail:
    return ListingDetail(test_detail_uri)


@pytest.fixture
def multiple_listing_page() -> str:
    return f"http://localhost:{HTTP_PORT}/listings-page.html"


@pytest.fixture
def test_detail_uri() -> str:
    return f"http://localhost:{HTTP_PORT}/aircraft-detail.html"


def _test_file(name: str) -> Path:
    this_dir = Path(__file__).parent
    return this_dir.joinpath(name)
