import datetime
import pickle
import socket
import sys
import time
import tkinter as tk

import numpy as np
import tensorflow as tf

import on_screen_overlay
import util


_IOU = 0.5
_SCORE = 0.25
_SOCKET_PATH = '/tmp/yolo-server'


def ts():
    return datetime.datetime.now().isoformat()


class Client:
    def __init__(self):
        self.conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.conn.connect(_SOCKET_PATH)
        print(f'{ts()}: Connected to {_SOCKET_PATH}')

        self.last_time = time.time_ns()

        self.window = tk.Tk()
        self.app = on_screen_overlay.FullScreen(self.window)
        self.window.bind("<Escape>", lambda x: self.window.destroy())

        self.start()
        self.window.destroy()

    def process_bbox(self, value):
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=_IOU,
            score_threshold=_SCORE
        )
        pred_bbox = (boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy())
        # print("predicted boxes: \n", boxes.numpy())
        return pred_bbox

    def client(self, image: np.ndarray):
        img_pkl = pickle.dumps(image)

        print(f'{ts()}: Sending {len(img_pkl)} bytes')
        self.conn.sendall(img_pkl)

        data = b''
        while ...:
            tmp = self.conn.recv(2097152)
            data += tmp
            try:
                unpickled = pickle.loads(data)
                print(f'{ts()}: Received {len(data)} bytes!')
                break
            except:
                ...

        bbox = self.process_bbox(unpickled)

        return bbox

    def start(self):
        while ...:
            image = util.capture_screen()
            bbox = self.client(image)
            # print(f"{ts()}: bbox getting form pipe:\n", bbox[0])
            self.app.clean_canvas()  # clean the bbox from previous frame
            # app.draw_background(image)
            self.app.draw_box(bbox, image)
            # self.app.draw_background(image)
            self.window.update_idletasks()
            self.window.update()

            t = time.time_ns()
            print(f'{ts()}: FPS: {1e9 / (t - self.last_time)}')
            self.last_time = t

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    Client()
