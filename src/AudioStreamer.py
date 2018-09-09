import json
import requests

from pydub import AudioSegment
from pydub.playback import play

import io

class AudioStreamer:

  def __init__(self):
    pass

  def getFile(self, fileUrl):
    return requests.get(fileUrl, verify=False)

  def getTextStream(self, streamUrl):
    r = requests.get(streamUrl, stream=True)

    streamData = []
    for line in r.iter_lines():
      if line:
        decoded_line = line.decode('utf-8')
        streamData.append(decoded_line)

    return streamData

  def getAudioFileStream(self, streamUrl):
    r = requests.get(streamUrl, stream=True)
    maxChunks = 1000

    chunks = 0
    with open('somedata', 'wb') as fd:
      for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
        chunks += 1

        if (chunks > maxChunks):
          break

    return fd



