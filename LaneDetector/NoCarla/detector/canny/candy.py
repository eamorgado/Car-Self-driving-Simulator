"""Summary of module
Canny detector logic
"""

import cv2 as cv
from PIL import Image

from detector.canny.converter import isCV, toCV, toPillow


def filterGaussian(size,stdv=1):
    """Summary of filterGaussian
    This will apply a noise reduction filter, we will use s 5x5 Gaussian filter to smooth
        the image to lower the sensitivity to noise. (The smaller the size the less visible the blur)

    To populate the Gaussian matrix we will use a kernel of normally distributed[stdv=1] numbers which will
        set each pixel value equal to the weighted average of its neighboor pixels

    The Gaussian distribution:
        Gd = (1/2pi*stdv^2)exp(-((i-(k+1)^2) + (j - (k+1)^2))/(2*stdv^2))

        i,j E [1,2k+1] for the kernel of size: (2k+1)x(2k+1) 
    """

    size = int(size) // 2
    #Create a multi-dimensional mesh grid with the x and y axis for horizontal and vertical filter
    # For instance, if size = 3x3 the mesh grids are as follows
    #   x = [               y = [
    #       [-1,-1,-1]           [-1,0,1]
    #       [0,0,0]              [-1,0,1]
    #       [1,1,1]              [-1,0,1]
    #       ]                    ]

    x,y = np.mgrid[-size:size+1, -size:size+1]

    gaussian = 1/(float(2) * np.pi * stdv**2)
    gaussian *= np.exp(-((x**2 + y**2) / (float(2) * stdv**2)))
    return gaussian



class CannyDetector():
    """
    The Canny detector is a multi-stage algorithm optimized for fast real-time edge detection, 
        which will reduce complexity of the image much further.

    The algorithm will detect sharp changes in luminosity and will define them as edges.

    The algorithm has the following stages:
        -   Noise reduction
        -   Intensity gradient
        -   Non-maximum suppression
        -   Hysteresis thresholding
    """
    def __init__(self,use_library=False):
        self.use_library = use_library
    
    def canny(self,image,min=50,max=150):
        if self.use_library:
            if not isCV(image):
                image = toCV(image)
                return cv.Canny(image,min,max)
    


