import cv2 as cv
import numpy as np
from detector.filters import toGrayScale, filterGaussian, filterCanny
from detector.logging.logging import log_info, log_error, show_traceback

def laneDetector(path,is_image=False,do_canny=True,do_gray=False,do_gaussian=False):
    try:
        if is_image:
            log_info('Image lane detection selected')
            img = cv.imread(path)

            if do_canny:
                canny = filterCanny(img)
                cv.imshow("Canny Filter",canny)
            elif do_gray:
                gray = toGrayScale(img)
                cv.imshow("Gray Scale Filter",gray)
            elif do_gaussian:
                gaussian = filterGaussian(img)
                cv.imshow("Gaussian Filter",gaussian)
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
                    elif do_gray:
                        s = "Gray Scale Filter"
                        img = toGrayScale(frame)
                    elif do_gaussian:
                        s = "Gaussian Filter"
                        img = filterGaussian(frame)
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