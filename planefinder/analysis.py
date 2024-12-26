import pandas as pd
import matplotlib.pyplot as plt
from planefinder.data import Database

def query_and_plot_trends():
    db = Database.mongodb()
    df = db.get_all_listings_as_dataframe()
    
    # Example: Plotting the number of listings per year
    df['year'] = pd.to_datetime(df['last_update']).dt.year
    listings_per_year = df.groupby('year').size()
    
    plt.figure(figsize=(10, 6))
    listings_per_year.plot(kind='bar')
    plt.title('Number of Aircraft Listings Per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Listings')
    plt.show()

# Add more functions as needed for different types of analysis and plotting

def get_all_listings(db_name: str) -> pd.DataFrame:
    db = Database.mongodb(db_name)
    df = db.get_all_listings_as_dataframe()
    return df

def get_listings_by_make_model(db_name: str) -> pd.Series:
    db = Database.mongodb(db_name)
    df = db.get_all_listings_as_dataframe()
    
    listings_by_make_model = df.groupby('make_model').size().sort_values(ascending=False)
    return listings_by_make_model

if __name__ == "__main__":
    pass
