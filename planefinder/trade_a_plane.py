"""
Functions specific to crawling the Trade-a-Plane website

Most functions accept a node from an HTML document and return the 
first matching data.
"""

import re
from datetime import datetime
from bs4 import Tag


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
        A result_listing node.
    """
    return node.attrs["data-listing_id"]


def seller_id(node):
    """
    Get seller id from a node.
    """
    return node.attrs["data-seller_id"]


def last_update(node: Tag) -> datetime:
    """
    Get last update according to Trade-a-Plane
    """
    update_node = node.find(name="p", class_="last-update")
    pattern = r"\d{2}/\d{2}/\d{4}"
    search_result = re.search(pattern, update_node.text).group(0)
    date_ = datetime.strptime(search_result, date_fmt)
    return date_


def make_model(node: Tag):
    """
    Get make and model from a node.

    Parameters
    ----------
    node: Tag
        A detail page
        <div id='main_info'>
    """


def price(node):
    """
    Get price from a node.
    """
    main_info = node.find(name="div", id="main_info")
    if main_info is None:
        raise ValueError(
            'Expected to find a node containing a <div id="main_info"> tag'
        )
    price_text = main_info.find(name="span", itemprop="price").text
    if price_text is None:
        raise ValueError('Expected to find a <span itemprop="price"> tag')
    return float(price_text)


def registration(node):
    """
    Get registration (N-number) from a node.
    """


def description(node):
    """
    Get seller's description from a node.
    """


def ttaf(node):
    """
    Get total time airframe from a node.
    """


def smoh(node):
    """
    Get time since major overhaul from a node.
    """
