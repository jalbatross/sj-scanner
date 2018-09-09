import unittest

from AudioStreamer import AudioStreamer

class AudioStreamerTest(unittest.TestCase):
  def setUp(self):
    self.streamer = AudioStreamer()
  
  # AudioStreamer is able to download a single regular file from a url
  def test_get_file(self):
    self.assertIsNotNone(self.streamer.getFile('https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'))

  # AudioStreamer should be able to get data from a text stream
  def test_get_text_stream(self):
    self.assertIsNotNone(self.streamer.getTextStream('http://httpbin.org/stream/20'))

  # AudioStreamer should get audio file streams from urls
  def test_get_audio_stream(self):
    self.assertIsNotNone(self.streamer.getAudioFileStream(audioStreamUrl))

if __name__ == '__main__':
    unittest.main()
