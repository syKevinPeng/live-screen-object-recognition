import os
import pickle
import socket
import traceback
import numpy as np
from detectors import YoloDetector
from client import _SOCKET_PATH
from util import ts


class Server:
    def __init__(self):
        if os.path.exists(_SOCKET_PATH):
            os.remove(_SOCKET_PATH)

        self.skt = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.skt.bind(_SOCKET_PATH)
        self.skt.listen()

        self.yolo = YoloDetector()

        print()
        print(f'{ts()}: ===================================')
        print(f'{ts()}: Listening on {_SOCKET_PATH}')
        print(f'{ts()}: ===================================')
        print()

        self.start()

    def process(self, img_np: np.ndarray) -> bytes:
        print(f"{ts()}: Processing data begin ...")

        pred = self.yolo.detect(img_np)

        print(f"{ts()}: Processing data done ...")
        return pickle.dumps(pred)

    def start(self):
        while ...:
            conn, addr = self.skt.accept()
            try:
                with conn:
                    print(f"{ts()}: New connection!")
                    while ...:
                        print(f"{ts()}: New request!")
                        next_conn = False
                        data = b''
                        while ...:
                            conn.settimeout(10)
                            tmp = conn.recv(2097152)
                            data += tmp
                            try:
                                img_np = pickle.loads(data)
                                print(f'{ts()}: Received {len(data)} bytes!')
                                break
                            except:
                                ...
                            if not tmp:
                                next_conn = True
                            if next_conn:
                                break
                        if next_conn:
                            break
                        processed = self.process(img_np)
                        print(f'{ts()}: Sending {len(processed)} bytes!')
                        conn.sendall(processed)
            except:
                traceback.print_exc()
            print(f'{ts()}: ===================================')


if __name__ == '__main__':
    Server()
