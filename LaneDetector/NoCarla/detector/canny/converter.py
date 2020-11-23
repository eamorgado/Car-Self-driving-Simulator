"""Summary of module
Converts cv image to Pillow or from Pillow to CV
"""

import cv2
import numpy as np
from PIL import Image

toPillow = lambda cv_image = Image.fromarray(cv_image) 
toCV = lambda pillow_image: np.asarray(pillow_image)
isCV = lambda img: isinstance(img,np.ndarray)