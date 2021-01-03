import cv2 as cv
import numpy as np

toCV = lambda pillow_image: np.asarray(pillow_image)
isCV = lambda img: isinstance(img,np.ndarray)

toGrayScale = lambda img: cv.cvtColor(img,cv.COLOR_RGB2GRAY) 

convertRGB = lambda img: cv.cvtColor(img,cv.COLOR_BGR2RGB)

resizeImg = lambda img,res: cv.resize(img,res)

gaussianFilter = lambda img,w,h: cv.bilateralFilter(img,d=-1,sigmaColor=w, sigmaSpace=h)

cannyFilter = lambda img,min,max: cv.Canny(img,min,max)


def segmentRegion(frame):
    # Image -> multi-directional array with intensities of each pixel ==> use fram.shape to get puple [#row,#cols,#channels] with the dimensions of image
    height_frame = frame.shape[0]
    width_frame = frame.shape[1]
    
    top_of_mask = height_frame*0.45
    area_interest_vertices = np.array([
        [0,height_frame],
        [width_frame*0.45,top_of_mask],
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
