from tqdm import tqdm
import json
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import sqlite3
from collections import Counter
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import pandas as pd
from p_tqdm import p_map



# Helper method for word type info
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmatize_lyrics(lyrics):
    # Use multi-processing for speed-up
    counters = p_map(lemmatize, lyrics)
    return counters

# Regex for building Tokenizer: Machtes an word character
tokenizer = RegexpTokenizer(r'\w+')
# Build lemmatizer
lemma = WordNetLemmatizer()

# Lemmatize any text. Word stems are lowered for better summarization
# Returns a counter dictonary for every text
def lemmatize(text):
    tokens, tokens_lemmatized = tokenizer.tokenize(text), []
    tokens_pos = nltk.pos_tag(tokens)
    for (word, pos) in tokens_pos:

        # Lemmatize text with additional word type information
        tokens_lemmatized.append(lemma.lemmatize(word, pos=get_wordnet_pos(pos)).lower())

    counter = Counter(tokens_lemmatized)

    # Remove stopwords
    stop_words = set([word.lower() for word in stopwords.words('english')])
    for stop_word in stop_words:
        counter.pop(stop_word, None)
    return counter



# This method combines N counter dictionaries into one dict (used for whole corpus of texts)
# Return dataframe with every single word stem and its abosulte and relative  frequency
def combine_bag_of_words(counters):
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)

    total_amount = sum(total_counter.values())
    look_up = total_counter
    total_counter = dict(total_counter)
    for key, value in total_counter.items():
        total_counter[key] = value / total_amount
    sorted_counter = sorted(total_counter.items(), key=lambda x: x[1], reverse=True)

    df = pd.DataFrame(index=total_counter.keys(), columns=["freq", "absolute"])
    counter = 0
    for (word, freq) in sorted_counter:
        df.loc[word] = freq, look_up[word]
        counter += 1
    print(df.sort_values(by=['freq'], ascending=False))
    return df


# Get repitiotion score
def get_repetition_scores(counters):
    rep_scores = list()
    for counter in counters:
        try:
            rep_scores.append(float(len(list(counter.keys())) / sum(counter.values())))
        except:
            rep_scores.append(float(0))
    return rep_scores