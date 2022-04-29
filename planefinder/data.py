from datetime import datetime
import attr
import requests
import pymongo
from pymongo.server_api import ServerApi

@attr.s
class AircraftSaleEntry:
    """
    A data class for aircraft sale information
    
    This is the main type of obejct that I wish to collect. I want to index
    aircraft sales entries. I want to record what is for sale, when, and for
    how much.
    """

    id: int = attr.ib()
    url: str = attr.ib()
    seller_id: int = attr.ib()
    make_model: str = attr.ib()
    price: float = attr.ib()
    registration: str = attr.ib()
    description: str = attr.ib()
    search_date: datetime = attr.ib()
    ttaf: float = attr.ib()
    smoh: float = attr.ib()


class PageGetter:
    def get(self, url):
        return requests.get(url).text


class MongoAtlas:
    password = "NHMe4roVZcNRmsaQ"
    db_name = "planefinder"
    db_user = "plane-finder-app"
class Database:
    def __init__(self):
        self.conn = None
    @classmethod
    def mongodb(cls):
        db_user = MongoAtlas.db_name
        password = MongoAtlas.password
        db_name = MongoAtlas.db_name
        client = pymongo.MongoClient("mongodb+srv://{db_user}:{password}@flydb.c4yh8.mongodb.net/{db_name}?retryWrites=true&w=majority", server_api=ServerApi('1'))
        db = client[db_name]
        instance = cls()
        instance.conn = client
        return instance
