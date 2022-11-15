""" Face recognition"""

import os
from datetime import datetime
from pathlib import Path

import cv2
import face_recognition as fr
import numpy as np


def capture_img(camera, testmode=False):
    """[Capture an img with a webcam]

    Args:
        camera ([int]): [0 - internal, 1 - external]
        testmode ([bool]): [False - dont save img, True - save img locally]

    Returns:
        [str: [Captured image]
    """

    capture = cv2.VideoCapture(camera)
    image = capture.read()[1]
    del capture
    if testmode:
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
        with open("encoded_user_faces.txt", 'r') as file:
            content = file.read()
            encoded = eval(content)
    else:
        # First use -> create fie with preencoded imgs
        #! IMPORTANT: Put .jpg or .png images with your face in "faces" folder
        encoded = {}
        for dirpath, dnames, fnames in os.walk("./faces"):
            for filename in fnames:
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    encoding = encode_face_img("faces/" + filename)
                    encoded[filename.split(".")[0]] = encoding

        # TODO add long cache?
        with open('encoded_user_faces.txt', 'w') as file:
            print(encoded, file=file)

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

def face_recognized():
    """ """
    return True