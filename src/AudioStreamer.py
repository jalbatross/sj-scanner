import json
import requests
import threading
import time
import sys
import io

from pydub import AudioSegment
from datetime import datetime
from pathlib import Path

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from ffmpy import FFmpeg

import os



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

    prevDelta = 0
    delta = 0
    for chunk in r.iter_content(chunk_size=512):
      
      delta = self.processAudio(chunk)
      
      if (prevDelta < 0 and delta < 0 and len(dataBuffer) > 20):
        delta = prevDelta * 2

      prevDelta = delta

      threshold = threshold + delta

      if (threshold <= 0):
        threshold = 0

        if (len(dataBuffer) <= 0):
          pass
        elif (len(dataBuffer) >1 and len(dataBuffer) <= 10) :
          dataBuffer = []
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
        return 15
      else:
        return -2

    except:
      return 0

    #print(' max vol: ',audio.max, ' was max vol')

  ###
  # buf is an iterable of mp3 data chunks
  #
  def buildAudioFile(self, buf):
    fileTitle = str(datetime.now())

    pathMp3 = Path('audioLogs/%s.mp3' % fileTitle)
    
    
    try:
      with open(pathMp3, 'wb') as fd:
        for data in buf:
          fd.write(data)
      fd.close()

      pathWav = Path('audioLogs/%s.wav' % fileTitle)

      ff = FFmpeg(
        inputs={str(pathMp3): None},
        outputs={str(pathWav): '-acodec pcm_s16le -ac 1 -ar 16000'}
      )
      ff.run()

    except:
      print("Unexpected error:", sys.exc_info()[0])
      return False

    return True







def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))




