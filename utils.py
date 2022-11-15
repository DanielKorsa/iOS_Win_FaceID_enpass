""" Handmade FaceID -> MacOS + Enpass Password Manager"""

# TODO Add Makefile
# TODO Add unitests

import time
import psutil
import pyautogui as pag




def enapss_insert_pass_img_rec(password):
    """[This is a more complicated way of unlocking Enpass.
    Find text field and button by recognizing template imgs]

    Args:
        password ([str]): [Enpass Master password]
    """
    # Get coordinates of "Passford text input field"
    for i in range(3):
        psw_txt_field_coords = pag.locateCenterOnScreen('TEST/text_field.png') # must be .png
        if psw_txt_field_coords is None:
            print(f"Try {i}")
        else:
            break
    # Get coordinates of textfield
    x_psw, y_psw = psw_txt_field_coords
    pag.leftClick(x_psw/2, y_psw/2)
    pag.typewrite(password) # Write pass in text field
    # Get coordinate os "Unlock" button
    unlock_btn_coords = pag.locateCenterOnScreen('TEST/unlock_button.png')
    x_btn, y_btn = unlock_btn_coords
    pag.leftClick(x_btn/2, y_btn/2) # Click button


def enapss_insert_pass_easy(password):
    """[This is a fast and easy way of entering the password and pressing a button.
    Assuming that Enpass browser extension is open and is waiting for input

    Args:
        password ([str]): [Enpass Master password]
    """

    pag.write(password) # enter pass
    time.sleep(0.5)
    pag.press('enter') # press "Unlock" button


def proces_running(process_name:str) -> bool:
    """Check if browser & Enpass processes are running.
        Process name: Chrome / Mozilla
    """
    for proc in psutil.process_iter():
        if process_name in proc.name().lower():
            return True

    print(f"{process_name} is not running")
    return False

def get_pass():
    """[IMPORTANT: This is just an example. Dont use this way for storing passwords.]

    Returns:
        [str]: [Enpass master password]
    """
    #! Replace with ENV Variable
    path = "trash/delete.txt"
    with open(path, "r") as file:
        password = file.read()

    return password





