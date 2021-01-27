
import numpy as np
import tkinter as tk
import datetime
import pyautogui

def read_class_names(class_file_name):
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names

def capture_screen():
    # customized value that crop the top and side bar
    vertical_cut = 25
    # horizontal_cut = 70
    dum = tk.Tk()
    screen_width = dum.winfo_screenwidth()
    horizontal_cut = int(screen_width/2)
    dum.withdraw()
    screen_shot = pyautogui.screenshot()
    screen_shot = np.array(screen_shot)[vertical_cut:,horizontal_cut:]
    return screen_shot

# convert rbg color to color hex which is accepted by pyinter
def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def ts():
    return datetime.datetime.now().isoformat()

# convert a list of tensor to a list of numpy array
def convert_tensor_to_np(tensor_list):
    return_list = []
    for tensor in tensor_list:
        return_list.append(tensor.detach().cpu().numpy())
    return return_list