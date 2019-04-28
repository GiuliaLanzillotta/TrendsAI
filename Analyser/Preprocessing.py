import re
import os
import simplejson as json
from nltk.tokenize import WordPunctTokenizer
from Analyser import data_folder


class Loader:
    # This class contains the code to load
    # the data for a specified woeid from file.
    # Default region is Rome.
    def __init__(self, woeid=721943) -> None:
        super().__init__()
        self.data_file = os.path.join(data_folder, 'trends_data_{}.json'.format(woeid))

    def load_all_in_one(self):
        """
        This function will load all the tweets from the
        different trends in one list.
        """
        print("")
        print("Start preprocessing all in one...")
        all_tweets = []
        with open(self.data_file, 'r') as json_file:
            data = json.load(json_file)
            for trend in data.keys():
                tweets = data[trend]
                all_tweets.append(tweets)
        # flatten the list of lists
        flattened_tweets = [tweet for tweets in all_tweets for tweet in tweets]
        print("...done preprocessing.")
        print("")
        return flattened_tweets

    def load_dict(self):
        """
        This function will load all the tweets
        in a dictionary organized by trends.
        """
        print("")
        print("Start preprocessing all in one...")
        with open(self.data_file, 'r') as json_file:
            data = json.load(json_file)
        print("...done preprocessing.")
        print("")
        return data


class Cleaner:
    # This class contains all the code and the necessary
    # informations to clean the text Loaded by the Scraper module.

    # Tweets' text problems:
    #   1. Hashtags: we should give the hash-tagged
    #       words more weight during the analysis.
    #   2. Emoticons and accents: all unrecognized encodings
    #       appear in the text data as \u-code-. For now we
    #       choose to ignore this informations and delete them.
    #   3. Links: maybe it would be a good idea to count
    #       the number of links in a tweet.
    #   4. Numbers: numbers are not useful in the analysis.

    def __init__(self) -> None:
        super().__init__()
        self.hashtags_regex = re.compile("#")   # hashtag
        self.link_regex = re.compile("https?://[A-Za-z0-9./]+")  # link
        #
        # This expression will remove particular encodings
        # and numbers from the text
        self.encodings_regex = re.compile("[^a-zA-Z#]")  # not carachters

    def clean_tweet(self, tweet):
        """
        This function cleans the tweet text by :
            - removing links, hashtags, encodings, numbers
            - lower-casing the text
            - tokenizing the text and reassembling the tokens
                (to remove unnecessary space)
        TODO : considering upper case enphasis
        TODO : considering hashtags importance
        TODO : considering emojis meaning
        """
        no_links = self.link_regex.sub(" ", tweet)
        no_hashtag = self.hashtags_regex.sub("", no_links)
        no_encodings = self.encodings_regex.sub(" ", no_hashtag)
        lower_case = no_encodings.lower()
        tokenizer = WordPunctTokenizer()
        words = tokenizer.tokenize(lower_case)
        cleaned_tweet = (" ".join(words)).strip()
        return cleaned_tweet


def clean_data(tweets):
    """
    This function uses a Cleaner object
    to preprocess the text data.
    The tweets are cleaned and grouped in
    a unique text.
    """
    cleaner = Cleaner()
    cleaned_tweets = []
    print("")
    print("Start cleaning...")
    for tweet in tweets:
        cleaned_tweet = cleaner.clean_tweet(tweet)
        cleaned_tweets.append(cleaned_tweet)

    cleaned_data = ("\n".join(cleaned_tweets)).strip()
    print("... done cleaning.")
    print("")
    return cleaned_data


def prepare_data_all_in_one(woeid=None):
    """
    This function does all the preprocessing steps,
    loading all the tweets data in one list:
        1. Load data with a Loader object
        2. Clean data calling the @clean_data function
    If a woeid is not given it will use the deault
    woeid of the Loader object (see Loader class).
    """
    if woeid:
        loader = Loader(woeid)
    else:
        loader = Loader()
    text_data = loader.load_all_in_one()
    cleaned_data = clean_data(text_data)
    return cleaned_data


def prepare_data_by_trends(woeid=None):
    """
        This function does all the preprocessing steps,
        loading all the tweets data in a dictionary,
        organised by trends:
            1. Load data with a Loader object
            2. Clean data calling the @clean_data function
        If a woeid is not given it will use the deault
        woeid of the Loader object (see Loader class).
        """
    if woeid:
        loader = Loader(woeid)
    else:
        loader = Loader()
    text_data = loader.load_dict()

    cleaned_data = {}
    for trend in text_data.keys():
        cleaned_data[trend] = clean_data(text_data[trend])

    return cleaned_data