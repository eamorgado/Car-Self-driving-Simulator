"""Summary of module
Collection of image filters (grayscale, gaussian, canny) and pillow <=> cv image conversion
"""

import cv2 as cv
import numpy as np
from PIL import Image

toPillow = lambda cv_image: Image.fromarray(cv_image) 
toCV = lambda pillow_image: np.asarray(pillow_image)
isCV = lambda img: isinstance(img,np.ndarray)

toGrayScale = lambda img: cv.cvtColor(img,cv.COLOR_RGB2GRAY) 

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
        raise ValueError("Image not in np.array format")

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
        raise ValueError("Image not in np.array format")
    
    if min_val >= max_val:
        raise ValueError('filterCanny: Value order incorrect')
    
    gray_scale = toGrayScale(img)
    gaussian = filterGaussian(img,size=size,stdv=stdv)
    return cv.Canny(gaussian,min_val,max_val)


def segmentRegion(frame):
    # Image -> multi-directional array with intensities of each pixel ==> use fram.shape to get puple [#row,#cols,#channels] with the dimensions of image
    height_frame = frame.shape[0]
    width_frame = frame.shape[1]
    
    top_of_mask = height_frame*0.45
    area_interest_vertices = np.array([
        [0,height_frame],
        [width_frame*0.50,top_of_mask],
        [width_frame*0.65,top_of_mask],
        [width_frame,height_frame]
    ],np.int32)
    area_interest_vertices = [area_interest_vertices]

    # Creates an image filled with zero intensities with the same dimensions as the frame
    mask = np.zeros_like(frame)

    if len(frame.shape) > 2:
        n_channels = frame.shape[2]
        ignore_colors = (255,)*n_channels
    else:
        ignore_colors = 255
    
    # mask will be filled with values of 1 and the other areas will be filled with values of 0
    cv.fillPoly(mask,area_interest_vertices,ignore_colors)

    #bitwise operator will keep only the desired area
    masked_frame = cv.bitwise_and(frame,mask)
    return masked_frame


def houghFilter(frame,distance_resolution=2,angle_resolution=np.pi/180,min_n_intersections=100,min_line_size=150,max_line_gap=50):
    """
    Params:
        frame
        distance_resolution:    distance resolution of accumulator in pixels, larger ==> less precision
        angle_resolution:   angle of accumulator in radians, larger ==> less precision
        min_n_intersections: minimum number of intersections
        min_line_size:  minimum length of line in pixels
        max_line_gap:   maximum distance in pixels between disconnected lines
    """

    frame = filterCanny(frame)
    frame = segmentRegion(frame)
    cv.imshow('Segment',frame)
    placeholder = np.array([])
    hough = cv.HoughLinesP(frame,distance_resolution,angle_resolution,min_n_intersections,placeholder,min_line_size,max_line_gap)
    return hough


