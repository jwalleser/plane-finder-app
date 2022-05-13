from datetime import datetime, timedelta
import time
from urllib.parse import urlparse
import attr
from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from pymongo.results import InsertOneResult
from cachetools import cached, TTLCache

from planefinder.trade_a_plane import ListingEntry
from planefinder import logging

log = logging.get_logger(__name__)


@attr.s
class AircraftSaleEntry:
    """
    A data class for aircraft sale information
    
    This is the main type of obejct that I wish to collect. I want to index
    aircraft sales entries. I want to record what is for sale, when, and for
    how much.
    """

    _id: ObjectId = attr.ib(init=False)
    id: int = attr.ib()
    url: str = attr.ib()
    seller_id: int = attr.ib()
    make_model: str = attr.ib()
    price: float = attr.ib()
    registration: str = attr.ib()
    description: str = attr.ib()
    last_update: datetime = attr.ib()
    ttaf: float = attr.ib()
    smoh: float = attr.ib()

    @classmethod
    def from_listings_entry(cls, entry: ListingEntry):
        return cls(
            id=entry.id,
            url=entry.listings_page.url,
            seller_id=entry.seller,
            make_model=entry.detail.make_model,
            price=entry.detail.price,
            registration=entry.detail.registration,
            description=entry.detail.description,
            last_update=entry.last_update,
            ttaf=entry.detail.ttaf,
            smoh=entry.detail.smoh,
        )


class PageGetter:
    def __init__(self):
        self.last_request_from_host = {}
        self.min_request_interval_in_seconds = 2

    @cached(cache=TTLCache(100, ttl=86400))
    def get(self, url) -> str:
        log.info(f"Getting data from {url}")
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if hostname in self.last_request_from_host:
            time_elapsed_since_last_request = (
                datetime.now() - self.last_request_from_host[hostname]
            )
            if time_elapsed_since_last_request < timedelta(
                seconds=self.min_request_interval_in_seconds
            ):
                time.sleep(self.min_request_interval_in_seconds)
        self.last_request_from_host[hostname] = datetime.now()
        response = requests.get(url)
        if response.status_code == 429:
            log.warning(f"Too many requests too fast to {hostname}: {response.headers}")
            raise Exception("Could not get page data")
        return response.text

    def get_soup(self, html_file):
        html = self.get(html_file)
        soup = BeautifulSoup(html, features="html.parser")
        return soup


class MongoAtlas:
    password = "NHMe4roVZcNRmsaQ"
    db_name = "planefinder"
    db_user = "plane-finder-app"


class Database:
    def __init__(self):
        self.conn = None

    def save(self, object_):
        if isinstance(object_, AircraftSaleEntry):
            return self._save_aircraft_entry(object_)
        else:
            raise NotImplementedError(
                "I only know how to save AircraftSaleEntry objects"
            )

    def save_or_update(self, object_):
        if isinstance(object_, AircraftSaleEntry):
            obj_dict = object_.__dict__
            del obj_dict["_id"]
            return self.conn["AircraftSaleEntry"].update_one(
                {"id": object_.id}, {"$set": obj_dict}, upsert=True
            )
        else:
            raise NotImplementedError(
                "I only know how to save AircraftSaleEntry objects"
            )

    def find_by_id(self, id):
        document = self.conn["AircraftSaleEntry"].find_one({"id": id})
        entry = AircraftSaleEntry(
            id=document["id"],
            url=document["url"],
            seller_id=document["seller_id"],
            make_model=document["make_model"],
            price=document["price"],
            registration=document["registration"],
            description=document["description"],
            last_update=document["last_update"],
            ttaf=document["ttaf"],
            smoh=document["smoh"],
        )
        entry._id = document["_id"]
        return entry

    def delete(self, object_):
        if isinstance(object_, ObjectId):
            self.conn["AircraftSaleEntry"].delete_one({"_id": object_})
        elif isinstance(object_, AircraftSaleEntry):
            self.conn["AircraftSaleEntry"].delete_one({"id": object_.id})
        else:
            raise NotImplementedError("Not yet implemented")

    def _save_aircraft_entry(self, entry: AircraftSaleEntry) -> InsertOneResult:
        return self.conn["AircraftSaleEntry"].insert_one(entry.__dict__)

    @classmethod
    def mongodb(cls, db_name=MongoAtlas.db_name):
        db_user = MongoAtlas.db_user
        password = MongoAtlas.password
        client = pymongo.MongoClient(
            f"mongodb+srv://{db_user}:{password}@flydb.c4yh8.mongodb.net/{db_name}?retryWrites=true&w=majority",
            server_api=ServerApi("1"),
        )
        db = client[db_name]
        instance = cls()
        instance.conn = db
        return instance
