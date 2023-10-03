from tone import ADSRTone

class NotePlayer():
    def __init__(self, scaling, harmonic_maker, timeline):
        self.scaling = scaling
        self.harmonic_maker = harmonic_maker
        self.timeline = timeline
        self.tones = dict()
    def startNote(self, index = 1, velocity = 1):
        try:
            tone = self.tones.get(index, None)
            if tone is None:
                fundamental = self.scaling(index)
                tone = ADSRTone(fundamental, self.harmonic_maker(),volume=velocity)
                self.timeline.add_tone(tone)
                self.tones[index]=tone
        except AttributeError:
            pass
    def stopNote(self, index = 1):
        try:
            tone = self.tones.get(index, None)
            if tone is not None:
                self.timeline.remove_tone(tone)
                self.tones.pop(index)
        except AttributeError:
            pass