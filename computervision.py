import numpy as np
import cv2 as cv
import json

from jsonparser import jsonParse

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

    def __init__ (self, config_dict):

        # Initialize the class with the desired color detection range
        self.HSVmin = config_dict["HSVmin"]
        self.HSVmax = config_dict["HSVmax"]

        # Set the parameter values to each filter
        self.gaussian = config_dict["filters"][0]
        self.opening = config_dict["filters"][1]
        self.closing = config_dict["filters"][2]
        
    def detect(self, InputArray):

        # Gaussian blur: Noise reduction
        blur = cv.GaussianBlur(InputArray,
                              (self.gaussian["size"],self.gaussian["size"]),
                               2)    # convolves a n x n gaussian kernel with the Input Array

        # BGR to HSV
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

        # HSV color based segmentation
        weak_segmentaiton = cv.inRange(hsv, self.HSVmin, self.HSVmax)

        # Structuring element aquisition: sliding window for morphological operations
        elem = cv.getStructuringElement(cv.MORPH_RECT,
                                        (self.closing["size"],(self.closing["size"])),
                                        (-1,-1))

        # Morphological opening: Noise reduction
        shape = weak_segmentaiton.shape             # Shape of the previous segmentation frame: n x m x c
        eroded = np.zeros(shape , dtype= "uint8")   # Placeholder for result of erosion
        opened = np.zeros(shape, dtype= "uint8")    # Placeholder for result of opening
        cv.erode(weak_segmentaiton, elem, eroded, (-1,-1), self.opening["iters"])
        cv.dilate(eroded, elem, opened, (-1,-1), self.opening["iters"])

        # Morphological closing: Close holes
        dilated = np.zeros(shape, dtype= "uint8")  # Placeholder for result of dilation
        closed  = np.zeros(shape, dtype= "uint8")  # Placeholder for result of closing
        cv.dilate(opened, elem, dilated, (-1,-1), self.closing["iters"])
        cv.erode(dilated, elem, closed, (-1,-1), self.closing["iters"])

        # Geometry calculations
        out = cv.connectedComponentsWithStatsWithAlgorithm(closed, 8, cv.CV_32S, cv.CCL_DEFAULT)

        # Number of blobs found
        num_labels = out[0]

        # Frame with labeld blobs from 0-N
        labels = out[1]

        # Gemoetrical data of each blob
        stats = out[2]

        # Centroids of each blob
        centroids = out[3]

        # Loop through each blob (blob 0 is always the background)
        for i in range(1,num_labels):

            
            width  = stats[i,cv.CC_STAT_WIDTH]
            height = stats[i,cv.CC_STAT_HEIGHT]
            area   = stats[i,cv.CC_STAT_AREA]

            (cx,cy) = centroids[i].astype(int)
            
            cv.circle(InputArray, (cx,cy) , 5,(0,220,10),-1)
        
        return InputArray
                     
    
# Debug for testing the cv pipeline
if __name__ == "__main__":
    
    configs = jsonParse('cv.config.json')

    cap = Camera()
    det = Detector(configs[0])

    # Wait 1 ms until the "esc" key is pressed (ASCII "esc" = 27)
    while (cv.waitKey(1) != 27):
        _, frame = cap.read()

        if _:

            debug = det.detect(frame)

            cv.imshow("Frame", debug)