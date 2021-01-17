import on_screen_overlay
import util
import tkinter as tk
from multiprocessing import Process, Queue
import detector
import time

def application(bbox_queue,img_queue):
    window = tk.Tk()
    app = on_screen_overlay.FullScreen(window)
    # app.queue_monitor()
    window.bind("<Escape>", lambda x: window.destroy())
    while ...:
        image = util.capture_screen()
        img_queue.put(image)

        # when detect process is detecting, wait
        while bbox_queue.empty():
            time.sleep(0.1)
        bbox = bbox_queue.get()
        app.clean_canvas() # clean the bbox from previous frame
        app.draw_background(image)
        app.draw_box(bbox, image)
        window.update_idletasks()
        window.update()

def detect(bbox_queue,img_queue):
    # initialize yolo
    yolo = detector.YoloDetector()
    while ...:
        while img_queue.empty():
            pass
        img = img_queue.get()
        bbox = yolo.detect(img)
        bbox_queue.put(bbox)



if __name__ == "__main__":
    # create multiprocessing queue for passing bbox and captured screen image between child process
    bbox_queue = Queue()
    img_queue = Queue()
    app_process = Process(target= application, args=(bbox_queue,img_queue,))
    detect_process = Process(target= detect, args=(bbox_queue,img_queue,))

    app_process.start()
    detect_process.start()

    app_process.join()
    detect_process.terminate() # once the app process stops, terminate detect process immediately
    detect_process.join()