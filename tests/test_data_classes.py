from pathlib import Path
from datetime import datetime, date
from planefinder.data import AircraftSaleEntry
from planefinder import trade_a_plane
from planefinder import utils
from bs4 import BeautifulSoup


def test_aircraft_sale_entry():
    """
    Tests whether an AircraftSaleEntry can be created.
    """
    AircraftSaleEntry(
        id=2399126,
        url="https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make=CESSNA&model=182Q+SKYLANE&listing_id=2400626&s-type=aircraft",
        seller_id=49743,
        price=15000,
        make_model="CESSNA 182Q SKYLANE",
        registration="N735GS",
        description="1977 Cessna 182Q Skylane, 3461TT, 798 SMOH, 483 SPOH, Garmin GTN 430W, Stratus ES ADS-B Out Transponder (ADS-B In WiFI Traffic and Wx Link to IPad (Foreflight), Narco Mark 12D, Garmin GMA 340, Bendix King KI206, JPI EGT-701 Engine Monitor, Horton STOL Kit (Leading Edge Cuff, Droop Wing Tips, Stall Fences), Rosen Sun Visors, Standby Altimeter, & More!",
        search_date=datetime(2021, 12, 12, 11, 53),
        ttaf=0,
        smoh=0,
    )


def test_read_entry_from_html():
    """
    Read
    """
    this_dir = Path(__file__).parent
    test_listing = this_dir.joinpath("single-result-listing.html")
    soup = utils.read_html_into_soup(test_listing)
    listing = soup.find(trade_a_plane.is_listing_result)
    # Parsed values equal expected values
    assert trade_a_plane.listing_id(listing) == "2399126"
    assert trade_a_plane.seller_id(listing) == "49743"
    assert trade_a_plane.last_update(listing) == date(2021, 11, 9)
    test_details = this_dir.joinpath("aircraft-detail.html")
    with open(test_details) as f:
        html = f.read()
    soup = BeautifulSoup(html, features="html.parser")
    assert trade_a_plane.make_model(soup) == "CESSNA 182Q SKYLANE"
    assert trade_a_plane.price(soup) == 250000
    assert trade_a_plane.registration(soup) == "N7574S"
    expected_description = """*News Alert* High demand highly desirable Q model has hit the market!!! 



I am listing this aircraft for a friend, I was a previous owner in 2017 and passed along the airplane to my good friend after my daughter was born, and he has taken this plane to the next level!!! 



This 182Q checks all the boxes. Low time, complete records, no damage history, no hail damage, low time recent motor overhaul (overhauled in 2010 by Air Transport International), stellar avionics. The paint and interior is dated, but still in great condition. If I owned the plane, I would keep it how it is, but if you'd like to freshen up the paint and/or interior, it could definitely use a refresh, and the beautiful thing is that if you choose to do that, you can pick your own paint scheme and interior colors, making this a fully customized "like new" Cessna 182. A nicely equipped new one will cost you $600,000+... and you won't get the option of state-of-the-art Garmin TOUCHSCREEN avionics!!! Top of the line with every option and feature you can imagine, including XM Satellite radio and weather!!! 



You can have this one fully customized and decked out for less than half of that!!! You won't have to worry about the avionics or the engine at all!! 



Due to the high interest and large number of inquiries, please reference logbooks to answer your questions before inquiring. The logbook files are labeled so you can easily open the one you're interested in. If it's something you cannot find, then I would be happy to research and help find the answer for you. This is a clean and straight airframe, engine, and avionics platform. These go for about a buck 75 with mid-time engine, clean airframe, and basic avionics. Add a 90k panel, and that's how we priced this beauty. These aircraft are used all over the world, and it's rare to find one this nice and well equipped. 



The aircraft's annual inspection is due in December 2021, and any discrepancies found will be corrected prior to sale, and therefore will be sold with a fresh annual. 



Thanks for your interest. 



Aircraft Location: GYI"""
    assert trade_a_plane.description(soup) == expected_description
    assert trade_a_plane.ttaf(soup) == 3388
    assert trade_a_plane.engine_time(soup) == "271 SMOH"
