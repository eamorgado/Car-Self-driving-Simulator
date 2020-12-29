import numpy as np
import cv2 as cv
from server.cv_utils import *

def detection(img,service,show_canny=False,show_hough=False):
    p1_r,p2_r,p_avg_r,count_pos_r,  p1_r,p2_r,p_avg_l,count_pos_r = initPoints()

    img = convertRGB(img)
    img = resizeImg(img,(service.screen_width,service.screen_height))

    #ROI coordinates
    img = img[240:480, 108:532]
    img = resizeImg(img, (424,240))

    #Gaussian filter 5x5
    img = gaussianFilter(img,5,5)

    #Canny edge detector with Sobel filter
    img = cannyFilter(img,50,100)

    if show_canny:
        cv.imshow('Canny edge Filter',img)


    #Hough lines transformation
    lines = cv.HoughLinesP(img, rho=1, theta=np.pi / 180.0, threshold=25, minLineLength=10, maxLineGap=20)