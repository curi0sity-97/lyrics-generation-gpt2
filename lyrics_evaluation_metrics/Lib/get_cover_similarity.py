#from sentence_transformers import SentenceTransformer
#from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import ast
import statistics
from nltk.translate.bleu_score import sentence_bleu

#model = SentenceTransformer('bert-base-nli-mean-tokens')


def get_lyrics_and_covers():
    df = pd.read_csv(r"Z:\Training-Data\covers\covers.csv", index_col=0)
    elements = list()
    for index in df.index:
        if pd.isna(df["completions"][index]):
            break
        completions = list(filter(None, ast.literal_eval(df["completions"][index])))
        end = df["start"][index]
        elements.append((end, completions))
    return elements


def get_BLEU_scores(covers):
    scores = list()
    for end, completions in get_lyrics_and_covers():
        bleus = list()
        for cover in completions:
            print(end[:10], " ---- ", cover[:10])
            bleus.append(sentence_bleu(end, cover))
        scores.append(bleus)
    return scores


covers = get_lyrics_and_covers()
bleus = get_BLEU_scores(covers)
for bleu in bleus:
    print(bleu)
#for org, covers in get_lyrics_and_covers():
#    print(org, covers)

