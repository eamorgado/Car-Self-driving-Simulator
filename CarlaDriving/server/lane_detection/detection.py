import numpy as np
import cv2 as cv
import math
from server.cv_utils import *
from server.lane_detection.utils import *
import matplotlib.pyplot as plt

left_a, left_b, left_c = [],[],[]
right_a, right_b, right_c = [],[],[]

def detection(img,service,curr_steering_angle,show_canny=False,show_hough=False):
    img = convertRGB(img)
    img = resizeImg(img,(service.screen_width,service.screen_height))
    
    #Gray scale + Gaussian + Canny/Sobel filter
    canny = filterCanny(img)
    cv.imshow("Canny edge filter",canny)

    segmented = segmentRegion(canny)
    cv.imshow("Segmented image",segmented)

    hough_lines = houghFilter(segmented)
    lines = calculateLines(img,hough_lines)

    #Calculate steering angle
    steering_angle = calculateSteeringAngle(img,lines)

    middle_img = showMidLine(img,steering_angle)
    lines_img = showLines(img,lines)

    lines_img = cv.add(lines_img, middle_img) 

    img =  cv.addWeighted(img, 1, lines_img, 0.5, 1)

    cv.imshow("Hough filter",img)

    #Steer the car
    steering_angle = stabilizeSteeringAngle(curr_steering_angle,steering_angle,len(lines))
    #print('Angle', steering_angle)

    return steering_angle
