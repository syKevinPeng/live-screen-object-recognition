import tkinter as tk
from tkinter import Canvas


class FullScreen(object):
    def __init__(self, master, **kwargs):
        self.master=master
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth(), master.winfo_screenheight()))

    def draw_box(self, bbox):
        canvas = Canvas(self.master)
        canvas.pack()
        canvas.create_rectangle(bbox, width=2, outline = 'black')


