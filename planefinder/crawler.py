from bs4 import BeautifulSoup
from planefinder import trade_a_plane
from planefinder import utils


class ListingsPage:
    def __init__(self, listing_page_url: str):
        self.url = listing_page_url
        self.page_soup = utils.read_html_into_soup(listing_page_url)

    @property
    def entries(self):
        for entry_soup in self.page_soup.find_all(trade_a_plane.is_listing_result):
            yield ListingEntry(self, entry_soup)


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
        absolute_url = str(self.listings_page.url) + trade_a_plane.detail_page_url(
            self.listing_soup
        )
        return absolute_url


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
        return trade_a_plane.description(self.description)

    @property
    def ttaf(self):
        return trade_a_plane.ttaf(self.page_soup)

    @property
    def engine_time(self):
        return trade_a_plane.engine_time(self.page_soup)

    @property
    def smoh(self):
        return trade_a_plane.smoh(self.page_soup)
