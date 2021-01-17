import tkinter as tk
from tkinter import Canvas
import numpy as np
import util

class FullScreen(object):
    def __init__(self, window, **kwargs):
        self.window = window
        self.window.geometry("{0}x{1}+0+0".format(
            self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.wait_visibility(window)
        self.window.wm_attributes("-alpha", 0.4)
        self.canvas = Canvas(self.window, width= self.window.winfo_screenwidth(), height = self.window.winfo_screenheight())
        # self.window.config(bg='#000000')
        self.window.wm_attributes("-topmost", 1)

    def draw_box(self, bbox, image):
        out_boxes, out_scores, out_classes, num_boxes = bbox
        image_h, image_w, _ = image.shape
        classes = util.read_class_names("./tensorflow-yolov4-tflite/data/classes/coco.names")
        num_classes = len(classes)
        for i in range(num_boxes[0]):
            if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > num_classes: continue
            coord = out_boxes[0][i]
            coord[0] = int(coord[0] * image_h)
            coord[2] = int(coord[2] * image_h)
            coord[1] = int(coord[1] * image_w)
            coord[3] = int(coord[3] * image_w)
            print("bbox: \n", [coord[1], coord[0], coord[3], coord[2]])
            self.canvas.create_rectangle(coord[1], coord[0], coord[3], coord[2], width=2, outline='black')
        self.canvas.pack()

    def clean_canvas(self):
        self.canvas.delete("all")



