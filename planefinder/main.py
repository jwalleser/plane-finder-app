"""
Main an only current module.

This contains all classes, functions, etc.  in my plane-finder-app
"""
import attr
from datetime import datetime
@attr.s
class AircraftSaleEntry:
    """
    A data class for aircraft sale information
    
    This is the main type of obejct that I wish to collect. I want to index
    aircraft sales entries. I want to record what is for sale, when, and for
    how much.
    """
    url: str = attr.ib()
    make_model: str = attr.ib()
    price: float = attr.ib()
    registration: str = attr.ib()
    description: str = attr.ib()
    search_date: datetime = attr.ib()
    ttaf: float = attr.ib()
    smoh: float = attr.ib()
