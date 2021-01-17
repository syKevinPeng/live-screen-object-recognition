from mss.linux import MSS as mss
# uncomment the following line if you are using windows
# from mss.windows import MSS as mss
import numpy as np
import detector
from PIL import Image
import random, colorsys

def read_class_names(class_file_name):
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names

def capture_screen():
    with mss() as sct:
        sct_img = sct.grab(sct.monitors[1])

        # Create captured image and return it as np array
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img = np.asarray(img)
    return img

