# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#import os 
#os.environ['DISPLAY'] = ':0'

# %% Import the image

image = cv2.imread('test_image.jpg') # load the image (read in BGR)
cv2.imshow('result1', image) # show the image
cv2.waitKey(1)

# %% Edge detection
lane_image = np.copy(image)

# % Step 1 - Convert image to gray scale
gray_BGR = cv2.cvtColor(lane_image, cv2.COLOR_BGR2GRAY)
# gray_RGB = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
cv2.imshow('result3', gray_BGR)
cv2.waitKey(1)


# image2 = mpimg.imread('test_image.jpg') # Read in RGBa
# image2bw = 0.2989*image2[:,:,0] + 0.5870*image2[:,:,1] + 0.1140*image2[:,:,2]

# # bw = 0.2989*r + 0.5870*g + 0.1140*b 
# gray2 = 0.2989*image2[...,0] + 0.570*image2[...,1] + 0.1140*image2[...,2]
# gray3 = image2[...,0:3].sum()


# %% Step 2 - Reduce Noise with Gaussian filter (Gaussian Blur)
blur = cv2.GaussianBlur(gray_BGR, (5,5), 0) # kernel with a size 5*5
cv2.imshow('result4', blur)
cv2.waitKey(1)

# The Canny function applies internely the 5 by 5 graussian when we call it

# %% Step 3 - Apply Canny function
'''
   ## Thresholds ##
 If the grandient is larger than the upper threshold then 
                  it is accepted as an edge pixel.
'''
canny = cv2.Canny(blur, threshold1=50, threshold2=150)
cv2.imshow('result5', canny)


# %% Step 4 - Segmentation - Region of interest

def canny(image):
    gray_BGR = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_BGR, (5,5), 0) # kernel with a size 5*5
    canny = cv2.Canny(blur, threshold1=50, threshold2=150)
    return canny

    

# %% Step 5 - Hought Transform


# %% Step 6 - Output Frame

