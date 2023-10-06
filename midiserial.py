import serial

class MidiSerial:
    def __init__(self, port, notePlayer):
        self.port = port
        self. notePlayer = notePlayer
        
    def start(self):
        with serial.Serial(self.port, 31250) as ser:
            while True:
                s = ser.read()
                if int.from_bytes(s, "big") == 0x90:
                    # start midi command
                    
                    note_byte = ser.read() 
                    vel_byte = ser.read() 

                    index = int.from_bytes(note_byte, "big")
                    vel = int.from_bytes(vel_byte, "big")

                    index = index - 21
                    if index == 0:
                        break

                    vel = ((2**(vel/10)-1024)*(1-0.02)/1023.7+1)
                    # vel *= (30/((index+1)*(index+1)/25))
                    
                    self.notePlayer.startNote(index,vel*0.5)

                elif int.from_bytes(s, "big") == 0x80:
                    # stop midi command
                    
                    note = ser.read() 
                    idk_yet_byte = ser.read() 
  
                    index = int.from_bytes(note, "big")
                    idk_yet = int.from_bytes(idk_yet_byte, "big")

                    index = index - 21

                    self.notePlayer.stopNote(index)