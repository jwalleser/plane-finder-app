"""
Functions specific to crawling the Trade-a-Plane website

Most functions accept a node from an HTML document and return the 
first matching data.
"""

def is_listing_result(tag):
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

def listing_id(node):
    """
    Get listing id from a node.
    """

def seller_id(node):
    """
    Get seller id from a node.
    """

def make_model(node):
    """
    Get make and model from a node.
    """

def price(node):
    """
    Get price from a node.
    """

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