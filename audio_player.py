# open audio
import pyaudio
import numpy as np

class AudioPlayer(object):

    def __init__(self, timeline, board, IS_LOOPED = False, smplRate = 44100):
        self.paud = pyaudio.PyAudio()
        self.position = 0
        self.timeline = timeline
        self.board = board
        self.IS_LOOPED = IS_LOOPED
        self.smplRate = 44100
        self.stream = None

    def callback_wrapper(self):
        def callback(in_data, frame_count, time_info, status):
            # If len(data) is less than requested frame_count, PyAudio automatically
            # assumes the stream is finished, and the stream stops.
            if self.timeline.size >= (self.position + frame_count):
                data = self.timeline[self.position:self.position+frame_count].copy()
                if not self.IS_LOOPED:
                    self.timeline[self.position:self.position+frame_count] = 0
                self.position += frame_count
            else:
                data = self.timeline[self.position:].copy()
                if not self.IS_LOOPED:
                    self.timeline[self.position:] = 0
                self.position += frame_count
                self.position -= self.timeline.size
                data = np.append(data, self.timeline[:self.position])
                if not self.IS_LOOPED:
                    self.timeline[:self.position] = 0
                    
            data = self.board.process(data,self.smplRate,reset = False)
            return (data, pyaudio.paContinue)
        return callback

    def start(self):
        self.stream = self.paud.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate=self.smplRate,
                    output=True,
                    stream_callback=self.callback_wrapper()
                    )
        
    def stop(self):
        self.stream.close()
        self.paud.terminate()