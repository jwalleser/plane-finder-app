"""
Main an only current module.

This contains all classes, functions, etc.  in my plane-finder-app
"""
import attr
from datetime import datetime
import requests
from bs4 import BeautifulSoup, ResultSet
import trade_a_plane


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


class PlaneListings:
    def __init__(self, listing_results: ResultSet):
        self.listing_results = listing_results
