import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import util, pickle

class YoloDetector:
    def __init__(self, input_size=416, iou=0.5, score=0.25):
        self.weights = "./tensorflow-yolov4-tflite/checkpoints/yolov4-416/"  # path to yolo weights
        self.input_size = input_size
        self.iou = iou
        self.score = score
        # load model:
        self.model: keras.Model = keras.models.load_model(self.weights)

    def detect(self, image):

        image_data = cv2.resize(image, (self.input_size, self.input_size))
        image_data = np.asarray(image_data).astype(np.float32) / 255
        batch_data = tf.constant([image_data])

        prediction = self.model.predict(batch_data)

        boxes = prediction[:, :, 0:4]
        pred_conf = prediction[:, :, 4:]
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=self.iou,
            score_threshold=self.score
        )
        pred_bbox = (boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy())
        # print("predicted boxes: \n", boxes.numpy())
        return pred_bbox

