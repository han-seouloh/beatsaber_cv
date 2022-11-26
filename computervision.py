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

                
class Detector:
    """General purpose color based object detection"""

    def __init__ (self, HSVmin, HSVmax):

        # Initialize the class with the desired color detection range
        self.HSVmin = HSVmin
        self.HSVmax = HSVmax
        
    def detect(self, InputArray):

        # Gaussian blur: Noise reduction
        blur = cv.GaussianBlur(InputArray, (5,5), 2)    # convolves a 5x5 gaussian kernel with the Input Array

        # BGR to HSV
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

        # HSV color based segmentation
        weak_segmentaiton = cv.inRange(hsv, self.HSVmin, self.HSVmax)

        # Structuring element aquisition: sliding window for morphological operations
        elem = cv.getStructuringElement(cv.MORPH_RECT, (5,5), (-1,-1))

        # Morphological opening: Noise reduction
        shape = weak_segmentaiton.shape             # Shape of the previous segmentation frame: n x m x c
        eroded = np.zeros(shape , dtype= "uint8")   # Placeholder for result of erosion
        opened = np.zeros(shape, dtype= "uint8")    # Placeholder for result of opening
        cv.erode(weak_segmentaiton, elem, eroded, (-1,-1), 2)
        cv.dilate(eroded, elem, opened, (-1,-1), 2)

        # Morphological closing: Close holes
        dilated = np.zeros(shape, dtype= "uint8")  # Placeholder for result of dilation
        closed  = np.zeros(shape, dtype= "uint8")  # Placeholder for result of closing
        cv.dilate(opened, elem, dilated, (-1,-1), 2)
        cv.erode(dilated, elem, closed, (-1,-1), 2)
        
        







                

                
# Debug for testing the cv pipeline
if __name__ == "__main__":
    
    cap = Camera()
    det = Detector(HSVmin = np.array([0,0,0]), HSVmax = np.array([10,255,255]))
    
    if not cap.isOpened():
        print("Could not access camera")
        exit()

    while (cv.waitKey(1) != 27):
        ret, frame = cap.read()

        if ret:

            debug = det.detect(frame)

            cv.imshow("Frame", debug)