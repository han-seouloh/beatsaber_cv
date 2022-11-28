import numpy as np
import cv2 as cv


from utils.jsonparser import jsonParse

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
        for f in config_dict["filters"]:
            if f["name"] == "gaussian":
                gaussian = {}
                gaussian["size"] = (f["size"],f["size"])
                gaussian["sd"] = f["iters"]

                self.gaussian = gaussian
            
            elif f["name"] == "opening":
                opening = {}
                opening["size"] = (f["size"],f["size"])
                opening["iters"] = f["iters"]

                self.opening = opening      

            elif f["name"] == "closing":
                closing = {}
                closing["size"] = (f["size"],f["size"])
                closing["iters"] = f["iters"]

                self.closing = closing       

    def detect(self, InputArray):

        # Gaussian blur: Noise reduction
        blur = cv.GaussianBlur(InputArray,
                              self.gaussian["size"],
                               2)    # convolves a n x n gaussian kernel with the Input Array

        # BGR to HSV
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

        # HSV color based segmentation
        weak_segmentaiton = cv.inRange(hsv, self.HSVmin, self.HSVmax)

        # Structuring element aquisition: sliding window for morphological opening
        elem_open = cv.getStructuringElement(cv.MORPH_RECT,
                                        self.opening["size"],
                                        (-1,-1))

        # Morphological opening: Noise reduction
        shape = weak_segmentaiton.shape             # Shape of the previous segmentation frame: n x m x c
        eroded = np.zeros(shape , dtype= "uint8")   # Placeholder for result of erosion
        opened = np.zeros(shape, dtype= "uint8")    # Placeholder for result of opening
        cv.erode(weak_segmentaiton, elem_open, eroded, (-1,-1), self.opening["iters"])
        cv.dilate(eroded, elem_open, opened, (-1,-1), self.opening["iters"])

        # Structuring element aquisition: sliding window for morphological closing
        elem_close = cv.getStructuringElement(cv.MORPH_RECT,
                                            self.closing["size"],
                                            (-1,-1))



        # Morphological closing: Close holes
        dilated = np.zeros(shape, dtype= "uint8")  # Placeholder for result of dilation
        closed  = np.zeros(shape, dtype= "uint8")  # Placeholder for result of closing
        cv.dilate(opened, elem_close, dilated, (-1,-1), self.closing["iters"])
        cv.erode(dilated, elem_close, closed, (-1,-1), self.closing["iters"])

        # Geometry calculations
        out = cv.connectedComponentsWithStatsWithAlgorithm(closed, 8, cv.CV_32S, cv.CCL_DEFAULT)

        # Number of blobs found
        num_labels = out[0]

        # Frame with labeled blobs from 0-N
        labels = out[1]

        # Gemoetrical data of each blob
        stats = out[2]

        # Centroids of each blob
        centroids = out[3]

        
        candidates = []
        # Loop through each blob (blob 0 is always the background)
        for i in range(1,num_labels):
            stats_dict = {}

            # unpack the area stat of blob i
            area  = stats[i,cv.CC_STAT_AREA]

            # select blobs with ares between the range
            if (area > 50 and area <10000):
                stats_dict["area"] = area
                stats_dict["centroid"] = centroids[i].astype(int)

                candidates.append(stats_dict)

        if len(candidates) < 2:
            return InputArray

        candidates = sorted(candidates, key= lambda d: d["area"], reverse=True)


        for c in candidates[:2]:
            cv.circle(InputArray, c["centroid"] , 5,(0,220,10), 2)

        d_cx = candidates[0]["centroid"][0] - candidates[1]["centroid"][0] 
        d_cy = candidates[0]["centroid"][1] - candidates[1]["centroid"][1] 

        angle = np.arctan2(d_cx, d_cy)

        #print(angle*180/np.pi)

        cv.line(InputArray,candidates[0]["centroid"],candidates[1]["centroid"],(0,10,220),2)

        cv.imshow("blobs", closed)

            
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