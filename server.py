import os
import pickle
import socket
import traceback

import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from detectors import YoloDetector

try:
    from multiprocessing import shared_memory
except:
    ...

from run import ts, self_check, _SOCKET_PATH, _SHM_IMG, _SHM_PRED



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
        del shm_img_buf, shm_img_np

        if pred.nbytes == 0:
            print(f'{ts()}: pred.nbytes is {pred.nbytes}!')
            print(f'{ts()}: pred.shape  is {pred.shape}!')

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
                        conn.settimeout(10)
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
