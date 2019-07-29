from os import listdir
from os.path import join, isfile
import pandas as pd


def read_files():
    files = [f for f in listdir('./corpus') if isfile(join('./corpus', f))]
    files_array = []
    for f in files:
        unread = pd.read_csv(join('./corpus', f), sep='\t')
        read = pd.read_csv(join('./transcripts', f), sep='\t')
        seconds = read['seconds'].sum()
        if not seconds:
            seconds = 0
        obj = {
            'file': f,
            'unread': len(unread),
            'read': len(read),
            'seconds': seconds
        }
        files_array.append(obj)
    return files_array