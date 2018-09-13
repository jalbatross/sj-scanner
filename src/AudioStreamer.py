import json
import requests
import threading
import time
import sys

from pydub import AudioSegment
from datetime import datetime
from pathlib import Path

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
    
    maxChunks = 4096
    chunks = 0
    threshold = 0
    dataBuffer = []

    for chunk in r.iter_content(chunk_size=512):
      
      threshold = threshold + self.processAudio(chunk)

      if (threshold <= 0):
        threshold = 0
        if (len(dataBuffer) <= 0):
          continue
        else:
          copiedBuf = dataBuffer[:]
          dataBuffer = []
          t = threading.Thread(target=self.buildAudioFile, args=(copiedBuf,))
          t.start()
          continue

      # otherwise there was sound
      print(chunks, ' thresh: ', threshold)
      dataBuffer.append(chunk)

      chunks += 1

      if (chunks > maxChunks):
        break

    return 0

  def processAudio(self, data):
    temp = open('temp', 'wb')
    temp.write(data)
    temp.close()

    try:
      audio = AudioSegment.from_mp3('temp')

      if (audio.max >= 1000):
        return 10
      else:
        return -10

    except:
      return 0

    #print(' max vol: ',audio.max, ' was max vol')

  ###
  # buf is an iterable of mp3 data chunks
  #
  def buildAudioFile(self, buf):
    fileTitle = str(datetime.now())
    path = Path('audioLogs/%s.mp3' % fileTitle)
    try:
      with open(path, 'wb') as fd:
        for data in buf:
          fd.write(data)
    except:
      print("Unexpected error:", sys.exc_info()[0])
      return False

    return True








