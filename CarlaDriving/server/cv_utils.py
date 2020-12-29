import cv2 as cv

convertRGB = lambda img: cv.cvtColor(img,cv.COLOR_BGR2RGB)

resizeImg = lambda img,res: cv.resize(img,res)

gaussianFilter = lambda img,w,h: cv.bilateralFilter(img,d=-1,sigmaColor=w, sigmaSpace=h)

cannyFilter = lambda img,min,max: cv.Canny(img,min,max)


def initPoints():
    p1_r = (0,0)
    p2_r = (0,0)
    p_avg_r = (0,0)
    count_pos_r = 0

    p1_l = (0,0)
    p2_l = (0,0)
    p_avg_l = (0,0)
    count_pos_l = 0

    return p1_r,p2_r,p_avg_r,count_pos_r,  p1_r,p2_r,p_avg_l,count_pos_r