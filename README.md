Plane Finder App is a web scraper designed to collect price entries from aircraft
sales websites. It collects prices over time and saves them.

To install locally use: `python -m pip install -e .` from the root directory.

## TODO:

1. Create some runnable module that performs the crawling operation. 
   Currently, there is a test function that does this, but it feels
   awkward to run a pytest to do work.

2. Copy test database to production database.

3. Implement some kind of progress meter when crawling.
