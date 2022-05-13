"""
Functions specific to crawling the Trade-a-Plane website

Most functions accept a node from an HTML document and return the 
first matching data.
"""

from pathlib import Path
import re
from datetime import datetime
from typing import List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag


class TAPPageGetter:
    page_getter = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        from planefinder.data import PageGetter

        if cls.page_getter is None:
            cls.page_getter = PageGetter()
        return cls.page_getter


class ListingsPage:
    def __init__(self, listing_page_url: str):
        self._page_getter = TAPPageGetter.get_instance()
        self.url = listing_page_url
        self.page_soup = self._page_getter.get_soup(listing_page_url)

    @property
    def entries(self):
        for entry_soup in self.page_soup.find_all(is_listing_result):
            yield ListingEntry(self, entry_soup)

    def __next__(self):
        next_url_path = next_page_url(self.page_soup)
        if next_url_path == "":
            raise StopIteration
        parts = urlparse(self.url)
        if parts.scheme == "file":
            next_absolute_url = (
                Path(parts.path[1:]).parent.joinpath(next_url_path).as_uri()
            )
        elif parts.scheme.startswith("http"):
            next_absolute_url = urljoin(self.url, next_url_path)
        self.url = next_absolute_url
        self.page_soup = self._page_getter.get_soup(self.url)
        return self


class ListingEntry:
    def __init__(self, listings_page: ListingsPage, listing_soup: BeautifulSoup):
        self.listings_page = listings_page
        self.listing_soup = listing_soup

    @property
    def id(self):
        return listing_id(self.listing_soup)

    @property
    def seller(self):
        return seller_id(self.listing_soup)

    @property
    def last_update(self):
        return last_update(self.listing_soup)

    @property
    def detail(self):
        return ListingDetail(self.detail_url)

    @property
    def detail_url(self):
        detail_path = detail_page_url(self.listing_soup)
        return urljoin(self.listings_page.url, detail_path)


class ListingDetail:
    def __init__(self, url):
        page_getter = TAPPageGetter.get_instance()
        self.url = url
        self.page_soup = page_getter.get_soup(self.url)

    @property
    def listing_id(self, url):
        return listing_id(self.page_soup)

    @property
    def seller_id(self):
        return seller_id(self.page_soup)

    @property
    def last_update(self):
        return last_update(self.page_soup)

    @property
    def make_model(self):
        return make_model(self.page_soup)

    @property
    def price(self):
        return price(self.page_soup)

    @property
    def registration(self):
        return registration(self.page_soup)

    @property
    def description(self):
        return description(self.page_soup)

    @property
    def ttaf(self):
        return ttaf(self.page_soup)

    @property
    def engine_time(self):
        return engine_time(self.page_soup)

    @property
    def smoh(self):
        return smoh(self.page_soup)


def next_page_url(node):
    link_tag_with_next_page = node.find(name="link", rel="next")
    if link_tag_with_next_page:
        return link_tag_with_next_page.attrs["href"]
    else:
        return ""


def is_listing_result(tag: Tag):
    """
    True if the node is a result listing.
    
    Result listings are <div> tags with `class="result_listing"
    """
    if not tag.name == "div":
        return False
    if not tag.has_attr("class"):
        return False
    classes = tag["class"]
    return "result_listing" in classes and "result" in classes


def listing_id(node: Tag):
    """
    Get listing id from a node.

    Parameters
    ----------
    node: Tag
        A `result_listing` node.
    """
    try:
        return node.attrs["data-listing_id"]
    except KeyError:
        print("Available attributes are: {}".format(node.attrs))
        raise


def seller_id(node: Tag) -> str:
    """
    Get seller id from a node.

    Parameters
    ----------
    node: Tag
        A `result_listing` node
    Returns
    -------
    seller_id: str
        The seller ID, as a string
    """
    return node.attrs["data-seller_id"]


def last_update(node: Tag) -> datetime:
    """
    Get last update according to Trade-a-Plane

    Parameters
    ----------
    node: Tag
        A `result_listing` node
    """
    try:
        update_node = node.find(name="p", class_="last-update")
        pattern = r"\d{2}/\d{2}/\d{4}"
        search_result = re.search(pattern, update_node.text).group(0)
        date_fmt = "%m/%d/%Y"
        date_ = datetime.strptime(search_result, date_fmt)
        return date_
    except AttributeError:
        return datetime.now()


def detail_page_url(node: Tag) -> str:
    description_node = node.find(name="p", class_="description")
    return description_node.find(name="a").attrs["href"]


def make_model(node: Tag):
    """
    Get make and model from a node.

    Parameters
    ----------
    node: Tag
        A detail page
        <div id='main_info'>

        A detail page expected to contain a <li class="makeModel> node
    Returns
    -------
    processed_model: str
        Make/Model text or 'Unknown' if not found. Example: Cessna 182 Q Skylane.
    """
    model_node = node.find(name="li", class_="makeModel")
    model_text = model_node.text
    # Capture model text, everything after the last colon, stripped of spaces
    processed_model = _text_after_colon_and_strip(model_text)
    if processed_model == "":
        processed_model = "Unknown"
    return processed_model


def price(node: Tag) -> float:
    """
    Get price from a node.
    """
    main_info = node.find(name="div", id="main_info")
    if main_info is None:
        raise ValueError(
            'Expected to find a node containing a <div id="main_info"> tag'
        )
    try:
        price_text = main_info.find(name="span", itemprop="price").text
    except AttributeError:
        return 0
    return float(price_text)


def registration(node: Tag) -> str:
    """
    Get registration (N-number) from a node.

    Parameters
    ----------
    node: Tag
        Tag from detail page. Expect info in <li class="reg-number">
    """
    reg_txt = node.find(name="li", class_="reg-number").text
    reg = _text_after_colon_and_strip(reg_txt)
    if reg == "":
        reg = "Unknown"
    return reg


def description(node: Tag) -> str:
    """
    Get seller's description from a node.

    Parameters
    ----------
    node: Tag
        Detail page containing an element with id="detailed_desc" which
        contains another tag with itemprop="description"
    
    Returns
    -------
    text: str
        Text as provided by seller
    """
    return node.find(id="detailed_desc").find(itemprop="description").text


def ttaf(node: Tag):
    """
    Get total time airframe from a node.
    """
    spec_list = _general_specs(node)
    for spec in spec_list:
        tokens = spec.split(":")
        if tokens[0].strip().lower() == "total time":
            return float(tokens[1])
    return -1


def engine_time(node: Tag) -> str:
    """
    Get engine time and type, SMOH, TTSN, factory overhaul.
    """
    spec_list = _general_specs(node)
    for spec in spec_list:
        tokens = spec.split(":")
        if tokens[0].strip().lower() == "engine 1 time":
            return tokens[1].strip()
    return ""


def _text_after_colon_and_strip(text: str):
    """
    Get the text after a colon and strip white spaces

    Intended to get data after a colon. Normalize to remove extra whitespaces.
    """
    multiple_whitespace = r"\s+"
    normalized = re.sub(multiple_whitespace, " ", text).strip()
    # Find the text after the colon and trim
    after_colon_pattern = r":(.*)$"
    target_match = re.search(after_colon_pattern, normalized)
    return target_match.group(1).strip()


def smoh(node):
    """
    Get time since major overhaul from a node.
    """
    return engine_time(node)


def _general_specs(node: Tag) -> List[str]:
    """
    Parameters
    ----------
    node: Tag
        Detail page containing <div id='general_specs'>
    
    Returns
    -------
    general_specs: List[Tag]
        A list of general spec field text
        Example: [Total Time:3388,
                  Engine 1 Time:271 SMOH,
                  Prop 1 Time:410 SMOH,
                  Useful Load:1100,
                  Condition:Used,
                  Year Painted:1994,
                  Interior Year:1992,
                  Flight Rules:IFR,
                  # of Seats:4]
    """
    general_specs = node.find(id="general_specs")
    if general_specs is None:
        return []
    spec_paragraphs = general_specs.find_all(name="p")
    if spec_paragraphs is None:
        return []
    return [general_spec_node.text for general_spec_node in spec_paragraphs]


def _spec_from_colon_separated_text_list(spec_name: str):
    """
    Get a specification value from a list of colon separated values in

    `_general_specs(...)` returns a list of strings of with the format
    `Spec Name: Spec Value`.
    TODO: Implement and use this. Refactor `ttaf(...)`
    """
