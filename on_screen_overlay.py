import tkinter as tk
from tkinter import Canvas, Label
from PIL import Image, ImageTk
import util, colorsys,random

class FullScreen(object):
    def __init__(self, window, **kwargs):
        self.window = window
        win_width = self.window.winfo_screenwidth()
        win_height = self.window.winfo_screenheight()
        # self.window.geometry("{0}x{1}+0+0".format(
        #     self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.geometry("2560x1440+0+0")
        self.window.wait_visibility(window)
        # self.window.wm_attributes("-alpha", 0.5)
        # self.window.wm_attributes("-fullscreen", True)

        self.canvas = Canvas(self.window, width= win_width, height = win_height)
        self.canvas.create_text(win_width/2, win_height/2,
                                font = ("Purisa", 120),
                                text = "Loading Libraries")
        self.canvas.pack()
        self.window.update()

    def draw_box(self, bbox, image):
        out_boxes, out_scores, out_classes, num_boxes = bbox
        image_h, image_w, _ = image.shape
        classes = util.read_class_names("./tensorflow-yolov4-tflite/data/classes/coco.names")
        num_classes = len(classes)

        hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
        random.seed(0)
        random.shuffle(colors)
        random.seed(None)

        for i in range(num_boxes[0]):
            if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > num_classes: continue
            coord = out_boxes[0][i]
            coord[0] = int(coord[0] * image_h)
            coord[2] = int(coord[2] * image_h)
            coord[1] = int(coord[1] * image_w)
            coord[3] = int(coord[3] * image_w)

            score = out_scores[0][i]
            class_ind = int(out_classes[0][i])
            bbox_color = colors[class_ind]
            bbox_thick = int(0.6 * (image_h + image_w) / 600)
            bbox_mess = '%s: %.2f' % (classes[class_ind], score)
            self.canvas.create_rectangle(coord[1], coord[0], coord[3], coord[2], width=bbox_thick, outline=util.rgb_to_hex(bbox_color))
        self.canvas.pack()

    def clean_canvas(self):
        self.canvas.delete("all")

    # update background image. Input is in np array format.
    def draw_background(self, img):
        my_img = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.canvas.create_image(0,0, anchor=tk.NW, image=my_img)
        self.canvas.pack()
        print("yes")

