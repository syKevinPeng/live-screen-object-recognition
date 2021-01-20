from mss.linux import MSS as mss
# uncomment the following line if you are using windows
# from mss.windows import MSS as mss
import numpy as np
# import detector
from PIL import Image
# import cv2

def read_class_names(class_file_name):
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names

def capture_screen():
    # customized value that crop the top and side bar
    vertical_cut = 25
    horizontal_cut = 70

    with mss() as sct:
        sct_img = sct.grab(sct.monitors[-1])

        # Create captured image and return it as np array
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img = np.asarray(img)[vertical_cut:,horizontal_cut:]
        # print("Got screenshot")
    return img
# convert rbg color to color hex which is accepted by pyinter
def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb
