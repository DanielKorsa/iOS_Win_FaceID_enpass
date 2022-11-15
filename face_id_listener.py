""" Handmade FaceID -> MacOS + Enpass Password Manager"""
from pynput import keyboard
from recognize_face import face_recognized

# The key combination to check for opening Enpass in Firefox.
COMBINATION = {keyboard.Key.cmd, keyboard.KeyCode.from_char('/')}
TESTMODE = 0

def on_press(key:dict):
    """
    Execute code on key combination
    """
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            if face_recognized():
                print('Face recognized')


def on_release(key:dict):
    """
    Waiting until user presses the key combination
    """
    try:
        current.remove(key)
    except KeyError:
        pass


def faceid_listener():
    """
    Main - start the keyboard listener
    """

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    current = set()
    faceid_listener()
