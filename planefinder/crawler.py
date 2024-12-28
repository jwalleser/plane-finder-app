"""
This module contains the Crawler class that is responsible for crawling a
Trade-a-Plane and saving the data to a database.
"""

import logging
import attr
from planefinder import trade_a_plane as tap
import planefinder.logging
from planefinder.data import AircraftSaleEntry, Database
from tqdm import tqdm

log = planefinder.logging.get_logger(__name__)


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

    def crawl(self, max_iterations=None):
        log.info(f"Crawling, starting from {self.entry}")
        # Expecting a Trade-a-Plane URL for listings
        # Collect all listing URLs first (breadth-first)
        all_entries = []
        listings_page = tap.ListingsPage(self.entry)
        with tqdm(desc="Paging through listings") as progress_bar:
            while True:
                page_entries = list(listings_page.entries)
                all_entries.extend(page_entries)
                progress_bar.update(len(page_entries))

                try:
                    listings_page = next(listings_page)
                except StopIteration:
                    break

        # Initialize progress bar
        total_listings = len(all_entries)
        progress_bar = tqdm(total=total_listings, desc="Crawling listings")
        iteration_count = 0
        # Process each listing URL (depth-first)
        for entry in all_entries:

            aircraft_sale_entry = AircraftSaleEntry.from_listings_entry(entry)
            log.info(f"Saving aircraft entry {aircraft_sale_entry.id}")
            self.database.save(aircraft_sale_entry)
            iteration_count += 1
            if max_iterations and iteration_count >= max_iterations:
                log.info(f"Reached max iterations: {max_iterations}")
                break
            progress_bar.update(1)
        progress_bar.close()


def crawl_trade_a_plane(max_iterations=None):
    """
    Crawl Trade-a-Plane for Cessna 182 aircraft.

    Save data to the 'planefinder' database.
    """
    cessna_182_trade_a_plane = "https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make=CESSNA&model_group=CESSNA+182+SERIES&s-type=aircraft"
    database = Database.mongodb("planefinder")
    crawler = Crawler(cessna_182_trade_a_plane, database)
    crawler.crawl(max_iterations=max_iterations)


if __name__ == "__main__":
    log.setLevel(logging.INFO)
    log.info("Starting Trade-a-Plane crawler")
    crawl_trade_a_plane(max_iterations=None)
