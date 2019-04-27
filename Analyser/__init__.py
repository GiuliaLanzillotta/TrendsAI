# This module will preprocess and analyse data contained in the 'data_folder'
# The Analyser is built upon Preprocessing, Training and Testing.
#
import os
data_folder = os.path.join(os.path.dirname(__file__), '../Data/')
credentials_file = os.path.join(os.path.dirname(__file__), 'TrendsAI-916500c63c69.json')
# in order to use Google APIs we need to set an environment variable
print("Setup for Google APIs sdk...")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file
print("...done")
environment = None