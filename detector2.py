import datetime
import os
import pickle
import socket
import sys

import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

_SOCKET_PATH = '/tmp/yolo-server'


def ts():
    return datetime.datetime.now().isoformat()


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
        # for value in pred_bbox:
        # # for key, value in pred_bbox.items():
        #     print(value.shape)
        #     boxes = value[:,0:4]
        #     pred_conf = value[:,0:4]
        #     # boxes = value[:, :, 0:4]
        #     # pred_conf = value[:, :, 4:]
        #     boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        #         boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        #         scores=tf.reshape(
        #             pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        #         max_output_size_per_class=50,
        #         max_total_size=50,
        #         iou_threshold=self.iou,
        #         score_threshold=self.score
        #     )
        value = pred_bbox
        # for key, value in pred_bbox.items():
        print(value.shape)
        # boxes = value[:,0:4]
        # pred_conf = value[:,0:4]
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
        pred_bbox = (boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy())
        print("predicted boxes: \n",boxes.numpy())
        return pred_bbox


class Server:
    def __init__(self):
        self.skt = None

        self.yolo = YoloDetector()
        self.init()
        self.start()

    def process(self, np_arr: np.ndarray) -> bytes:
        print(f"{ts()}: Processing data begin ...")
        # np_arr = pickle.loads(data)

        image = np_arr
        bbox = self.yolo.detect(image)
        result = bbox

        print(f"{ts()}: Processing data done ...")
        return pickle.dumps(result)

    def init(self):
        if os.path.exists(_SOCKET_PATH):
            os.remove(_SOCKET_PATH)

        self.skt = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.skt.bind(_SOCKET_PATH)
        self.skt.listen()
        print()
        print(f'{ts()}: ===================================')
        print(f'{ts()}: Listening on {_SOCKET_PATH}')
        print(f'{ts()}: ===================================')
        print()

    def start(self):
        while ...:
            conn, addr = self.skt.accept()
            try:
                with conn:
                    print(f"{ts()}: New connection!")
                    data = b''
                    while ...:
                        tmp = conn.recv(2097152)
                        data += tmp
                        try:
                            np_arr = pickle.loads(data)
                            print(f'{ts()}: Received {len(data)} bytes!')
                            break
                        except:
                            ...
                    processed = self.process(np_arr)
                    print(f'{ts()}: Sending {len(processed)} bytes!')
                    conn.send(processed)
            except Exception as e:
                print(f'Error: {e}', file=sys.stderr)
            print(f'{ts()}: ===================================')


if __name__ == '__main__':
    Server()
