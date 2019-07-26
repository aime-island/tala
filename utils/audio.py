import uuid
import ffmpeg
import os
from io import BytesIO
import soundfile as sf


def save_audio(file, id, corpus):
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')
    data, samplerate = sf.read(BytesIO(file))
    fileLocation = os.path.join('./tmp', str(uuid.uuid4()) + '.wav')
    sf.write(fileLocation, data, samplerate)
    convertedFile = normalize_file(fileLocation, id, corpus)
    os.remove(fileLocation)
    return convertedFile


def normalize_file(file, id, corpus):
    corpus_name, _ = os.path.splitext(corpus)
    path = os.path.join('./audio/', corpus_name)
    if not os.path.exists(path):
        os.makedirs(path)
    filename = id + ".wav"
    loc = os.path.join(path, filename)
    stream = ffmpeg.input(file)
    stream = ffmpeg.output(stream, loc, acodec='pcm_s16le', ac=1, ar='16k')
    ffmpeg.run(stream)
    return filename
