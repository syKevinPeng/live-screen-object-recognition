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
        image_h, image_w, _ = image.shape
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
        bbox = self.bbox_post_processing(boxes.numpy(), image_h,image_w)
        pred_bbox = (bbox, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0])
        # print("predicted boxes: \n", boxes.numpy())
        return pred_bbox

    def bbox_post_processing(self, bbox, image_h, image_w):
        bbox = bbox[0]
        new_bbox = np.zeros(bbox.shape)
        new_bbox[:,1] = bbox[:,0]* image_h
        new_bbox[:,0] = bbox[:,1]* image_w
        new_bbox[:,3] = bbox[:,2]* image_h
        new_bbox[:,2] = bbox[:,3]* image_w
        return new_bbox
