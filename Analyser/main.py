# Runs the project
import simplejson as json
import os
from Analyser import Analysing, Preprocessing, result_folder
from Scraper import TrendsReading


def all_in_one(woeid=None):
    """
    Get the all in one analysis for the
    specified region and store it in json.
    """
    if woeid:
        data = Preprocessing.prepare_data_all_in_one(woeid)
        # The result will be written in this file
        result_file = os.path.join(result_folder, 'all_result_{}.json'.format(woeid))
    else:
        data = Preprocessing.prepare_data_all_in_one()
        # The result will be written in this file
        result_file = os.path.join(result_folder, 'all_result_default.json')

    analysis = Analysing.analyse_all(data)
    # Writing the dict to file in json format
    print("")
    print("Writing results to file")
    with open(result_file, 'w') as f:
        json.dump(analysis, f)


def by_trends(woeid=None):
    """
        Get the by-trends analysis for the
        specified region and store it in json.
        """
    if woeid:
        data = Preprocessing.prepare_data_by_trends(woeid)
        # The result will be written in this file
        result_file = os.path.join(result_folder, 'by_trends_result_{}.json'.format(woeid))
    else:
        data = Preprocessing.prepare_data_by_trends()
        # The result will be written in this file
        result_file = os.path.join(result_folder, 'by_trends_result_default.json')

    analysis = Analysing.analyse_trends(data)

    # Writing the dict to file in json format
    print("")
    print("Writing results to file")
    with open(result_file, 'w') as f:
        json.dump(analysis, f)


if __name__ == '__main__':
    by_trends()

