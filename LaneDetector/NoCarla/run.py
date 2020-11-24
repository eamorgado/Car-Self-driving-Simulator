import os
import argparse
import sys
from detector.service import laneDetector
from detector.logging.logging import log_info, log_error, show_traceback

if __name__ == '__main__':
    log_info("Created service. Parsing arguments")
    print('Run python run.py --help to get info about running config\n')

    try:
        log_info('Parsing Arguments')
        helps = """
        Configure service:\n\n
        """

        parser = argparse.ArgumentParser(description=''.join(helps))
        parser.add_argument('--path',dest='path',type=str,required=True,help='Path to video or image, if image, add the tag --image to script')
        parser.add_argument('--image', dest='image', action='store_true',help='If used, it will consider the path to be of an image file')
        parser.add_argument('--gray',dest='gray',action='store_true',help='If used, it will convert the image or video to gray scale')
        parser.add_argument('--gaussian',dest='gaussian',action='store_true',help='If used, it will apply a Gaussian filter to the image or video')
        parser.add_argument('--canny',dest='canny',action='store_true',help='If used, it will apply a Canny filter to the image or video')
        parser.set_defaults(
            image=False,
            gray=False,
            gaussian=False,
            canny=False
        )
        #Add other parameters:
        #   --canny
        #   --gaussian
        #   --sobel
        #   --segment
        #   --hough Transform
        #   --use-cv-functions - for testing with more efficient library

        args = parser.parse_args()
        path = args.path

        image = args.image
        gray, gaussian, canny = args.gray, args.gaussian, args.canny


        log_info('Starting Lane detection')
        #check if path exists
        if not os.path.exists(path) or not os.path.isfile(path):
            raise ValueError("Path is not file or does not exist")

        laneDetector(
            path,
            is_image=image,
            do_canny=canny,
            do_gray=gray,
            do_gaussian=gaussian
        )


    except Exception as e:
        show_traceback()
        log_error("Service failed: " + str(e))
