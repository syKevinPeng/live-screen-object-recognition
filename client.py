import pickle
import socket
import time
import tkinter as tk
import numpy as np
import on_screen_overlay
import util

_SOCKET_PATH = '/tmp/yolo-server'
_IOU = 0.5
_SCORE = 0.25


class Client:
    def __init__(self):
        self.conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.conn.connect(_SOCKET_PATH)
        print(f'{util.ts()}: Connected to {_SOCKET_PATH}')

        self.last_time = time.time_ns()

        self.window = tk.Tk()
        self.app = on_screen_overlay.FullScreen(self.window)
        self.window.bind("<Escape>", lambda x: self.window.destroy())

        self.start()
        self.window.destroy()

    def client(self, image: np.ndarray):
        img_pkl = pickle.dumps(image)

        print(f'{util.ts()}: Sending {len(img_pkl)} bytes')
        self.conn.sendall(img_pkl)

        data = b''
        while ...:
            tmp = self.conn.recv(2097152)
            data += tmp
            try:
                unpickled = pickle.loads(data)
                print(f'{util.ts()}: Received {len(data)} bytes!')
                break
            except:
                ...

        return unpickled

    def start(self):
        while ...:
            image = util.capture_screen()
            bbox = self.client(image)
            # print(f"{ts()}: bbox getting form pipe:\n", bbox[0])
            self.app.clean_canvas()  # clean the bbox from previous frame
            self.app.draw_background(image)
            self.app.draw_box(bbox, image)

            self.window.update_idletasks()
            self.window.update()


            t = time.time_ns()
            print(f'{util.ts()}: FPS: {1e9 / (t - self.last_time)}')
            self.last_time = t

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    Client()
