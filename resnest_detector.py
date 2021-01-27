from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import util
# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

CONFIG_1 = "./detectron2-ResNeSt/configs/COCO-InstanceSegmentation/mask_rcnn_ResNeSt_101_FPN_syncBN_1x.yaml"
CONFIG_2 = "./detectron2-ResNeSt/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"

class ResnestDetector():
    def __init__(self):
        self.cfg = get_cfg()
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")


    def detect(self, image:np.ndarray):
        predictor = DefaultPredictor(self.cfg)
        outputs = predictor(image)
        pred_class = outputs["instances"].pred_classes #a vector of N labels in range [0, num_categories).
        pred_class = pred_class.detach().cpu().numpy()
        pred_box = outputs["instances"].pred_boxes # Boxes object storing N boxes. [left, up, right, bottom]
        pred_box = pred_box.tensor.cpu().numpy()
        pred_score = outputs["instances"].scores # a vector of N confidence scores.
        pred_score = pred_score.detach().cpu().numpy()
        pred_mask = outputs["instances"].pred_masks # a tensor of shape (N, H, W), masks for each detected instance.
        pred_mask = pred_mask.detach().cpu().numpy()
        predictions = [pred_box, pred_score, pred_class,len(pred_box)]
        return predictions

