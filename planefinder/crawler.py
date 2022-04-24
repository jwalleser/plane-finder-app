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
    def listing_detail(self):
        return ListingDetail()

    @property
    def detail_url(self):
        return trade_a_plane.detail_page_url(self.listing_soup)


class ListingDetail:
    @property
    def listing_id(self):
        pass

    @property
    def seller_id(self):
        pass

    @property
    def last_update(self):
        pass

    @property
    def make_model(self):
        pass

    @property
    def price(self):
        pass

    @property
    def registration(self):
        pass

    @property
    def description(self):
        pass

    @property
    def ttaf(self):
        pass

    @property
    def engine_time(self):
        pass

    @property
    def smoh(self):
        pass
