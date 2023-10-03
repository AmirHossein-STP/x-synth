import serial
from tone import ADSRTone
import numpy as np

class MidiSerial:
    def __init__(self, port):
        self.port = port
        self.tones = dict()
        
    def start(self,  scaling, harmonic_maker, timeline):
        # with serial.Serial('/dev/cu.usbserial-00000000', 31250) as ser:
        with serial.Serial(self.port, 31250) as ser:
            #  x = ser.read()          # read one byte
            while True:
                s = ser.read()        # read up to ten bytes (timeout)
                if int.from_bytes(s, "big") == 0x90:
                    note_byte = ser.read() 
                    vel_byte = ser.read() 

                    index = int.from_bytes(note_byte, "big")
                    vel = int.from_bytes(vel_byte, "big")
                    
                    fundamental = scaling(index-21)
                    vel = ((2**(vel/10)-1024)*(1-0.02)/1023.7+1)
                    vel *= (30/((index-20)*(index-20)/25))
                    print("start:  ",index," vel:",vel)
                    tone = ADSRTone(fundamental, harmonic_maker(),volume=vel)
                    timeline.add_tone(tone)
                    self.tones[index]=tone


                elif int.from_bytes(s, "big") == 0x80:
                    note = ser.read() 
                    vel_byte = ser.read() 

                    try:
                        index = int.from_bytes(note, "big")
                        vel = int.from_bytes(vel_byte, "big")
                        print("stop:  ",index," vel:",vel)
                        tone = self.tones.get(index, None)
                        if tone is not None:
                            timeline.remove_tone(tone)
                            self.tones.pop(index)
                    except AttributeError:
                        pass
            #  line = ser.readline()   # read a '\n' terminated line