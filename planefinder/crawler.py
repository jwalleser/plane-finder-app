from bs4 import BeautifulSoup
from planefinder import trade_a_plane


class ListingsPage:
    def __init__(self, page_soup: BeautifulSoup):
        self.page_soup = page_soup

    @property
    def entries(self):
        for entry_soup in self.page_soup.find_all(trade_a_plane.is_listing_result):
            yield ListingEntry(entry_soup)


class ListingEntry:
    def __init__(self, listing_soup: BeautifulSoup):
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
