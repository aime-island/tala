import pandas as pd
import os
from utils.audio import save_audio
import asyncio


def make_queue(queue, filename):
    data = pd.read_csv(os.path.join('./corpus', filename), sep='\t')

    for _, row in data.iterrows():
        queue.put({'utterance': row['utterance'], 'id': row['id']})


def remove_utterance(id, corpus):
    path = os.path.join('./corpus', corpus)
    df = pd.read_csv(path, sep='\t')
    df = df[df.id != id]
    df.to_csv(path, index=False, sep='\t')
    return "none"

def save_utterances(transcript_queue, audio_queue, corpus):
    while(True):
        transcript = transcript_queue.get()
        audio = audio_queue.get()
        seconds = save_audio(audio, transcript['id'], corpus)
        row = {
            'utterance': transcript['transcript'],
            'id': transcript['id'] + '.wav',
            'seconds': seconds
        }
        df = pd.DataFrame(columns=['utterance', 'id'])
        df = df.append(row, ignore_index=True)
        df.to_csv(
            os.path.join('./transcripts', corpus),
            mode='a', header=False, index=False, sep='\t')
        _ = remove_utterance(transcript['id'], corpus)
        transcript_queue.task_done()
