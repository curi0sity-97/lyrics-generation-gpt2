import sys
import pandas as pd
from langdetect import detect
import re
import sqlite3
import string


''' Data to do
1. Check for songs with empty line after each verse \r\n\r\n <example verse line> \r\n\r\n or \r\n\r\n\r\n
2. Check songs which contrain (chorus),  (1st verse), (8x), [Chorus: Mercedes Martinez] [<artist name>] -Chorus-   for example
'''


def get_infos():
    con = sqlite3.connect("lyrics.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    response = cur.execute(f'''SELECT lyrics FROM lyrics''').fetchall()
    text = " ".join(response)


    chars = sorted(list(set(text)), reverse=True)
    print("Total Characters: ", len(text))
    print("Total Vocab: ", len(chars))
    print(chars)



def read_csv_into_db(src_file):
    chunk = pd.read_csv(src_file, chunksize=1000000)
    pd_df = pd.concat(chunk)
    pd_df['Lyrics'] = pd_df['Lyrics'].fillna('').apply(str)

    con = sqlite3.connect("lyrics.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS lyrics (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            artist TEXT,
                            title TEXT,
                            lyrics BLOB,
                            lang TEXT,
                            allowed_chars INTEGER                         
                            )''')
    # Insert DataFrame to Table
    for row in pd_df.itertuples():
        cur.execute('''INSERT INTO lyrics (artist, title, lyrics)
                        VALUES (?,?,?)''',
                    (row.Band, row.Song, row.Lyrics))

    con.commit()
    con.close()


# Get language for songs
def detect_lang():
    con = sqlite3.connect("lyrics.db")
    cur = con.cursor()

    cur.execute('''SELECT id, lyrics, lang FROM lyrics WHERE lang IS NULL''')
    response = cur.fetchall()
    counter = 0
    for (id, lyrics, lang) in response:

        if counter > 10000:
            con.commit()
            counter = 0
            print(id)
        try:
            lang_detected = detect(lyrics)
        except:
            lang_detected = None
        cur.execute('''UPDATE lyrics SET lang = ? WHERE id = ?''', (lang_detected, id))
        counter += 1

    con.commit()
    cur.execute('''SELECT lang, COUNT(id)
                    FROM lyrics
                    GROUP BY lang
                    ORDER BY COUNT(id) DESC''')
    print(cur.fetchall())
    con.close()


# Remove unwanted patterns
def unwanted_patterns():
    con = sqlite3.connect("lyrics.db")
    cur = con.cursor()

    cur.execute(f'''SELECT id, lyrics FROM lyrics WHERE no_descriptors IS NULL ''')
    response = cur.fetchall()
    size = len(response)
    count = 0

    pattern_artist = re.compile('\[.*\]', re.IGNORECASE)
    pattern_chorus = re.compile('chorus', re.IGNORECASE)
    pattern_verse = re.compile('verse', re.IGNORECASE)

    for (id, lyrics) in response:
        # Only further investigate if it contains descriptor or text in square brackets at all
        if pattern_chorus.search(lyrics) or pattern_verse.search(lyrics) or pattern_artist.search(lyrics):
            # Split text into individual lines
            lines = lyrics.split("\n")
            for line in lines:
                # Check if line has a descriptor in square brackets or only consists of "chorus" or "verse"
                if pattern_chorus.search(line) or pattern_verse.search(line) or pattern_artist.search(line):
                    cur.execute('''UPDATE lyrics SET no_descriptors = ? WHERE id = ?''', (0, id))
                    print(line)
                elif line.startswith(" "):
                    print(line)
                    cur.execute('''UPDATE lyrics SET no_descriptors = ? WHERE id = ?''', (0, id))
                    count += 1
            count += 1
            cur.execute('''UPDATE lyrics SET no_descriptors = ? WHERE id = ?''', (0, id))
        else:
            cur.execute('''UPDATE lyrics SET no_descriptors = ? WHERE id = ?''', (1, id))

    print(count, "/", size, "->", count/size*100, "%")
    con.commit()


# Set marker for lyrics that have not allowed chars
def check_characters():
    allowed = set(string.ascii_letters + string.digits + string.whitespace + "()\[\]$?%!,_:;/.!\"#'%\*/\-")
    con = sqlite3.connect("lyrics.db")
    cur = con.cursor()
    cur.execute('''SELECT id, lyrics, lang, allowed_chars FROM lyrics WHERE allowed_chars IS NULL''')
    response = cur.fetchall()

    for (id, lyrics, lang, allowed_chars) in response:
        # Check if all chars are in allowed set
        chars_ok = set(lyrics) <= allowed
        if chars_ok:
            cur.execute('''UPDATE lyrics SET allowed_chars = ? WHERE id = ?''', (1, id))
        else:
            cur.execute('''UPDATE lyrics SET allowed_chars = ? WHERE id = ?''', (0, id))

    con.commit()
    con.close()



# Get lyrics for training data
def get_lyrics_text(limit=None, random=False):
    con = sqlite3.connect("lyrics.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    cur.execute(f'''SELECT lyrics FROM lyrics WHERE allowed_chars=1 AND lang='en' AND no_descriptors=1 AND words<1000
                    {" ORDER BY RANDOM() " if random else ""}
                    {" LIMIT "+ str(limit) if limit else ""}''')
    response = cur.fetchall()
    joined = "\r\n\r<|endoftext|>\r\n\r<|startoftext|>\r\n\r".join(response)
    return ("<|startoftext|>\r\n\r" + joined + "\r\n\r<|endoftext|>").replace("\r", "")



if __name__ == "__main__":
    get_infos()
    sys.exit()
    start_time = time.time()

    limit = None
    dest = r"C:\Users\Philipp\PycharmProjects\gpt-2\src"

    text = get_lyrics_text(limit=limit, random=False)
    f = open( f"test-lyrics-{limit}.txt", "w", encoding="utf-8").write(text)
    print("--- %s seconds ---" % (time.time() - start_time))