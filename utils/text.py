import pandas as pd
from io import StringIO
import os
import uuid
import csv


def save_corpus(text, name, self):
    text = text.decode('utf-8')
    data = StringIO(text)
    df = pd.read_csv(data, names=['utterance'], quoting=csv.QUOTE_NONE)
    df['id'] = 'nothing'
    for _, row in df.iterrows():
        row['id'] = str(uuid.uuid4())
    df['seconds'] = 0
    df.to_csv(os.path.join('./corpus', name), index=False, sep='\t')
    df2 = pd.DataFrame(columns=['utterance', 'id', 'seconds'])
    df2.to_csv(os.path.join('./transcripts', name), index=False, sep='\t')
    self.sendMessage('móttekið'.encode('utf8'))
