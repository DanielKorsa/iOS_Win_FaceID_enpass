import cv2
import face_recognition as fr
import os
from pathlib import Path
import time
from datetime import datetime
import numpy as np
from numpy import array


# 1. Get a webcam pic

def capture_img(camera, testmode):
    """
    Get an image from webcam 0 - internal, 1 - external
    """

    capture = cv2.VideoCapture(camera) # 0 - use built in camera
    return_value, image = capture.read()
    del(capture)
    
    if testmode == 1:
        # For test purposes -> save pic
        webcam_pics_dir = str(Path.cwd() / "webcam_pics")
        now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_")
        pic_path = webcam_pics_dir + "/" + now + '.jpg'
        cv2.imwrite(pic_path, image) # Save webcam pic
    else:
        pic_path = ''

    return image, pic_path

# 2. Encode single face

def encode_face_img(img):
    """
    Encode a face on an img
    """
    #face = fr.load_image_file("faces/" + img)
    face = fr.load_image_file(img)
    encoding = fr.face_encodings(face)[0]

    return encoding

def pre_encode_user_faces():
    """
    Encodes given user sample faces and stores it

    :return: dict of (name, image encoded)
    """

    if os.path.exists("encoded_user_faces.txt") == True:
        # If file with preencoded images exists -> read it

        with open("encoded_user_faces.txt", 'r') as f: 
            content = f.read()
            encoded = eval(content) 
    else:
        # First use -> create fie with preencoded imgs
        encoded = {}
        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png"):
                    encoding = encode_face_img("faces/" + f)
                    encoded[f.split(".")[0]] = encoding
        
        #Save results as txt
        with open('encoded_user_faces.txt', 'w') as f:
            print(encoded, file=f)

    return encoded

def classify_face(webcam_pic, preencoded_imgs, testmode):
    """
    Compares webcam face against user predefined facial pics

    :param im: webcam image, preencoded user defined images
    :return: True if webcam pic matches predifined user face
    """

    faces_preencoded = list(preencoded_imgs.values())
    face_locations = fr.face_locations(webcam_pic) # Get faces locations on webcam pic
    webcam_face_encoding = fr.face_encodings(webcam_pic, face_locations)
    
    if len(webcam_face_encoding) == 0:
        msg = 'No Faces on the Img'
        result = False
    
    else:

        matches = fr.compare_faces(faces_preencoded, webcam_face_encoding[0])

        # Can be tweaked -> check if webcam face is recognized more then on 1 pic
        if matches.count(True) > 1:
            msg = "Success"
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
                        cv2.rectangle(webcam_pic, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

                        # Draw a label with a name below the face
                        cv2.rectangle(webcam_pic, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(webcam_pic, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)

                # Display the resulting image
                while True:

                    cv2.imshow('Video', webcam_pic)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        return face_names

        else: 
            msg = "No Matches Found"
            result = False
        
    return result, msg





def main():

    testmode = 0
    webcam_pic, pic_path = capture_img(0, testmode)
    #encd_temp_pic = encode_face_img(temp_pic)
    preencoded_imgs = pre_encode_user_faces()
    faceid_result = classify_face(webcam_pic, preencoded_imgs, testmode)
    print(faceid_result)



if __name__ == "__main__":
    main()