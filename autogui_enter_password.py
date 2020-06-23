#!.venv_enpass/bin/python
#Entering the password with pyautogui
"""
Script for Enpass
"""

import subprocess
import re
import pyautogui as pag
from pynput import keyboard
from main import main

def enapss_insert_pass_img_rec(password):
    """
    This is a more complicated way of unlocking Enpass.
    Find text field and button by recognizing template imgs
    """
    # Get coordinates of "Passford text input fiel"
    for i in range(3):
        psw_txt_field_coords = pag.locateCenterOnScreen('TEST/text_field.png') # must be .png
        if psw_txt_field_coords is None:
            print('Try {}'.format(i))
        else:
            break
        # if psw_txt_field_coords == None:
        #     print('Didnt find enpass window')

    x_psw, y_psw = psw_txt_field_coords
    pag.leftClick(x_psw/2, y_psw/2)
    pag.typewrite(password) # Write pass in text field
    # Get coordinate os "Unlock" button
    unlock_btn_coords = pag.locateCenterOnScreen('TEST/unlock_button.png')
    x_btn, y_btn = unlock_btn_coords
    pag.leftClick(x_btn/2, y_btn/2) # Click button

def enapss_insert_pass_easy(password):
    """
    This is a fast and easy way of entering the password and pressing a button.
    Assumin that Enpass browser extension is open and is waiting for input
    """

    pag.write(password) # enter pass
    pag.press('enter') # press "Unlock" button


def check_process(process_name):
    """
    Check if browser & Enpass processes are running
    """

    process = subprocess.Popen('pgrep ' + process_name,\
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    my_pid, err = process.communicate()
    msg = re.findall(r"\'(.*?)\'", str(my_pid))[0]
    if msg == '':

        print("{}  is not running".format(process_name))
        return False

    else:

        print("{} is running".format(process_name))
        return True

def get_pass():
    """
    This is just an example. Dont use this way for storing passwords.
    Find a secure solution.
    """
    path = "trash/delete.txt"
    with open(path, "r") as f:
        password = f.read()
    return password

# The key combination to check
COMBINATION = {keyboard.Key.cmd, keyboard.KeyCode.from_char('/')}

# The currently active modifiers
current = set()

def on_press(key):
    """
    Run code
    """
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            if check_process('firefox') and check_process('Enpass') is True:
                face_recognition, msg = main()
                print(face_recognition, msg)
                #time.sleep(1) # if the PC is slow delay is needed while opening enpass ext
                if face_recognition is True:
                    enapss_insert_pass_easy(get_pass()) #Getting master password

    if key == keyboard.Key.esc:
        listener.stop()


def on_release(key):
    """
    Waiting until user presses the key combination
    """
    try:
        current.remove(key)
    except KeyError:
        pass


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
