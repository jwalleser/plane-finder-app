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
        for page in listings_page:
            page_counter += 1
            log.info(f"Reading entries, page {page_counter}")
            for entry in page.entries:
                aircraft_sale_entry = AircraftSaleEntry.from_listings_entry(entry)
                log.info(f"Saving aircraft entry {aircraft_sale_entry.id}")
                self.database.save(aircraft_sale_entry)
