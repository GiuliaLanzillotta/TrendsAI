# To analyse the data we will use the Google
# Cloud Natural Language API
# To use this code you will need the Google SDK
import sys
# Imports the Google Cloud client library

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types




class LanguageAnalyser:
    # This class provides all the code to do language
    # analysis with the google cloud nlp kit.

    def __init__(self) -> None:
        super().__init__()
        self.client = language.LanguageServiceClient()

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

        # Detect and send native Python encoding to
        # receive correct word offsets.
        encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            encoding = enums.EncodingType.UTF16
        try:
            result = self.client.analyze_sentiment(document, encoding)
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
        # The Natural Language API processes the given text
        # to extract the entities and determine sentiment.
        # API response has this structure :
        # {
        #   "entities": [
        #     {
        #       "name": name of the entity
        #       "type": type of the entity
        #       ...
        #       "salience":  indicates the importance or relevance
        #           of this entity to the entire document text.
        #       "mentions": list of all the mentions for the entity
        #       [
        #         {
        #           "text": {
        #             "content": content of the mention
        #             ...
        #           },
        #           "type": can be PROPER / COMMON
        #           "sentiment": analysis for each mention
        #           {
        #             ...
        #           }
        #         }
        #       ],
        #       "sentiment": result of the analysis for the entity
        #       {
        #         "magnitude": level of sentiment in the text
        #         "score": ranges from -1 (negative) to 1 (positive)
        #       }
        #     },
        #     ...
        #   ],
        #   "language": language used
        # }

        print("")
        print("Start analysing...")

        document = types.Document(
            content=text.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)

        # Detect and send native Python encoding to
        # receive correct word offsets.
        encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            encoding = enums.EncodingType.UTF16
        try:
            result = self.client.analyze_entity_sentiment(document, encoding)
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




