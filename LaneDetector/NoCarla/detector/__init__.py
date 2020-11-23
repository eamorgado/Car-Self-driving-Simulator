
import keyboard #module to real user keyboard input
import cv2 as cv

def startLaneDetection(video_path):
    #load video
    video = cv.VideoCapture(video_path)

    #Apply filters while reading the video frames
    while(video.isOpened()):
        _, frame = video.read()

        if keyboard.read_key() == "q":#user has stopped
            break 
    
    video.release()
    cv.destroyAllWindows()
