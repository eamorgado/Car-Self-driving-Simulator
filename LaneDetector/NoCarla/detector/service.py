import cv2 as cv
import numpy as np
from detector.filters import *
from detector.logging.logging import log_info, log_error, show_traceback

def laneDetector(path,is_image=False,do_canny=True,do_gray=False,do_gaussian=False,do_segment=False,do_hough=False):
    try:
        if is_image:
            log_info('Image lane detection selected')
            img = cv.imread(path)

            if do_canny:
                canny = filterCanny(img)
                cv.imshow("Canny Filter",canny)
                if do_segment:
                    segment = segmentRegion(canny)
                    cv.imshow("Segmented Canny",segment)
            elif do_gray:
                gray = toGrayScale(img)
                cv.imshow("Gray Scale Filter",gray)
                if do_segment:
                    segment = segmentRegion(gray)
                    cv.imshow("Segmented gray",segment)
            elif do_gaussian:
                gaussian = filterGaussian(img)
                cv.imshow("Gaussian Filter",gaussian)
                if do_segment:
                    segment = segmentRegion(gaussian)
                    cv.imshow("Segmented gaussian",segment)
            elif do_segment:
                segment = segmentRegion(img)
                cv.imshow("Segmented image",segment)
            elif do_hough:
                hough = houghFilter(img)
                cv.imshow("Hough filter",hough)

            cv.waitKey(0); cv.destroyAllWindows(); cv.waitKey(1) 
        else:
            log_info('Video lane detection selected')
            print(path)
            cap = cv.VideoCapture(path)
            prev_frame = None
            while(cap.isOpened()):
                try:
                    _,frame = cap.read()
                    frame = cv.resize(frame,(800,600))
                    if do_canny:
                        s = "Canny Filter"
                        img = filterCanny(frame)
                        if do_segment:
                            s = "Segmented Canny"
                            img = segmentRegion(img)
                    elif do_gray:
                        s = "Gray Scale Filter"
                        img = toGrayScale(frame)
                        if do_segment:
                            s = "Segmented Gray"
                            img = segmentRegion(img)
                    elif do_gaussian:
                        s = "Gaussian Filter"
                        img = filterGaussian(frame)
                        if do_segment:
                            s = "Segmented Gaussian"
                            img = segmentRegion(img)
                    elif do_segment:
                        s = "Segmented"
                        img = segmentRegion(frame)
                    elif do_hough:
                        s = "Hough filter"
                        img = houghFilter(img)
                    cv.imshow(s,img)
                    prev_frame = img
                except Exception as e:
                    print(e)
                    if prev_frame is not None:
                        s = ""
                        if do_canny:
                            s = "Canny Filter"
                        elif do_gray:
                            s = "Gray Scale Filter"
                        elif do_gaussian:
                            s = "Gaussian Filter"
                        elif do_segment:
                            s = "Segmented"
                        elif do_hough:
                            s = "Hough filter"
                        cv.imshow(s,prev_frame)
                    continue
                if cv.waitKey(10) & 0xFF == ord('q'):
                    break
            cap.release()
            log_info('Closing all windows')
            cv.destroyAllWindows()
    except Exception as e:
        show_traceback()
        log_error("Error Running laneDetector: " + str(e))