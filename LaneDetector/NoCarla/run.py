import os
import argparse
import sys

from detector import startLaneDetection
from detector.logging import log_info, log_error, show_traceback

if __name__ == '__main__':
    log_info("Created service. Parsing arguments")
    print('Run python run.py --help to get info about running config\n')

    try:
        log_info('Parsing Arguments')
        helps = """
        Configure service:\n\n
        """

        parser = argparse.ArgumentParser(description=''.join(helps))
        parser.add_argument('--path',dest='path',type=str,required=True,help='Path to video')
        #Add other parameters:
        #   --canny
        #   --gaussian
        #   --sobel
        #   --segment
        #   --hough Transform
        #   --use-cv-functions - for testing with more efficient library

        args = parser.parse_args()
        path = args.path

        log_info('Starting Lane detection')
        #check if path exists
        if not os.path.exists(path) or not os.path.isfile(path):
            raise ValueError("Path is not file or does not exist")


    except Exception as e:
        show_traceback()
        log_error("Service failed: " + str(e))
