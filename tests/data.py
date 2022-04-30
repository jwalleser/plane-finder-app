from pathlib import Path

def multiple_listing_page() -> str:
    return _test_file("listings-page.html").as_uri()


def test_detail_page() -> str:
    return _test_file("aircraft-detail.html").as_uri()


def _test_file(name: str) -> Path:
    this_dir = Path(__file__).parent
    return this_dir.joinpath(name)
