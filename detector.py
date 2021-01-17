import numpy as np
import cv2,util, colorsys, random
import tensorflow as tf
from tensorflow.python import saved_model


class YoloDetector():
    def __init__(self, input_size = 416, iou = 0.5, score = 0.25 ):
        # if weights:
        #     self.weights = weights
        # else :
        self.weights = "./tensorflow-yolov4-tflite/checkpoints/yolov4-416/" # path to yolo weights
        self.input_size = input_size
        self.iou = iou
        self.score = score
        # load model:
        self.saved_model_loaded = saved_model.load(self.weights, tags=[saved_model.tag_constants.SERVING])
        # # self.infer = saved_model_loaded.signatures['serving_default']
        # classes = util.read_class_names("./tensorflow-yolov4-tflite/data/classes/coco.names")
        # self.num_classes = len(classes)
        # hsv_tuples = [(1.0 * x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
        # colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        # colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
        # random.seed(0)
        # random.shuffle(colors)
        # random.seed(None)
        # self.colors = colors

    def detect(self, image):
        image_data = cv2.resize(image, (self.input_size, self.input_size))
        image_data = np.asarray(image_data / 255).astype(np.float32)
        batch_data = tf.constant([image_data])
        infer = self.saved_model_loaded.signatures['serving_default']
        pred_bbox = infer(batch_data)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]
            boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
                boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
                scores=tf.reshape(
                    pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                max_output_size_per_class=50,
                max_total_size=50,
                iou_threshold=self.iou,
                score_threshold=self.score
            )



        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        return pred_bbox