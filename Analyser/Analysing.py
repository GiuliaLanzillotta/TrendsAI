# To analyse the data we will use the Google
# Cloud Natural Language API
# To use this code you will need the Google SDK
import sys
import statistics
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#
# ENTITY SENTIMENT ANALYSIS
# Combining entity analysis and sentiment analysis:
# this analysis attempts to determine the sentiment
# expressed about entities within the text.
# Entity sentiment is represented by :
#   - numerical score
#   - magnitude values
# and is determined for each mention of an entity.
# Those scores are then aggregated into an overall
# sentiment score and magnitude for an entity.
#


class LanguageAnalyser:
    # This class provides all the code to do language
    # analysis with the google cloud nlp kit.

    def __init__(self) -> None:
        super().__init__()
        self.client = language.LanguageServiceClient()
        # Detect and send native Python encoding to
        # receive correct word offsets.
        self.encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            self.encoding = enums.EncodingType.UTF16

    def analyse_sentiment(self, text):
        """
        This function computes the sentiment
        analysis of the provided text.
        """
        print("")
        print("Start analysing...")
        document = types.Document(
            content=text.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)
        try:
            result = self.client.analyze_sentiment(document, self.encoding)
        except Exception as e:
            print(e)
            exit(1)
        print("... done analysis.")
        print("")

        return result

    def analyse_entity_sentiment(self, text):
        """
        This function computes the entity-sentiment
        analysis of the provided text.
        NB: Entity sentiment analysis is only
            supported in English and Japanese now.
        """
        print("")
        print("Start analysing...")
        document = types.Document(
            content=text.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)
        try:
            result = self.client.analyze_entity_sentiment(document, self.encoding)
        except Exception as e:
            print(e)
            exit(1)
        print("... done analysis.")
        print("")

        return result

    @staticmethod
    def print_sentiment_result(result):
        score = result.document_sentiment.score
        magnitude = result.document_sentiment.magnitude
        print('Overall Sentiment: score of {} with magnitude of {}'.format(
            score, magnitude))

    @staticmethod
    def print_entity_sentiment_result(result):
        for entity in result.entities:
            print(u'Name: "{}"'.format(entity.name))
            print(u'Salience: {}'.format(entity.salience))
            print(u'Sentiment: {}\n'.format(entity.sentiment))


def analyse_all(trends_data):
    """
    This function takes twitter trends
    data (already preprocessed) all in one text
    and returns the entity-sentiment analysis
    of the text in the form of a dictionary.
    Structure of the result dictionary:

    """
    result = {}
    analyser = LanguageAnalyser()
    try:
        analysis = analyser.analyse_sentiment(trends_data)
        for entity in analysis.entities:
            result[entity] = {
                "name": entity.name,
                "salience": entity.salience,
                "sentiment": entity.sentiment
            }
    except Exception as e:
        print(e)
        exit(1)

    return result


def analyse_trends(trends_data):
    """
    This function takes twitter trends data
    (already preprocessed) in form of a dictionary
    and returns the sentiment analysis for each
    trend and an overall analysis over the data.
    The result is in the form of a dictionary.
    Structure of the result dictonary :
        {
            trend_name :
            {
                "score": trend_score,
                "magnitude": trend_magnitude
            }
            "score": overall_score,
            "magnitude": overall_magnitude

        }

    TODO : weighted overall sentiment
    NB: this overall sentiment is now calculated
    as the average of sentiments, but it could be
    weighted on the 'importance' of the trend, measured
    as the total number of tweets for the trend,
    or the average number of comments under a tweet.
    """
    scores = []
    magnitudes = []
    result = {}
    analyser = LanguageAnalyser()
    for trend in trends_data.keys():
        data = trends_data[trend]
        try:
            analysis = analyser.analyse_sentiment(data)
            score = analysis.document_sentiment.score
            magnitude = analysis.document_sentiment.magnitude
            scores.append(score)
            magnitudes.append(magnitude)
            result[trend] = {
                "score": score,
                "magnitude": magnitude
            }
        except Exception as e:
            print(e)
            continue

    average_score = statistics.mean(scores)
    average_magnitude = statistics.mean(magnitudes)
    result["score"] = average_score
    result["magnitude"] = average_magnitude
    return result

