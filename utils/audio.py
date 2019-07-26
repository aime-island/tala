import os
from io import BytesIO
import soundfile as sf


def save_audio(file, id, corpus):
    data, samplerate = sf.read(BytesIO(file))
    seconds = len(data) / samplerate
    corpus_name, _ = os.path.splitext(corpus)
    path = os.path.join('./audio/', corpus_name)
    if not os.path.exists(path):
        os.makedirs(path)
    filename = id + ".wav"
    fileLocation = os.path.join(path, filename)
    sf.write(fileLocation, data, samplerate)
    return seconds
