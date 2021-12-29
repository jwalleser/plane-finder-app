from pathlib import Path
from datetime import datetime
from planefinder.main import AircraftSaleEntry
from planefinder import trade_a_plane
from bs4 import BeautifulSoup

def test_aircraft_sale_entry():
    """
    Tests whether an AircraftSaleEntry can be created.
    """
    AircraftSaleEntry(id=2399126,
                    url='https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make=CESSNA&model=182Q+SKYLANE&listing_id=2400626&s-type=aircraft',
                    seller_id=49743,
                    price=15000,
                    make_model='CESSNA 182Q SKYLANE',
                    registration='N735GS',
                    description='1977 Cessna 182Q Skylane, 3461TT, 798 SMOH, 483 SPOH, Garmin GTN 430W, Stratus ES ADS-B Out Transponder (ADS-B In WiFI Traffic and Wx Link to IPad (Foreflight), Narco Mark 12D, Garmin GMA 340, Bendix King KI206, JPI EGT-701 Engine Monitor, Horton STOL Kit (Leading Edge Cuff, Droop Wing Tips, Stall Fences), Rosen Sun Visors, Standby Altimeter, & More!',
                    search_date=datetime(2021, 12, 12, 11, 53),
                    ttaf=0,
                    smoh=0)

def test_read_entry_from_html():
    """
    Read
    """
    this_dir = Path(__file__).parent
    test_listing = this_dir.joinpath('single-result-listing.html')
    with open(test_listing) as f:
        html = f.read()
    soup = BeautifulSoup(html, features='html.parser')
    listing = soup.find(trade_a_plane.is_listing_result)
    # Parsed values equal expected values
    assert trade_a_plane.listing_id(listing) == '2399126'
    assert trade_a_plane.seller_id(listing) == '49743'
    assert trade_a_plane.last_update(listing) == datetime(2021, 11, 9)
