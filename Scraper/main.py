# Run this code to have the data updated
from Scraper import TrendsReading

if __name__ == '__main__':
    # This will load data for the dafault
    # region (which is set to Rome for now)
    # Change the woeid to change the region.
    TrendsReading.trends_data_builder(woeid=None)

