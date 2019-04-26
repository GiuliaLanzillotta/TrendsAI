# This package contains the code to get the data about
# Twitter trends that will be used by the Analyser.
#
# To have access to Twitter data access keys are needed.
#
# I will use the Twitter library tweepy to easily get the
# data needed.
#

#
# Reading the keys
#
import configparser
import os
data_folder = os.path.join(os.path.dirname(__file__), '../Data/')
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), './Access.ini'))
consumerKeys = config['CONSUMERAPIKEYS']
accessTokens = config['ACCESSTOKENS']




