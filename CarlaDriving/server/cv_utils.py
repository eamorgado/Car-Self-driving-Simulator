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
    
    top_of_mask = height_frame*0.55
    area_interest_vertices = np.array([
        [0,height_frame],
        [width_frame*0.45,top_of_mask],
        [width_frame*0.60,top_of_mask],
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



def calculateLinesFromHough(frame,hough):
    def calcCoordinates(frame,slope_intercept):
        slope,intercept = slope_intercept[0],slope_intercept[1]
        
        # Sets initial y-coordinate as height from top down (bottom of the frame)
        y_1 = frame.shape[0]

        # Sets final y-coordinate as 150 above the bottom of the frame
        y_2 = int(y_1 - 150)

        # Sets initial x-coordinate as (y1 - b) / m since y1 = mx1 + b
        x_1 = int((y_1 - intercept) / slope)

        # Sets final x-coordinate as (y2 - b) / m since y2 = mx2 + b
        x_2 = int((y_2 - intercept) / slope)
        return np.array([x_1, y_1, x_2, y_2])

    
    #Lists will all coordinates for lines on left and right side
    left,right = [],[]
    if hough is None:
        return None
    for line in hough:
        x1, y1, x2, y2 = line.reshape(4)

        #Fit linear polly and return (a,b) a = slope, b = intercept
        slope_intercept = np.polyfit((x1, x2), (y1, y2), 1)
        slope,intercept = slope_intercept[0],slope_intercept[1]

        #m < 0 => line on left
        #m > 0 => line on right
        if slope < 0:
            left.append((slope,intercept))
        else:
            right.append((slope,intercept))
        
    left = np.average(left,axis=0)
    right = np.average(right,axis=0)

    left = calcCoordinates(frame,left)
    right = calcCoordinates(frame,right)
    return np.array([left,right])