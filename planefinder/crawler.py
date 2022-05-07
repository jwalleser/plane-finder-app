from pathlib import Path
import attr
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from planefinder import trade_a_plane
from planefinder import utils


@attr.s
class Crawler:
    """
    Crawls a website collecting pages.

    1. Select an entry website.
    2. Add a filter to filter nodes.
    3. Add link following rules.
    """

    entry: str = attr.ib(default="")

    def set_entry(self, url):
        """
        Set an entry point for the crawler.
        """
        self.entry = url

    def add_filter(self, filter):
        """
        Add a filter on the entry page for HTML to collect.
        """

    def read_page(self, url) -> BeautifulSoup:
        """
        Read a web page and do something.
        """
        response = requests.get(url)
        soup = BeautifulSoup(response)
        return soup

    def save_page(self, page: BeautifulSoup):
        """
        Save a page for later retrieval
        
        I do not know what I mean by save. Save the raw HTML? Save the 
        BeautifulSoup object? What do I want to save and why? Such a save
        operation implies its reciprocal, `load_page`.
        
        Consider adding some additional metadata such as date crawled to this
        saved object.
        """

    def run(self):
        """
        Crawl a website.

        DEVELOPMENT
        Currently limited to crawling only the first entry.
        """
        if self.entry == "":
            raise Exception("`entry` must be set before running.")
        soup = self.read_page(self.entry)
        self.save_page(soup)  # Save the initial entry page.
        listing_entries = soup.find_all(trade_a_plane.is_listing_result)
        # Iterate through entries
        for init_listing in listing_entries:
            # Save entry HTML
            # Collect some information from the initial entry

            # HTTP get detail page
            # Save detail page
            # Collect information from detail pages
            # Next entry
            raise NotImplementedError("Need to implement this block.")

class ListingsPage:
    def __init__(self, listing_page_url: str):
        self.url = listing_page_url
        self.page_soup = utils.read_html_into_soup(listing_page_url)

    @property
    def entries(self):
        for entry_soup in self.page_soup.find_all(trade_a_plane.is_listing_result):
            yield ListingEntry(self, entry_soup)

    def __next__(self):
        next_url_path = trade_a_plane.next_page_url(self.page_soup)
        if next_url_path == "":
            raise StopIteration
        parts = urlparse(self.url)
        if parts.scheme == "file":
            next_absolute_url = (
                Path(parts.path[1:]).parent.joinpath(next_url_path).as_uri()
            )
        elif parts.scheme.startswith("http"):
            next_absolute_url = urljoin(self.url, next_url_path)
        return ListingsPage(next_absolute_url)


class ListingEntry:
    def __init__(self, listings_page: ListingsPage, listing_soup: BeautifulSoup):
        self.listings_page = listings_page
        self.listing_soup = listing_soup

    @property
    def id(self):
        return trade_a_plane.listing_id(self.listing_soup)

    @property
    def seller(self):
        return trade_a_plane.seller_id(self.listing_soup)

    @property
    def last_update(self):
        return trade_a_plane.last_update(self.listing_soup)

    @property
    def detail(self):
        return ListingDetail(self.detail_url)

    @property
    def detail_url(self):
        detail_path = trade_a_plane.detail_page_url(self.listing_soup)
        return urljoin(self.listings_page.url, detail_path)


class ListingDetail:
    def __init__(self, url):
        self.url = url
        self.page_soup = utils.read_html_into_soup(self.url)

    @property
    def listing_id(self, url):
        return trade_a_plane.listing_id(self.page_soup)

    @property
    def seller_id(self):
        return trade_a_plane.seller_id(self.page_soup)

    @property
    def last_update(self):
        return trade_a_plane.last_update(self.page_soup)

    @property
    def make_model(self):
        return trade_a_plane.make_model(self.page_soup)

    @property
    def price(self):
        return trade_a_plane.price(self.page_soup)

    @property
    def registration(self):
        return trade_a_plane.registration(self.page_soup)

    @property
    def description(self):
        return trade_a_plane.description(self.page_soup)

    @property
    def ttaf(self):
        return trade_a_plane.ttaf(self.page_soup)

    @property
    def engine_time(self):
        return trade_a_plane.engine_time(self.page_soup)

    @property
    def smoh(self):
        return trade_a_plane.smoh(self.page_soup)
