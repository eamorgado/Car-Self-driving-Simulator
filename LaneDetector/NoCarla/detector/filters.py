"""Summary of module
Collection of image filters (grayscale, gaussian, canny) and pillow <=> cv image conversion
"""

import cv2
import numpy as np
from PIL import Image

toPillow = lambda cv_image: Image.fromarray(cv_image) 
toCV = lambda pillow_image: np.asarray(pillow_image)
isCV = lambda img: isinstance(img,np.ndarray)

toGrayScale = lambda img: cv.cvtColor(toCV(img) if not isCV(img) else img,cv.COLOR_RGB2GRAY) 

def filterGaussian(img,size=(5,5),stdv=0):
    """Summary of filterGaussian
    This will apply a noise reduction filter, we will use s 5x5 Gaussian filter to smooth
        the image to lower the sensitivity to noise. (The smaller the size the less visible the blur)

    To populate the Gaussian matrix we will use a kernel of normally distributed[stdv=1] numbers which will
        set each pixel value equal to the weighted average of its neighboor pixels

    The Gaussian distribution:
        Gd = (1/2pi*stdv^2)exp(-((i-(k+1)^2) + (j - (k+1)^2))/(2*stdv^2))

        i,j E [1,2k+1] for the kernel of size: (2k+1)x(2k+1) 
    """

    if not isCV(img):
        img = toCV(img)

    if not isinstance(size,tuple):
        raise ValueError('filterGaussian: Size for Gaussian filter not tuple')
    return cv.GaussianBlur(img,size,stdv)


def filterCanny(img,min_val=50,max_val=150,size=(5,5),stdv=0):
    """
    The Canny detector is a multi-stage algorithm optimized for fast real-time edge detection, 
        which will reduce complexity of the image much further.

    The algorithm will detect sharp changes in luminosity and will define them as edges.

    The algorithm has the following stages:
        -   Noise reduction
        -   Intensity gradient - here it will apply a Sobel filter along the x and y axis to detect if edges are horizontal vertical or diagonal
        -   Non-maximum suppression - this shortens the frequency bandwith of the signal to sharpen it
        -   Hysteresis thresholding
    """
    if not isCV(img):
        img = toCV(img)
    
    if min_val >= max_val:
        raise ValueError('filterCanny: Value order incorrect')
    
    gray_scale = toGrayScale(img)
    gaussian = filterGaussian(img,size=size,stdv=stdv)
    return cv.Canny(gaussian,min_val,max_val)
    