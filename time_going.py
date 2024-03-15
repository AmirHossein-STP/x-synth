import numpy as np
from os import path
from scipy.io import wavfile

class Timeline:
    def __init__(self, smplRate, duration = 2, IS_LOOPED = False):
        self.IS_LOOPED = IS_LOOPED
        self.smplRate = smplRate
        self.duration = duration
        self.tones = set()
        self.position = 0
        
    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, value):
        self._duration = value
        self.values = np.zeros(self._duration * self.smplRate, dtype = np.float32)
    
    def clear(self):
        self.tones = set()
        self.values = np.zeros(self.duration * self.smplRate, dtype = np.float32)
    
    def add(self, audio):
        data_size = audio.size
        if self.values.size >= (self.position + data_size):
            self.values[self.position:self.position+data_size] += audio
        else:
            audio.size - self.values.size
            self.values[self.position:] += audio[:self.values.size-self.position]
            self.values[:self.position+audio.size-self.values.size] += audio[self.values.size-self.position:]
    
    def walk(self, count):
        tones = set(self.tones)
        for tone in tones:
            self.add(tone.make(frame_count = count))

    def add_tone(self, tone):
        self.tones.add(tone)
    def remove_tone(self, tone):
        self.add(tone.make(still_on = False))
        self.tones.remove(tone)



    def save(self, new_file_name = None, is_wave = False):
        if new_file_name is None:
            new_file_name = input('enter your new timeline name: ')
        if not new_file_name:
            print("didn't save.")
        else:
            if is_wave:
                file_address = path.join('database/saved_sounds/' , new_file_name + '.wav')
                wavfile.write(file_address, self.smplRate, self.values)
            else:
                file_address = path.join('database/saved_sounds/' , new_file_name + '.npy')
                with open(file_address,'wb') as file:
                    np.save(file,self.values)
                    print(new_file_name + " saved as timeline successfully.")



    def load(self, file_name = None):
        if file_name is None:
            file_name = input('enter your timeline name: ')
        file_address = path.join('database/saved_sounds/' , file_name + '.npy')
        if not file_name:
            print("didn't load.")
        else:
            with open(file_address,'rb') as file:
                self.values += np.load(file)
                print(file_name + " loaded as timeline successfually.")