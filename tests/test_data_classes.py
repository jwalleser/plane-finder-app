from datetime import datetime
from planefinder.main import AircraftSaleEntry

def test_aircraft_sale_entry():
    AircraftSaleEntry(url='https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&make=CESSNA&model=182Q+SKYLANE&listing_id=2400626&s-type=aircraft',
                    price=15000,
                    make_model='CESSNA 182Q SKYLANE',
                    registration='N735GS',
                    description='1977 Cessna 182Q Skylane, 3461TT, 798 SMOH, 483 SPOH, Garmin GTN 430W, Stratus ES ADS-B Out Transponder (ADS-B In WiFI Traffic and Wx Link to IPad (Foreflight), Narco Mark 12D, Garmin GMA 340, Bendix King KI206, JPI EGT-701 Engine Monitor, Horton STOL Kit (Leading Edge Cuff, Droop Wing Tips, Stall Fences), Rosen Sun Visors, Standby Altimeter, & More!',
                    search_date=datetime(2021, 12, 12, 11, 53),
                    ttaf=0,
                    smoh=0)