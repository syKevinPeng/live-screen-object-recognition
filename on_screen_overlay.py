import tkinter as tk
from tkinter import Canvas, Label
from PIL import Image, ImageTk
import util, colorsys,random, math

class FullScreen(object):
    def __init__(self, window, **kwargs):
        self.window = window
        win_width = self.window.winfo_screenwidth()
        win_height = self.window.winfo_screenheight()
        self.window.geometry("{0}x{1}+0+0".format(
            int(win_width/2), win_height))
        # self.window.geometry("2560x1440+0+0")
        self.window.wait_visibility(window)
        # self.window.wm_attributes("-alpha", .3)
        # self.window.wm_attributes("-fullscreen", True)

        self.canvas = Canvas(self.window, width= win_width, height = win_height)
        self.canvas.create_text(win_width//4, win_height//2,
                                font = ("Purisa", 50),
                                text = "Loading Libraries")
        self.canvas.pack()
        self.window.update()

    def draw_box(self, bbox, image):
        out_boxes, out_scores, out_classes, num_boxes = bbox
        print(num_boxes)
        image_h, image_w, _ = image.shape
        classes = util.read_class_names("./tensorflow-yolov4-tflite/data/classes/coco.names")
        num_classes = len(classes)

        hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
        random.seed(0)
        random.shuffle(colors)
        random.seed(None)

        for i in range(num_boxes):
            # if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > num_classes: continue
            coord = out_boxes[i]
            score = out_scores[i]
            class_ind = int(out_classes[i])
            bbox_color = colors[class_ind]
            bbox_thick = int(0.6 * (image_h + image_w) / 600)
            bbox_mess = '%s: %.2f' % (classes[class_ind], score)
            # print([coord[1], coord[0], coord[3], coord[2]])
            self.canvas.create_rectangle(coord[0], coord[1], coord[2], coord[3], width=bbox_thick, outline=util.rgb_to_hex(bbox_color))
            self.draw_text(bbox_mess,[coord[0], coord[1], coord[2], coord[3]])
        self.canvas.pack()


    def clean_canvas(self):
        self.canvas.delete("all")

    # update background image. Input is in np array format.
    def draw_background(self, img):
        my_img = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.canvas.create_image(0,0,anchor=tk.NW, image=my_img)
        self.window.one = my_img
        self.canvas.pack()

    def draw_text(self, message, bbox):
        padding = 20 # in pixel
        x1, y1, x2, y2 = bbox
        pos_x = math.ceil(x1)
        if (math.ceil(y1) - padding) < 0:
            pos_y = math.ceil(y2) + padding
        else:
            pos_y = math.ceil(y1) - padding
        self.canvas.create_text(pos_x, pos_y,anchor=tk.NW, font = "Times 15", text = message)
        # self.canvas.pack()
