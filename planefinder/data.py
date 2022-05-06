from datetime import datetime
import attr
import requests
import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from pymongo.results import InsertOneResult

from planefinder.crawler import ListingEntry


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
            smoh=entry.detail.smoh
        )

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
    
    def save(self, object_):
        if isinstance(object_, AircraftSaleEntry):
            return self._save_aircraft_entry(object_)
        else:
            raise NotImplementedError("I only know how to save AircraftSaleEntry objects")
    
    def delete(self, object_):
        if isinstance(object_, ObjectId):
            self.conn["AircraftSaleEntry"].delete_one({"_id": object_})
        elif isinstance(object_, AircraftSaleEntry):
            self.conn["AircraftSaleEntry"].delete_one({"id": object_.id})
        else:
            raise NotImplementedError("Not yet implemented")

    def _save_aircraft_entry(self, entry: AircraftSaleEntry) -> InsertOneResult:
        return self.conn["AircraftSaleEntry"].insert_one(entry.__dict__).inserted_id

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
