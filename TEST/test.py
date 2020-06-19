import face_recognition as fr
# image = face_recognition.load_image_file("kek.jpg")
# face_landmarks_list = face_recognition.face_landmarks(image)



# from PIL import Image
# import face_recognition

# Load the jpg file into a numpy array
#image = face_recognition.load_image_file("webcam_pics/16_06_2020_14_27_54_.png")

# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py
# face_locations = face_recognition.face_locations(image)

# print("I found {} face(s) in this photograph.".format(len(face_locations)))

# for face_location in face_locations:

#     # Print the location of each face in this image
#     top, right, bottom, left = face_location
#     print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

#     # You can access the actual face itself like this:
#     face_image = image[top:bottom, left:right]
#     pil_image = Image.fromarray(face_image)
#     pil_image.show()



# CODE TO DETEC FACES
# frame = capture_img(0)
# #frame = cv2.imread('kek.jpg')# img for testing
# grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #cv2.imshow('Image', grayscale_image) # TESTING
# #cv2.waitKey(0) # TESTING

# # Load the classifier and create a cascade object for face detection
# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

# detected_faces = face_cascade.detectMultiScale(grayscale_image, 1.2, 5)


# for (column, row, width, height) in detected_faces:
#     cv2.rectangle(
#         frame,
#         (column, row),
#         (column + width, row + height),
#         (0, 255, 0),
#         2
#     )

# cv2.imshow('RESULT', frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# img = 'daniel_lucia.png'
# #face = fr.load_image_file("faces/" + img)
# face = fr.load_image_file(img)
# encoding = fr.face_encodings(face)#[0]

# print(len(encoding))
# print(type(encoding))

matches = [True, True, True, False]

if matches.count(True) > 1:
    print("Success")

else: 
    print("No Matches")

