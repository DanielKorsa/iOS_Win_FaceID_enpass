#!.venv_enpass/bin/python

# FaceID Recognition for Enpass Password Manager on MacOS

import os
import time
import subprocess
import re
from pathlib import Path
from datetime import datetime

import cv2
import face_recognition as fr
from numpy import array
import numpy as np
import pyautogui as pag
from pynput import keyboard


def capture_img(camera, testmode):
    """[Capture an img with a webcam]

    Args:
        camera ([int]): [0 - internal, 1 - external]
        testmode ([int]): [0 - dont save img, 1 - save img locally]

    Returns:
        [str: [Captured image]
    """

    capture = cv2.VideoCapture(camera) # 0 - use built in camera
    image = capture.read()[1]
    del capture # delete captured img
    if testmode == 1:
        # Save img locally in folder
        webcam_pics_dir = str(Path.cwd() / "webcam_pics")
        if not os.path.exists(webcam_pics_dir):
            os.makedirs(webcam_pics_dir) # Create a dir if doesnt exist

        now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_")
        pic_path = webcam_pics_dir + "/" + now + '.jpg'
        cv2.imwrite(pic_path, image) # Save webcam pic

    return image

def encode_face_img(img):
    """[Encode face on the img]

    Args:
        img ([str]): [Image]

    Returns:
        [numpy.ndarray]: [Encoded face numpy array]
    """
    face = fr.load_image_file(img)
    encoding = fr.face_encodings(face)[0]

    return encoding

def pre_encode_user_faces():
    """[Encodes given user sample faces and stores it in txt file]

    Returns:
        [dict]: [(file name, image encoded)]
    """

    if os.path.exists("encoded_user_faces.txt"):
        # If file with pre-encoded images exists -> read it
        with open("encoded_user_faces.txt", 'r') as f:
            content = f.read()
            encoded = eval(content)
    else:
        # First use -> create fie with preencoded imgs
        #! IMPORTANT: Put .jpg or .png images with your face in "faces" folder
        encoded = {}
        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png"):
                    encoding = encode_face_img("faces/" + f)
                    encoded[f.split(".")[0]] = encoding

        #Save results as .txt file
        with open('encoded_user_faces.txt', 'w') as f:
            print(encoded, file=f)

    return encoded

def classify_face(webcam_pic, preencoded_imgs, testmode):
    """[Compare webcam face against user predefined facial pics]

    Args:
        webcam_pic ([str]): [Web cam img]
        preencoded_imgs ([type]): [description]
        testmode ([int]): [1 - show the best face match, 0 - skip ]

    Returns:
        [bool]: [1 - face recognized , 0 - face not recognized]
    """

    faces_preencoded = list(preencoded_imgs.values())
    face_locations = fr.face_locations(webcam_pic) # Get faces locations on webcam pic
    webcam_face_encoding = fr.face_encodings(webcam_pic, face_locations)

    if len(webcam_face_encoding) == 0:
        result = False

    else:
        matches = fr.compare_faces(faces_preencoded, webcam_face_encoding[0])

        #! Set a trashhold here: if more than 1 match -> face identified
        if matches.count(True) > 1:
            result = True

            if testmode == 1: # Show which face matching the best

                face_names = []
                known_face_names = list(preencoded_imgs.keys())
                for face_encoding in webcam_face_encoding:

                    # See if the face is a match for the known face(s)
                    matches = fr.compare_faces(faces_preencoded, face_encoding)
                    name = "Unknown"
                    # use the known face with the smallest distance to the new face
                    face_distances = fr.face_distance(faces_preencoded, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        # Draw a box around the face
                        cv2.rectangle(webcam_pic, (left-20, top-20),\
                        (right+20, bottom+20), (255, 0, 0), 2)

                        # Draw a label with a name below the face
                        cv2.rectangle(webcam_pic, (left-20, bottom -15), (right+20, bottom+20),\
                        (255, 0, 0), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(webcam_pic, name, (left -20, bottom + 15),\
                        font, 1.0, (255, 255, 255), 2)

                # Display the resulting image
                while True:

                    cv2.imshow('Video', webcam_pic)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        return face_names

        else:
            result = False

    return result

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
            print('Try {}'.format(i))
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


def check_process(process_name):
    """[Check if browser & Enpass processes are running]

    Args:
        process_name ([str]): [Process name: Chrome / Mozilla]

    Returns:
        [bool]: [1 - process is running, 0 - not running]
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
    """[IMPORTANT: This is just an example. Dont use this way for storing passwords.]

    Returns:
        [str]: [Enpass master password]
    """

    path = "trash/delete.txt"
    with open(path, "r") as f:
        password = f.read()

    return password


# # The currently active modifiers
# current = set()

def on_press(key):
    """
    Execute code on key combination
    Key combination: "command" + "/"
    """

    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            if check_process('firefox') and check_process('Enpass'):
                webcam_pic = capture_img(0, TESTMODE) # Capture webcam img
                preencoded_imgs = pre_encode_user_faces() # Get preencoded imgs
                faceid_result = classify_face(webcam_pic, preencoded_imgs, TESTMODE)
                #time.sleep(1) # if the PC is slow delay is needed while opening enpass ext
                if faceid_result:
                    enapss_insert_pass_easy(get_pass()) #Getting master password
                    print('Face recognized')
                else:
                    print('Face not recognized')

def on_release(key):
    """
    Waiting until user presses the key combination
    """
    try:
        current.remove(key)
    except KeyError:
        pass

# For testing some feaures
TESTMODE = 0
# The key combination to check for opening Enpass in Firefox
COMBINATION = {keyboard.Key.cmd, keyboard.KeyCode.from_char('/')}
# The currently active modifiers
current = set()

def main():
    """
    Main - start the keyboard listener
    """

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
