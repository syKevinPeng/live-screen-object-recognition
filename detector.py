import numpy as np
import cv2,util, colorsys, random
import tensorflow as tf
from tensorflow.python import saved_model
# import os
# print(os.environ["CUDA_VISIBLE_DEVICES"])
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# RGB img input
def yolo_detector(original_image):
    input_size = 416
    weights = "./tensorflow-yolov4-tflite/checkpoints/yolov4-416/" # path to the yolo weights
    iou = 0.5 # IOU threshold
    score = 0.25 # prediction score threshold

    image_data = cv2.resize(original_image,(input_size,input_size))
    image_data = np.asarray(image_data / 255).astype(np.float32)

    #load model
    saved_model_loaded = saved_model.load(weights, tags = [saved_model.tag_constants.SERVING])
    infer = saved_model_loaded.signatures['serving_default']
    batch_data = tf.constant([image_data])
    pred_bbox = infer(batch_data)
    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class = 50,
        max_total_size = 50,
        iou_threshold = iou,
        score_threshold = score
    )
    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
    return pred_bbox

def yolo_init():
    # load parameters
    input_size = 416
    weights = "./tensorflow-yolov4-tflite/checkpoints/yolov4-416/" # path to the yolo weights
    iou = 0.5 # IOU threshold
    score = 0.25 # prediction score threshold

    # load model
    saved_model_loaded = saved_model.load(weights, tags=[saved_model.tag_constants.SERVING])
    infer = saved_model_loaded.signatures['serving_default']

    # init classes and colors
    classes = util.read_class_names("./tensorflow-yolov4-tflite/data/classes/coco.names")
    num_classes = len(classes)
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    random.seed(0)
    random.shuffle(colors)
    random.seed(None)
    return classes, colors