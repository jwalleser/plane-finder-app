from pathlib import Path
import pytest

from planefinder.crawler import ListingDetail, ListingsPage


@pytest.fixture
def listings_page(multiple_listing_page) -> ListingsPage:
    return ListingsPage(multiple_listing_page)


@pytest.fixture
def listing_detail(test_detail_uri) -> ListingDetail:
    return ListingDetail(test_detail_uri)


@pytest.fixture
def multiple_listing_page() -> str:
    return _test_file("listings-page.html").as_uri()


@pytest.fixture
def test_detail_uri() -> str:
    return _test_file("aircraft-detail.html").as_uri()


def _test_file(name: str) -> Path:
    this_dir = Path(__file__).parent
    return this_dir.joinpath(name)
