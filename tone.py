import numpy as np

class Tone:
    # make tone

    def __init__(self, harmonics, duration = 0.2, fade_duration = 0.002, smplRate = 44100):
        self.smplRate = smplRate
        t0 = .0
        t = np.array( range( int(t0*self.smplRate) , int((t0+duration)*self.smplRate) ) , dtype="float") / self.smplRate
        self.t2p = t * 2 * np.pi
        self.fade_duration = fade_duration
        self.harmonics = harmonics

    @property
    def fade_duration(self):
        return self._fade_duration
    
    @fade_duration.setter
    def fade_duration(self, value):
        self._fade_duration= value
        self.fade_size = int(self.smplRate*value)
        self.fade_in = np.linspace(0, 1, self.fade_size, dtype=np.float32)
        self.fade_out = np.linspace(1, 0, self.fade_size, dtype=np.float32)

    def make(self, fundamental):
        ft2p = fundamental * self.t2p
        sound = np.sin(ft2p)
        for harmonic in self.harmonics:
            harmonic_ratios = harmonic[0]
            harmonic_ratios_level = harmonic[1]
            sound += np.sin(ft2p * harmonic_ratios)/harmonic_ratios_level
        sound[:self.fade_size] *= self.fade_in
        sound[-self.fade_size:] *= self.fade_out
        return sound
        # return sound/10