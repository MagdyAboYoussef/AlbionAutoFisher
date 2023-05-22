import pyaudio
import pygetwindow as gw

def get_game_window(title):
    windows = gw.getWindowsWithTitle(title)
    if windows:
        return windows[0]
    else:
        raise Exception("Game window not found")
    




def indexOfSound():
    p = pyaudio.PyAudio()
    # List all audio devices
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if ("CABLE Output (VB-Audio Virtual " in dev['name']) and (dev['maxInputChannels'] == 8) and (dev['maxOutputChannels'] == 0):
            return i



