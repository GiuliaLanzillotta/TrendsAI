import simplejson as json
import tweepy
import os
# importing the access keys from the init
from Scraper import consumerKeys, accessTokens, data_folder


class Reader:

    def __init__(self) -> None:
        super().__init__()
        auth = tweepy.OAuthHandler(consumerKeys['APIkey'],
                                   consumerKeys['APIsecretkey'])
        auth.set_access_token(accessTokens['AccessToken'],
                              accessTokens['AccessTokenSecret'])

        #
        # Create the api to connect to twitter with your creadentials
        # wait_on_rate_limit= True;
        # will make the api to automatically wait for rate
        # limits to replenish
        # wait_on_rate_limit_notify= Ture;
        # will make the api to print a notification when
        # Tweepyis waiting for rate limits to replenish
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True,
                              compression=True)

    @staticmethod
    def read_tweet(tweet):
        """
        This function is given a tweet in json format and
        reads it to get the needed information inside it.
        The structure of a tweet (only important infos):
        {
            "id" => tweets unique ID
            "text" => text of the tweet (140 character max)
            "created_at"=> tweet's creation date
            "place"=>{ info about the place
                        "id"=> place id
                        "name"=>
                        "full_name"=>
                        "place_type"=> type of the place (neighborhood/city)
                        "country_code"=>
                        "country"=> name of the country

                    }

        }


        """

        # For now we are only interested in the text
        # of the tweet.

        text = tweet['text']
        return text

    def get_trends(self, woeid=None):
        """
        Gets the trends for the specified woeid.
        If no woeid is specified get the global trends.
        NB: Twitter trending topics can change every
        5 minutes.
        """
        if woeid:
            trends = self.api.trends_place(id=woeid)
        else:
            trends = self.api.trends_available()

        #
        # The trends are available in this JSON format:
        # [
        #   {
        #       "trends":[
        #           {
        #               "name": name of the topic
        #               "url": Twitter Search url
        #               "query": Twitter Search query parameter
        #           },
        #           ...
        #               ],
        #        ...
        #       "locations":[
        #           {
        #               "name":
        #               "woeid":
        #           }
        #       ]
        #   }
        # ]
        #
        # From this infos we can get the tweets
        # for a specific topic
        return trends[0]['trends']

    def get_tweets(self, trend_name):
        """
        Gets the 15 most popular tweets from the specified trend,
        read them and return a list of read tweets.
        The tweets are read using the @read_tweet
        function.

        """
        trend_tweets = tweepy.Cursor(self.api.search, q=trend_name,
                                     result_type='popular',
                                     count=15)

        tweets = []
        for tweet in trend_tweets.items():
            tweet_json = tweet._json
            tweet_read = self.read_tweet(tweet_json)
            tweets.append(tweet_read)

        return tweets


def trends_data_builder(woeid=721943):
    """
    This function reads the trends data using a
    Reader objects and stores them in the Data folder.
    The default place is Rome.
    """
    #
    # The data read will be written in this file
    data_file = os.path.join(data_folder, 'trends_data_{}.txt'.format(woeid))

    reader = Reader()
    try:
        print("Start reading trends for woeid ", woeid)
        print("")
        trends = reader.get_trends(woeid=woeid)

        with open(data_file, 'w') as f:
            for trend in trends:
                trend_name = trend['name']
                print("Reading tweets for trend ", trend_name)
                print("")
                trend_tweets = reader.get_tweets(trend_name=trend_name)

                # write to file all the trend tweets
                f.write("TREND : %s\n" % trend_name)
                for tweet in trend_tweets:
                    f.write("%s\n" % tweet)

        print("Finished reading trends for woeid ", woeid)

    except tweepy.TweepError as e:
        error_code = e.message[0]['code']
        print("Error code ", error_code)
        exit(1)





