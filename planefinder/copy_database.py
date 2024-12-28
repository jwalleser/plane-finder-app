"""
Copy database from one database to another
"""

import logging
from planefinder.data import Database

def copy_database(source, destination):
    """
    Copy the database from one database to another.
    """
    listings = source.get_all_listings()
    result = destination.bulk_save_or_update(listings)
    return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    source = Database.mongodb(db_name="planefinder_test_crawl")
    destination = Database.mongodb(db_name="planefinder")
    copy_database(source, destination)
    source.close()
    destination.close()
