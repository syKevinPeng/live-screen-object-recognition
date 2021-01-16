import on_screen_overlay
import util
import tkinter as tk
from multiprocessing import Process, Queue
import colorsys, random
import time

def application(queue):
    window = tk.Tk()
    window.wait_visibility(window)
    window.wm_attributes("-alpha", 0.4)
    app = on_screen_overlay.FullScreen(window, queue)
    app.queue_monitor()
    window.bind("<Escape>", lambda x: window.destroy())
    window.mainloop()


def capture_and_detect(queue):
    while (True):
        if(queue.empty()):
            pred_bbox, image = util.capture_screen()
            queue.put([pred_bbox, image])
            print(queue)
        time.sleep(0.2)



if __name__ == "__main__":
    bbox_queue = Queue()
    app_process = Process(target= application, args=(bbox_queue,))
    detect_process = Process(target= capture_and_detect, args=(bbox_queue,))

    app_process.start()
    detect_process.start()

    app_process.join()
    detect_process.terminate()
    detect_process.join()