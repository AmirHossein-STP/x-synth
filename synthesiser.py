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


smplRate = 96000

timeline = Timeline(IS_LOOPED = False, smplRate = smplRate)

board = Pedalboard([ Reverb(room_size=0.25)])
audioplayer = AudioPlayer(timeline,board)
audioplayer.start()

e = 2.1
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

notePlayer = NotePlayer(scaling_1, harmonics_maker, timeline)


# keyboard_layout = KeyboardLayout(notePlayer)
# keyboard_layout.load('complete left to right')
# keyboard_layout.start()
# while keyboard_layout.is_on:
#     time.sleep(1)


midsr = MidiSerial('/dev/cu.usbserial-00000000', notePlayer)
midsr.start()

time.sleep(1)
audioplayer.stop()