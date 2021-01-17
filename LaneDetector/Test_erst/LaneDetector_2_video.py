# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def canny(image):
    gray_BGR = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Step 1
    blur = cv2.GaussianBlur(gray_BGR, (5,5), 0) #Step 2 - kernel with a size 5*5
    canny = cv2.Canny(blur, threshold1=50, threshold2=150) #Step 3
    return canny

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height),
                         (1100, height),
                         (600, 250)]])
    mask = np.zeros_like(image) #creates an array of zeros with the same shape of image
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            #x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1), (x2, y2), (255,0,0), thickness=10)
    return line_image

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5)) #until 3/5 of the image
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1, y1, x2, y2])



def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2), deg=1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    
    if len(left_fit) and len(right_fit):
        left_fit_average = np.average(left_fit, axis=0) #average slope of the left lines
        right_fit_average = np.average(right_fit, axis=0) #average slope of the right lines
        left_line = make_coordinates(image, left_fit_average)
        right_line = make_coordinates(image, right_fit_average)
        averaged_lines = [left_line, right_line]
        return averaged_lines


# %% 
cap = cv2.VideoCapture("test2.mp4")
# cap = cv2.VideoCapture("project_video.mp4")
while (cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_canny = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_canny, 
                            rho=2, 
                            theta=np.pi/180,
                            threshold=100,
                            lines=np.array([]),
                            minLineLength=40,
                            maxLineGap=10)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow('result', combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


