import base64
import numpy as np
import cv2
import tensorflow as tf

model = None
BASE_WIDTH = 28

def loadNetwork():
    global model
    model = tf.keras.models.load_model('trained-model/digit_prediction_model.h5')
    return model

def process_image(image):
    # image : encoded b64 string
    image = base64.b64decode(image)
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    image_compressed = cv2.resize(img_np, (BASE_WIDTH, BASE_WIDTH), interpolation=cv2.INTER_LINEAR)
    image_compressed = cv2.bitwise_not(image_compressed)
    image_compressed = image_compressed.reshape(1, 784)
    image_compressed = image_compressed.astype('float32')
    image_compressed = image_compressed/255.0
    image_compressed[image_compressed < 0.5] = 0.
    return image_compressed

def predict(image):
    image_array = process_image(image)
    predict_value = model.predict([image_array])[0]
    digit = np.argmax(predict_value)
    return str(digit)