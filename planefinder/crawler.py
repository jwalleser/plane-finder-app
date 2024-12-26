"""
This module contains the Crawler class that is responsible for crawling a
Trade-a-Plane and saving the data to a database.
"""

import attr
from planefinder import trade_a_plane as tap
from planefinder import logging
from planefinder.data import AircraftSaleEntry, Database

log = logging.get_logger(__name__)


@attr.s
class Crawler:
    """
    Crawls a website collecting pages.

    1. Select an entry website.
    2. Add a filter to filter nodes.
    3. Add link following rules.
    """

    entry: str = attr.ib(default="")
    database: Database = attr.ib(default=None)

    def set_entry(self, url):
        """
        Set an entry point for the crawler.
        """
        self.entry = url

    def crawl(self):
        log.info(f"Crawling, starting from {self.entry}")
        listings_page = tap.ListingsPage(self.entry)
        page_counter = 0
        while True:
            page_counter += 1
            log.info(f"Reading entries, page {page_counter}")
            for entry in listings_page.entries:
                aircraft_sale_entry = AircraftSaleEntry.from_listings_entry(entry)
                log.info(f"Saving aircraft entry {aircraft_sale_entry.id}")
                self.database.save(aircraft_sale_entry)
            try:
                listings_page = next(listings_page)
            except StopIteration:
                break


def crawl_trade_a_plane():
    """
    Crawl Trade-a-Plane for Cessna 182 aircraft.

    Save data to the 'planefinder' database.
    """
    cessna_182_trade_a_plane = "https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make=CESSNA&model_group=CESSNA+182+SERIES&s-type=aircraft"
    database = Database.mongodb("planefinder")
    crawler = Crawler(cessna_182_trade_a_plane, database)
    crawler.crawl()


if __name__ == "__main__":
    log.setLevel(logging.INFO)
    log.info("Starting Trade-a-Plane crawler")
    crawl_trade_a_plane()
