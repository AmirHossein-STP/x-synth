from os import path
from pynput import keyboard
from threading import Timer
class KeyboardLayout:
    def __init__(self, notePlayer):
        self. notePlayer = notePlayer
        self.value = list()
        self.is_on = False

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

        new_file_name = input('enter your new keyboar layout name: ')
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
            file_name = input('enter your keyboar layout name: ')
        file_address = path.join('database/keyboard_layouts/' , file_name + '.txt')
        if not file_name:
            print("didn't load.")
        else:
            with open(file_address,'r') as file:
                self.value = list(file.readlines()[0])
                print(file_name + " loaded as keyboard layout successfully.")

    def start(self):
        # listen to keyboard
        self.is_on = True
        def on_press(key):
            try:
                index = self.value.index(key.char)
                print("start ",index)
                # self.notePlayer.startNote(index)

                self.notePlayer.single_hit(index)
                def second_note():
                    self.notePlayer.single_hit(index+7)
                def third_note():
                    self.notePlayer.single_hit(index+14)
                t1 = Timer(0.3,second_note)
                t1.start()
                t2 = Timer(0.6,third_note)
                t2.start()
                
            except AttributeError:
                pass

            
        def on_release(key):
            if key == keyboard.Key.esc:
                # Stop listener
                # audioplayer.stop()
                print("stoped.")
                self.is_on = False
                # timeline.tones = set()
                # self.tones = dict()
                return False
            try:
                index = self.value.index(key.char)
                print("stop ",index)
                # self.notePlayer.stopNote(index)
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