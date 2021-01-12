import numpy as np
import cv2
import tensorflow as tf
from tensorflow.python import saved_model

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