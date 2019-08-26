import cv2
import sys
import os



# Get user supplied values

cascPath = "./haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

W = 1000.

preview_W = 100

def DetectNumOfFace(imagePath):

    # Read the image
    image = cv2.imread(imagePath)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #, flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    num_of_face = len(faces)
    #limit 5 persons in one phc
    if num_of_face > 5:
        num_of_face = 5


    return num_of_face


def ResizeAndSave(imagePath, newSavePath):

    # Read the image
    image = cv2.imread(imagePath)

    image = cv2.imread(imagePath)
    height, width, depth = image.shape
    imgScale = W/width
    newX,newY = image.shape[1]*imgScale, image.shape[0]*imgScale
    newimg = cv2.resize(image,(int(newX),int(newY)))

    cv2.imwrite(newSavePath,newimg)


def ResizeAndSavePreview(imagePath, newSavePath):

    # Read the image
    image = cv2.imread(imagePath)

    image = cv2.imread(imagePath)
    height, width, depth = image.shape
    imgScale = preview_W/width
    newX,newY = image.shape[1]*imgScale, image.shape[0]*imgScale
    newimg = cv2.resize(image,(int(newX),int(newY)))

    cv2.imwrite(newSavePath,newimg)
