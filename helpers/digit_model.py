import base64
import numpy as np
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib import cm
import base64
from io import BytesIO
import math
from scipy import ndimage

top_left_model = None
top_right_model = None
bottom_right_model = None
bottom_left_model = None
BASE_WIDTH = 14

def loadNetwork():
    global top_left_model, top_right_model, bottom_left_model, bottom_right_model, model
    top_left_model = tf.keras.models.load_model('trained-model/top_left.h5')
    bottom_left_model = tf.keras.models.load_model('trained-model/bottom_left.h5')
    top_right_model = tf.keras.models.load_model('trained-model/top_right.h5')
    bottom_right_model = tf.keras.models.load_model('trained-model/bottom_right.h5')
    return top_left_model, bottom_left_model, top_right_model, bottom_right_model

def getBestShift(img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty

def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted

def process_image(image):
    # image : encoded b64 string
    image = base64.b64decode(image)
    nparr = np.fromstring(image, np.uint8)
    gray = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    gray = cv2.resize(255-gray, (14,14), interpolation=cv2.INTER_LINEAR)
    (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # while np.sum(gray[0]) == 0:
    #   gray = gray[1:]

    # while np.sum(gray[:,0]) == 0:
    #   gray = np.delete(gray,0,1)

    # while np.sum(gray[-1]) == 0:
    #   gray = gray[:-1]

    # while np.sum(gray[:,-1]) == 0:
    #   gray = np.delete(gray,-1,1)

    # rows,cols = gray.shape

    # if rows > cols:
    #   factor = 20.0/rows
    #   rows = 20
    #   cols = int(round(cols*factor))
    #   gray = cv2.resize(gray, (cols,rows))
    # else:
    #   factor = 20.0/cols
    #   cols = 20
    #   rows = int(round(rows*factor))
    #   gray = cv2.resize(gray, (cols, rows))
    
    # colsPadding = (int(math.ceil((14-cols)/2.0)),int(math.floor((14-cols)/2.0)))
    # rowsPadding = (int(math.ceil((14-rows)/2.0)),int(math.floor((14-rows)/2.0)))
    # gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')
    # shiftx,shifty = getBestShift(gray)
    # shifted = shift(gray,shiftx,shifty)
    # gray = shifted

    # # plt.imshow(gray)
    gray = gray.reshape(1,14,14,1)
    return gray/255.0

def predict(image):
    image_array = process_image(image)
    predict_value = model.predict([image_array])[0]
    digit = np.argmax(predict_value)
    return str(digit)


def predictTopLeft(image):
    image_array = process_image(image)
    predict_value = top_left_model.predict([image_array.reshape(1, 196)])[0]
    digit = np.argmax(predict_value)
    return str(digit)

def predictTopRight(image):
    image_array = process_image(image)
    predict_value = top_right_model.predict([image_array.reshape(1, 196)])[0]
    digit = np.argmax(predict_value)
    return str(digit)

def predictBottomLeft(image):
    image_array = process_image(image)
    predict_value = bottom_left_model.predict([image_array.reshape(1, 196)])[0]
    digit = np.argmax(predict_value)
    return str(digit)

def predictBottomRight(image):
    image_array = process_image(image)
    predict_value = bottom_right_model.predict([image_array.reshape(1, 196)])[0]
    digit = np.argmax(predict_value)
    return str(digit)