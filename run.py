import datetime
# from multiprocessing import Process, Queue
import pickle
import socket
# import time
import tkinter as tk

# import detector
import on_screen_overlay
import util

_SOCKET_PATH = '/tmp/yolo-server'


def ts():
    return datetime.datetime.now().isoformat()


def client(data: bytes) -> bytes:
    conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    conn.connect(_SOCKET_PATH)
    print(f'{ts()}: Connected to {_SOCKET_PATH}')
    with conn:
        print(f'{ts()}: Sending {len(data)} bytes')
        conn.sendall(data)
        data = b''
        while ...:
            tmp = conn.recv(40960)
            if tmp:
                data += tmp
            else:
                break
    return data
    # client.close()


# def application(bbox_queue,img_queue):
#     window = tk.Tk()
#     app = on_screen_overlay.FullScreen(window)
#     # app.queue_monitor()
#     window.bind("<Escape>", lambda x: window.destroy())
#
#     while ...:
#         image = util.capture_screen()
#         img_queue.put(image)
#         print("Imager Waiting...")
#         time.sleep(1)
#         bbox = bbox_queue.get()
#         print("bbox getting form pipe:\n", bbox[0])
#         app.clean_canvas()  # clean the bbox from previous frame
#         # app.draw_background(image)
#         app.draw_box((bbox), image)
#         window.update_idletasks()
#         window.update()


# def detect(bbox_queue, img_queue):
#     # initialize yolo
#     yolo = detector.YoloDetector()
#     i = 1
#     while ...:
#         # while img_queue.empty():
#         #     pass
#         img = img_queue.get()
#         print("image getting form pipe:\n", img.shape)
#         # if i%5==0: Image.fromarray(img).save(f'/tmp/detect-{time.time()}-{i:3}.jpg')
#         bbox = yolo.detect(img)
#         # i+=1
#         bbox_queue.put(bbox)
#         print("Detector Waiting...")
#         time.sleep(1)


# def application(bbox_queue, img_queue):
def application():
    window = tk.Tk()
    app = on_screen_overlay.FullScreen(window)
    # app.queue_monitor()
    window.bind("<Escape>", lambda x: window.destroy())

    while ...:
    # for _ in range(3):
        image = util.capture_screen()
        dumped = pickle.dumps(image)
        processed = client(dumped)
        bbox = pickle.loads(processed)
        # print(f"{ts()}: bbox getting form pipe:\n", bbox[0])
        app.clean_canvas()  # clean the bbox from previous frame
        # app.draw_background(image)
        app.draw_box(bbox, image)
        window.update_idletasks()
        window.update()


if __name__ == "__main__":
    # # create multiprocessing queue for passing bbox and captured screen image between child process
    # bbox_queue = Queue()
    # img_queue = Queue()
    # app_process = Process(target=application, args=(bbox_queue, img_queue,))
    # detect_process = Process(target=detect, args=(bbox_queue, img_queue,))
    #
    # app_process.start()
    # detect_process.start()
    #
    # app_process.join()
    # detect_process.terminate()  # once the app process stops, terminate detect process immediately
    # detect_process.join()

    application()
