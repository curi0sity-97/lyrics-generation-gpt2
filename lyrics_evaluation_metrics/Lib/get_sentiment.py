from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from p_tqdm import p_map

sia = SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    return list(sia.polarity_scores(text).values())


# Get sentiment analysis results as dataframe form multiple texts
def calculate_sentiment_scores(lyrics):
    # Multi threading for speed-up
    scores = p_map(get_sentiment_score, lyrics)

    df = pd.DataFrame(scores, columns=['neg', 'neu', 'pos', 'compound'])
    df.index.name = 'index'
    # Calculate custom emotional intensity score
    df['intensity'] = df.apply(lambda row: 1 - row['neu'], axis=1)
    return df