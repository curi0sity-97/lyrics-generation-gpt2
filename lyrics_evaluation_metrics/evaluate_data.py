import os

import pandas as pd
from Lib.get_texts import get_generated_lyrics, get_lyrics_dataset
from Lib.get_structure import get_lyrics_structure
from Lib.get_sentiment import calculate_sentiment_scores
from Lib.get_bagofwords import get_repetition_scores, combine_bag_of_words, lemmatize_lyrics


# This method performs the calculations of the evaluation metrics for a corpus of texts
# Information are stored in a pandas dataframe
# parameters: Text corpus as list, name of the *csv file
def evaluate_text(texts, name):

    # get song structure
    pd.set_option("display.max_columns", 20)
    pd.set_option("large_repr", "truncate")
    df = get_lyrics_structure(texts)
    print(df)

    # get bag of words
    counters = lemmatize_lyrics(texts)
    df_words = combine_bag_of_words(counters)
    rep_scores = get_repetition_scores(counters)
    df["bagofwords"] = counters
    df["repscores"] = rep_scores
    print(df)

    # get sentiment
    df2 = calculate_sentiment_scores(texts)
    df = pd.concat([df, df2], axis=1)
    print(df)

    print(df.columns)
    # Write to file
    df.to_csv(f"Evaluated/evaluated-{name}-{len(df.index)}.csv")
    df_words.to_csv(f"Evaluated/evaluated-{name}-{len(df.index)}-bagofwords.csv")



#%%
lyrics = get_lyrics_dataset()[150000:300000]
evaluate_text(lyrics, "dataset-validation")


#%%
lyrics = get_generated_lyrics()
evaluate_text(lyrics, "generated")


#%%
lyrics = [text.replace("\n\n", "\n") for text in get_generated_lyrics(folder=r"Z:\Training-Data\generated_orig")]
evaluate_text(lyrics, "gpt-org")


#%%
df = pd.read_csv("datasets/kaggle_poetry.csv")
poems = df["content"].to_list()
evaluate_text(poems, "poems")

#%%
lyrics = get_generated_lyrics(folder=r"Z:\Training-Data\generated")
evaluate_text(lyrics, "gpt-custom")






