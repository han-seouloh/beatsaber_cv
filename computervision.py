import numpy as np
import cv2 as cv

class Camera (cv.VideoCapture):
    """Camera handler class"""

    def __init__(self, cam = 0):
        
        # Call the init function of cv.VideoCapture
        super(Camera, self).__init__(cam)

        # Assert that the camera has been opened
        if not self.isOpened():

            try:
                raise AssertionError("Camera was not found in the given index")
            except AssertionError as e:
                print("Assertion error: ", e)

                
                

                
# Debug for testing the cv pipeline
if __name__ == "__main__":
    cap = Camera()

    if not cap.isOpened():
        print("Could not access camera")
        exit()

    while (cv.waitKey(1) != 27):
        ret, frame = cap.read()
        
        if ret:
            cv.imshow("Frame",frame)