import os
import pickle
import socket
import traceback

import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

try:
    from multiprocessing import shared_memory
except:
    ...

from run import ts, self_check, _SOCKET_PATH, _SHM_IMG, _SHM_PRED


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
        # # for value in pred_bbox:
        # # # for key, value in pred_bbox.items():
        # #     print(value.shape)
        # #     boxes = value[:,0:4]
        # #     pred_conf = value[:,0:4]
        # #     # boxes = value[:, :, 0:4]
        # #     # pred_conf = value[:, :, 4:]
        # #     boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        # #         boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        # #         scores=tf.reshape(
        # #             pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        # #         max_output_size_per_class=50,
        # #         max_total_size=50,
        # #         iou_threshold=self.iou,
        # #         score_threshold=self.score
        # #     )
        # value = pred_bbox
        # # for key, value in pred_bbox.items():
        # # print(value.shape)
        # # boxes = value[:,0:4]
        # # pred_conf = value[:,0:4]
        # boxes = value[:, :, 0:4]
        # pred_conf = value[:, :, 4:]
        # boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        #     boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        #     scores=tf.reshape(
        #         pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        #     max_output_size_per_class=50,
        #     max_total_size=50,
        #     iou_threshold=self.iou,
        #     score_threshold=self.score
        # )
        # pred_bbox = (boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy())
        # print("predicted boxes: \n", boxes.numpy())
        return pred_bbox


class Server:
    def __init__(self):
        if os.path.exists(_SOCKET_PATH):
            os.remove(_SOCKET_PATH)

        self.skt = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.skt.bind(_SOCKET_PATH)
        self.skt.listen()

        self.shm_pred_buf = None

        self.yolo = YoloDetector()

        print()
        print(f'{ts()}: ===================================')
        print(f'{ts()}: Listening on {_SOCKET_PATH}')
        print(f'{ts()}: ===================================')
        print()

        self.start()

    def process(self, shape_dtype: tuple) -> bytes:
        print(f"{ts()}: Processing data begin ...")

        if self.shm_pred_buf is not None:
            try:
                self.shm_pred_buf.close()
                self.shm_pred_buf.unlink()
            except:
                traceback.print_exc()

        shm_img_buf = shared_memory.SharedMemory(_SHM_IMG)
        shm_img_np = np.ndarray(shape_dtype[0], dtype=shape_dtype[1], buffer=shm_img_buf.buf)

        pred = self.yolo.detect(shm_img_np)

        shm_img_buf.close()

        self.shm_pred_buf = shared_memory.SharedMemory(_SHM_PRED, create=True, size=pred.nbytes)
        shm_pred_np = np.ndarray(pred.shape, dtype=pred.dtype, buffer=self.shm_pred_buf.buf)
        shm_pred_np[:] = pred[:]

        print(f"{ts()}: Processing data done ...")
        return pickle.dumps((pred.shape, pred.dtype))

    def start(self):
        while ...:
            conn, addr = self.skt.accept()
            try:
                print(f"{ts()}: New connection!")
                while ...:
                    print(f"{ts()}: New request!")
                    next_conn = False
                    data = b''
                    while ...:
                        tmp = conn.recv(512)
                        data += tmp
                        try:
                            unpickled = pickle.loads(data)
                            print(f'{ts()}: Received {len(data)} bytes!')
                            break
                        except:
                            ...
                        if not tmp:
                            next_conn = True
                    if next_conn:
                        break
                    processed = self.process(unpickled)
                    print(f'{ts()}: Sending {len(processed)} bytes!')
                    conn.send(processed)
            except:
                traceback.print_exc()
            print(f'{ts()}: ===================================')


if __name__ == '__main__':
    self_check()
    Server()
