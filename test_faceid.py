#!.venv_enpass/bin/python
"""
FaceID Recognition for Enpass Password Manager on MacOS
"""
import os
import subprocess
import re
from pathlib import Path
from datetime import datetime
import cv2
import face_recognition as fr
import numpy as np
from numpy import array
import pyautogui as pag
from pynput import keyboard

#Get a webcam pic

def capture_img(camera, testmode):
    """
    Get an image from webcam 0 - internal, 1 - external
    :return: captured img and img path
    """

    capture = cv2.VideoCapture(camera) # 0 - use built in camera
    return_value, image = capture.read() #! add [1]
    del capture
    if testmode == 1:
        # For test purposes -> save pic
        webcam_pics_dir = str(Path.cwd() / "webcam_pics")
        now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_")
        pic_path = webcam_pics_dir + "/" + now + '.jpg'
        cv2.imwrite(pic_path, image) # Save webcam pic
    else:
        pic_path = ''

    return image, pic_path

capture_img(0, 1)