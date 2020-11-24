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
                cv.imshow("Canny Filter",img)
            elif do_gray:
                gray = toGrayScale(img)
                cv.imgshow("Gray Scale Filter",gray)
            elif do_gaussian:
                gaussian = filterGaussian(img)
                cv.imgshow("Gaussian Filter",gaussian)
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
                        str = "Canny Filter"
                        img = filterCanny(frame)
                    elif do_gray:
                        str = "Gray Scale Filter"
                        img = toGrayScale(frame)
                    elif do_gaussian:
                        str = "Gaussian Filter"
                        img = filterGaussian(frame)
                    cv.imshow(str,img)
                    prev_frame = img
                except Exception as e:
                    print(e)
                    if prev_frame is not None:
                        str = ""
                        if do_canny:
                            str = "Canny Filter"
                        elif do_gray:
                            str = "Gray Scale Filter"
                        elif do_gaussian:
                            str = "Gaussian Filter"
                        cv.imshow(str,prev_frame)
                    continue
                if cv.waitKey(10) & 0xFF == ord('q'):
                    break
            cap.release()
    except Exception as e:
        show_traceback()
        log_error("Error Running laneDetector: " + str(e))

    log_info('Closing all windows')
    cv.destroyAllWindows()