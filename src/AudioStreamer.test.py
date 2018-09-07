import unittest

from AudioStreamer import AudioStreamer

class AudioStreamerTest(unittest.TestCase):
  def setUp(self):
    self.streamer = AudioStreamer()
  
  # AudioStreamer is able to download a single regular file from a url
  def test_get_file(self):
    self.assertIsNotNone(self.streamer.getFile('aUrl'))

  # AudioStreamer should be able to get data from a file stream from a url
  def test_get_file_stream(self):
    self.assertIsNotNone(self.streamer.getFileStream('streamUrl'))

  # AudioStreamer should get audio file streams from urls
  def test_get_audio_stream(self):
    self.assertIsNotNone(self.streamer.getAudioFileStream('audioStreamUrl'))

if __name__ == '__main__':
    unittest.main()
