# import the necessary packages
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from nms import non_max_suppression
import config
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2 as cv


#Parse cmd line args (path to image)
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

image_path = args["image"]

##
#Load Model and labels
print("[INFO] loading model and label binarizer...")
model = load_model(config.MODEL_PATH)
lb = pickle.loads(open(config.ENCODER_PATH, "rb").read())

#Load image + resize
#TODO: change resize size to app/Carla
image = cv.imread(args["image"])
image = imutils.resize(image, width=500)



# run selective search on the image to generate bounding box proposal
# regions
print("[INFO] running selective search...")
ss = cv.ximgproc.segmentation.createSelectiveSearchSegmentation()

cv.imshow("test",ss)

ss.setBaseImage(image)
ss.switchToSelectiveSearchFast()
rects = ss.process()




