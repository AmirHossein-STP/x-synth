import numpy as np
from os import path

class Timeline:
    def __init__(self, duration = 2, IS_LOOPED = False, smplRate = 44100):
        self.IS_LOOPED = IS_LOOPED
        self.smplRate = smplRate
        self.duration = duration
        
    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, value):
        self._duration = value
        self.values = np.zeros(self._duration * self.smplRate, dtype = np.float32)
    
    def clear(self):
        self.values = np.zeros(self.duration * self.smplRate, dtype = np.float32)

    def save(self, new_file_name = None):
        if new_file_name is None:
            new_file_name = input('enter your new timeline name')
        if not new_file_name:
            print("didn't save.")
        else:
            file_address = path.join('database/saved_sounds/' , new_file_name + '.npy')
            with open(file_address,'wb') as file:
                np.save(file,self.values)
                print(new_file_name + " saved as timeline successfully.")

    def load(self, file_name = None):
        if file_name is None:
            file_name = input('enter your timeline name')
        file_address = path.join('database/saved_sounds/' , file_name + '.npy')
        if not file_name:
            print("didn't load.")
        else:
            with open(file_address,'rb') as file:
                self.values += np.load(file)
                print(file_name + " loaded as timeline successfually.")