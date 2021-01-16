import tkinter as tk
from tkinter import Canvas
import numpy as np
import cv2, time
import tensorflow as tf
from tensorflow.python import saved_model
import detector

class FullScreen(object):
    def __init__(self, master, queue, **kwargs):
        self.master=master
        self.queue = queue
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth(), master.winfo_screenheight()))

    def draw_box(self, bbox, image):
        out_boxes, out_scores, out_classes, num_boxes = bbox
        image_h, image_w, _ = image.shape
        canvas = Canvas(self.master)
        canvas.pack()
        for i in range(num_boxes[0]):
            if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > self.num_classes: continue
            coord = out_boxes[0][i]
            coord[0] = int(coord[0] * image_h)
            coord[2] = int(coord[2] * image_h)
            coord[1] = int(coord[1] * image_w)
            coord[3] = int(coord[3] * image_w)
            canvas.create_rectangle([coord[0],coord[1],coord[2],coord[3]], width=2, outline = 'black')

    def queue_monitor(self):
        while(True):
            if(not self.queue.empty()):
                self.queue.put([])
                pred_bbox, image = self.queue.get()
                print(image)
                self.queue.get()
            time.sleep(0.2)



