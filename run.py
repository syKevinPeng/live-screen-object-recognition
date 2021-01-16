import on_screen_overlay
import util
import tkinter as tk
from multiprocessing import Process, Queue
import time

def application():
    window = tk.Tk()
    window.wait_visibility(window)
    window.wm_attributes("-alpha", 0.4)
    app = on_screen_overlay.FullScreen(window)
    window.bind("<Escape>", lambda x: window.destroy())
    window.mainloop()

def capture_and_detect():
    while (True):
        pred_bbox = util.capture_screen()
        print(pred_bbox)
        time.sleep(5)

if __name__ == "__main__":
    app_process = Process(target= application)
    detect_process = Process(target= capture_and_detect)

    app_process.start()
    detect_process.start()

    app_process.join()
    detect_process.terminate()
    detect_process.join()