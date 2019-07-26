from os import listdir
from os.path import join, isfile
import pandas as pd


def read_files():
    files = [f for f in listdir('./corpus') if isfile(join('./corpus', f))]
    files_array = []
    for f in files:
        unread = pd.read_csv(join('./corpus', f))
        read = pd.read_csv(join('./transcripts', f))
        obj = {
            'file': f,
            'unread': len(unread),
            'read': len(read)
        }
        files_array.append(obj)
    return files_array