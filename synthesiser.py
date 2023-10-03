# init
from os import path
import numpy as np
from pynput import keyboard
from pedalboard import Pedalboard, Chorus, Reverb, LowpassFilter, load_plugin
from pedalboard.io import AudioFile
import music21
from keyboard_layout import KeyboardLayout
from tone import Tone
from audio_player import AudioPlayer
from time_going import Timeline
from tone import ADSRTone
from midiserial import MidiSerial
from note_player import NotePlayer
import time


smplRate = 44100

timeline = Timeline(IS_LOOPED = False)

board = Pedalboard([ Reverb(room_size=0.25)])
audioplayer = AudioPlayer(timeline,board)
audioplayer.start()

e = 2
def harmonics_maker():
    rng = np.random.default_rng()
    modifier = rng.random(18)>0.5
    harmonics = np.array([(np.power(e,np.log2(i)),np.power(e,np.log2(i))) for i in range(2,20)])
    harmonics[:,0] = harmonics[:,0]+modifier*10000
    harmonics[:,1] = harmonics[:,1]+modifier*10000
    return harmonics

def scaling_1(point):
    return 27.5 * np.power(e,point/12)
def scaling_2(point):
    scale = [2,2,1,2,2,2,1]
    result = 1
    for i in range(point):
        result += scale[i%len(scale)]
    return result
def scaling(point):
    return scaling_1(scaling_2(point))

# keyboard_layout = KeyboardLayout()
# keyboard_layout.load('complete left to right')
# keyboard_layout.start(scaling_1, harmonics, timeline)


notePlayer_1 = NotePlayer(scaling_1, harmonics_maker, timeline)
notePlayer_1.startNote(10)
time.sleep(1)
notePlayer_1.stopNote(10)
notePlayer_1.startNote(10)
time.sleep(1)
notePlayer_1.stopNote(10)
time.sleep(1)
audioplayer.stop()

# midsr = MidiSerial('/dev/cu.usbserial-00000000')
# midsr.start(scaling_1, harmonics_maker, timeline)