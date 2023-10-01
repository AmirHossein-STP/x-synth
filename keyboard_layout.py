from os import path
from pynput import keyboard
from tone import ADSRTone

class KeyboardLayout:
    def __init__(self):
        self.value = list()
        self.tones = dict()

    def set():
        # reset keyboard layout
        temp_keyboard_layout = []
        def on_press(key):
            if key == keyboard.Key.esc:
                # Stop listener
                return False
            try:
                temp_keyboard_layout.append(key.char)
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

        new_file_name = input('enter your new keyboar layout name')
        if not new_file_name:
            print("didn't save.")
        else:
            file_address = path.join('database/keyboard_layouts/' , new_file_name + '.txt')
            with open(file_address,'w') as file:
                file.writelines(temp_keyboard_layout)
                print(new_file_name + " saved as keyboard layout successfully.")


    def load(self, file_name = None):
        # load saved keyboard layout
        if file_name is None:
            file_name = input('enter your keyboar layout name')
        file_address = path.join('database/keyboard_layouts/' , file_name + '.txt')
        if not file_name:
            print("didn't load.")
        else:
            with open(file_address,'r') as file:
                self.value = list(file.readlines()[0])
                print(file_name + " loaded as keyboard layout successfully.")

    def start(self, scaling, harmonics, timeline):
        # listen to keyboard
        self.harmonics = harmonics
        def on_press(key):
            try:
                index = self.value.index(key.char)

                tone = self.tones.get(index, None)
                if tone is None:
                    fundamental = scaling(index)
                    tone = ADSRTone(fundamental, self.harmonics)
                    timeline.add_tone(tone)
                    self.tones[index]=tone

            except AttributeError:
                pass
                # print('special key {0} pressed'.format(
                #     key))
                # return
            # position = audioplayer.position
            # tone = tonemaker.make(fundamental)/10
            # timeline.add(tone, position)

            
        def on_release(key):
            if key == keyboard.Key.esc:
                # Stop listener
                # audioplayer.stop()
                print("stoped.")
                timeline.tones = set()
                self.tones = dict()
                return False
            try:
                index = self.value.index(key.char)
                tone = self.tones.get(index, None)
                if tone is not None:
                    timeline.remove_tone(tone)
                    self.tones.pop(index)
            except AttributeError:
                pass
                # print('special key {0} pressed'.format(
                #     key))
                # return

        # Collect events until released
        # with keyboard.Listener(
        #         on_press=on_press,
        #         on_release=on_release) as listener:
        #     listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()
        print("started...")