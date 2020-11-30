"""Summary of module
Collection of functions to visualize lane detected lines
"""
import cv2 as cv
import numpy as np


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


def showLines(frame,lines,color=(0,0,255),thickness=5):
    # Creates an image filled with zero intensities with the same dimensions as the frame
    lines_visualize = np.zeros_like(frame)
    # Checks if any lines are detected
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            # Draws lines between two coordinates with red color and 5 thickness
            cv.line(lines_visualize, (x1, y1), (x2, y2), color, thickness)
    return lines_visualize






