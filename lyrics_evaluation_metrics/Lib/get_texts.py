import os
import sqlite3


def get_generated_lyrics(folder=r"Z:\Training-Data\generated", files=None):
    songs = list()
    if not files:
        files = os.listdir(folder)
        try:
            files.remove('.idea')
        except ValueError:
            pass
        for file in files:
            songs.extend(open(os.path.join(folder, file), "r", encoding="utf-8").read().split("=" * 20 + "\n")[:-1])
    elif isinstance(files, list):
        for file in files:
            songs.extend(open(os.path.join(folder, file), "r", encoding="utf-8").read().split("=" * 20 + "\n")[:-1])
    elif isinstance(files, str):
        songs.extend(open(os.path.join(folder, files), "r", encoding="utf-8").read().split("=" * 20 + "\n")[:-1])
    else:
        raise Exception("not implemented")
    return songs


def get_lyrics_dataset():
    con = sqlite3.connect(r"C:\Users\Philipp\PycharmProjects\tensorflow_conda\lyrics.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    return cur.execute(f'''SELECT lyrics FROM lyrics WHERE allowed_chars=1 AND lang='en' AND no_descriptors=1 AND words<1000''').fetchall()


