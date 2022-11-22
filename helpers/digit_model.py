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

model = None
BASE_WIDTH = 28

def loadNetwork():
    global model
    model = tf.keras.models.load_model('https://storage.googleapis.com/smooth-helper-360323_cloudbuild/first_mod.h5')
    return model

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

    gray = cv2.resize(255-gray, (28,28), interpolation=cv2.INTER_LINEAR)
    (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    while np.sum(gray[0]) == 0:
      gray = gray[1:]

    while np.sum(gray[:,0]) == 0:
      gray = np.delete(gray,0,1)

    while np.sum(gray[-1]) == 0:
      gray = gray[:-1]

    while np.sum(gray[:,-1]) == 0:
      gray = np.delete(gray,-1,1)

    rows,cols = gray.shape

    if rows > cols:
      factor = 20.0/rows
      rows = 20
      cols = int(round(cols*factor))
      gray = cv2.resize(gray, (cols,rows))
    else:
      factor = 20.0/cols
      cols = 20
      rows = int(round(rows*factor))
      gray = cv2.resize(gray, (cols, rows))
    
    colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
    rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
    gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')
    shiftx,shifty = getBestShift(gray)
    shifted = shift(gray,shiftx,shifty)
    gray = shifted

    # plt.imshow(gray)
    gray = gray.reshape(1,28,28,1)
    return gray/255.0

def predict(image):
    image_array = process_image(image)
    predict_value = model.predict([image_array])[0]
    digit = np.argmax(predict_value)
    return str(digit)