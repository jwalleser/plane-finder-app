"""
Functions specific to crawling the Trade-a-Plane website

Most functions accept a node from an HTML document and return the 
first matching data.
"""

import re
from datetime import datetime
from typing import List
from bs4 import Tag

def is_listing_result(tag: Tag):
    """
    True if the node is a result listing.
    
    Result listings are <div> tags with `class="result_listing"
    """
    if not tag.name == 'div':
        return False
    if not tag.has_attr('class'):
        return False
    classes = tag['class']
    return ('result_listing' in classes
     and 'result' in classes)

def listing_id(node: Tag):
    """
    Get listing id from a node.

    Parameters
    ----------
    node: Tag
        A `result_listing` node.
    """
    try:
        return node.attrs['data-listing_id']
    except KeyError:
        print('Available attributes are: {}'.format(node.attrs))
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
    return node.attrs['data-seller_id']

def last_update(node: Tag) -> datetime:
    """
    Get last update according to Trade-a-Plane

    Parameters
    ----------
    node: Tag
        A `result_listing` node
    """
    update_node = node.find(name='p', class_='last-update')
    pattern = r'\d{2}/\d{2}/\d{4}'
    search_result = re.search(pattern, update_node.text).group(0)
    date_fmt = '%m/%d/%Y'
    date_ = datetime.strptime(search_result, date_fmt)
    return date_
def make_model(node: Tag):
    """
    Get make and model from a node.

    Parameters
    ----------
    node: Tag
        A detail page expected to contain a <li class="makeModel> node
    Returns
    -------
    processed_model: str
        Make/Model text or 'Unknown' if not found. Example: Cessna 182 Q Skylane.
    """
    # Get model node, <li class="makeModel">
    model_node = node.find(name='li', class_='makeModel')
    model_text = model_node.text
    # Capture model text, everything after the last colon, stripped of spaces
    processed_model = _text_after_colon_and_strip(model_text)
    if processed_model == '':
        processed_model = 'Unknown'
    return processed_model

def price(node: Tag) -> float:
    """
    Get price from a node.
    """
    main_info = node.find(name='div', id='main_info')
    if  main_info is None:
        raise ValueError('Expected to find a node containing a <div id="main_info"> tag')
    price_text = main_info.find(name='span', itemprop='price').text
    if price_text is None:
        raise ValueError('Expected to find a <span itemprop="price"> tag')
    return float(price_text)

def registration(node: Tag) -> str:
    """
    Get registration (N-number) from a node.

    Parameters
    ----------
    node: Tag
        Tag from detail page. Expect info in <li class="reg-number">
    """
    reg_txt = node.find(name='li', class_='reg-number').text
    reg =_text_after_colon_and_strip(reg_txt)
    if reg == '':
        reg = 'Unknown'
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
    return node.find(id='detailed_desc').find(itemprop='description').text

def ttaf(node: Tag):
    """
    Get total time airframe from a node.
    """
    spec_list = _general_specs(node)
    for spec in spec_list:
        tokens = spec.split(':')
        if tokens[0].strip().lower() == 'total time':
            return float(tokens[1])
    return -1

def engine_time(node: Tag) -> str:
    """
    Get engine time and type, SMOH, TTSN, factory overhaul.
    """
    spec_list = _general_specs(node)
    for spec in spec_list:
        tokens = spec.split(':')
        if tokens[0].strip().lower() == 'engine 1 time':
            return tokens[1].strip()
    return ''
def _text_after_colon_and_strip(text: str):
    """
    Get the text after a colon and strip white spaces

    Intended to get data after a colon. Normalize to remove extra whitespaces.
    """
    multiple_whitespace = r'\s+'
    normalized =  re.sub(multiple_whitespace, ' ', text).strip()
    # Find the text after the colon and trim
    after_colon_pattern = r':(.*)$'
    target_match = re.search(after_colon_pattern, normalized)
    return target_match.group(1).strip()

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
    general_specs = node.find(id='general_specs')
    if general_specs is None:
        return []
    spec_paragraphs = general_specs.find_all(name='p')
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