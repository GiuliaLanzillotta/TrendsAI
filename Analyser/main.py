# Runs the project
from Analyser import Analysing, Preprocessing
from Scraper import TrendsReading
if __name__ == '__main__':

    data = Preprocessing.prepare_data()
    analyser = Analysing.LanguageAnalyser()
    analysis = analyser.analyse_sentiment(data)
    analyser.print_sentiment_result(analysis)