import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

class YoloDetector:
    def __init__(self, input_size=416, iou=0.5, score=0.25):
        # if weights:
        #     self.weights = weights
        # else :
        self.weights = "./tensorflow-yolov4-tflite/checkpoints/yolov4-416/"  # path to yolo weights
        self.input_size = input_size
        self.iou = iou
        self.score = score
        # load model:
        self.model: keras.Model = keras.models.load_model(self.weights)

    def detect(self, image):
        # self.saved_model_loaded = saved_model.load(self.weights, tags=[saved_model.tag_constants.SERVING])
        # self.infer = self.saved_model_loaded.signatures['serving_default']
        # infer = saved_model_loaded.signatures['serving_default']

        image_data = cv2.resize(image, (self.input_size, self.input_size))
        image_data = np.asarray(image_data).astype(np.float32) / 255
        batch_data = tf.constant([image_data])

        pred_bbox = self.model.predict(batch_data)

        return pred_bbox
