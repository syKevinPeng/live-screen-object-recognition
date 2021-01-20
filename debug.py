import on_screen_overlay
import util
import tkinter as tk
from multiprocessing import Process, Queue
import detector
import time
from PIL import Image
import copy

def application(bbox_queue,img_queue):
    window = tk.Tk()
    app = on_screen_overlay.FullScreen(window)
    # app.queue_monitor()
    window.bind("<Escape>", lambda x: window.destroy())

    yolo = detector.YoloDetector()
    i=1



    while ...:
        image = util.capture_screen()
        #time.sleep(5)
        #img_queue.put(image)
        #img = img_queue.get()
        bbox = yolo.detect(image)
        # bbox_queue.put(bbox)
        # bbox = bbox_queue.get()
        #print("bbox getting form pipe:\n", bbox[0])
        # app.clean_canvas()  # clean the bbox from previous frame
        # # app.draw_background(image)
        # app.draw_box((bbox), image)
        # window.update_idletasks()
        # window.update()



if __name__ == "__main__":
    # create multiprocessing queue for passing bbox and captured screen image between child process
    bbox_queue = Queue()
    img_queue = Queue()
    app_process = Process(target= application, args=(bbox_queue,img_queue,))
    # detect_process = Process(target= detect, args=(bbox_queue,img_queue,))

    app_process.start()
    #detect_process.start()

    app_process.join()
    #detect_process.terminate() # once the app process stops, terminate detect process immediately
    #detect_process.join()