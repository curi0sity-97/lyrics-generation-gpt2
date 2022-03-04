import re
import pandas as pd
from tqdm import tqdm


def get_strophe_amount(text, pattern):
    text.replace("\r", "")
    return len(re.findall(pattern, text))

def get_verse_amount(text):
    return sum(1 for line in text.splitlines() if line.strip())


def get_word_amount(text):
    return len(text.split())


# This method retrievies text structure for multiple texts
def get_lyrics_structure(lyrics):
    structures = list()
    pattern = re.compile(r"\n\s*\n")
    for song_text in tqdm(lyrics, desc="Amount of songs"):
        structures.append([get_strophe_amount(song_text, pattern), get_verse_amount(song_text), get_word_amount(song_text)])

    df = pd.DataFrame(structures, columns=['strophes', 'lines', 'words'])
    df.index.name = 'index'
    return df
