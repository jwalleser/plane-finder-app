"""
Put application configuration here
"""
import attr
from datetime import datetime
import requests
from bs4 import BeautifulSoup, ResultSet
import trade_a_plane
from planefinder import logging

logging.setup_applevel_logger()