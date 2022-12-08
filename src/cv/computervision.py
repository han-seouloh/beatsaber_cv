from threading import Thread
import numpy as np
import cv2 as cv
import sys
import mediapipe as mp
import time
from queue import Queue


class VideoStream:
    """Camera handler class"""

    def __init__(self, cam = 0):
        
        # Call the init function of cv.VideoCapture
        self.capture = cv.VideoCapture(cam)

        # Assert that the camera has been opened
        if not self.capture.isOpened():
            try:
                raise Exception("Camera was not found in the given index")
            except Exception as e:
                print("Assertion error: ", e)
                sys.exit(1)

        # Buffer to store retrieved images
        self.fifoBuffer = Queue(maxsize=128)

        # Read first frame
        self.grabbed, frame = self.capture.read()
        
        # Push the frame into the buffer
        self.fifoBuffer.put(frame)

        # Thread has been stopped
        self.stopped = False


    def start(self):
        # Start thread to read frame from the video stream

        t = Thread(target = self.update, args=())
        t.daemon = True
        t.start()
        print("Starting thread...")
        return self

    def update(self):
        while True:
            start = time.time()
            if self.stopped:
                return
        
            if not self.fifoBuffer.full():
                # If the thread has not been stopped, read the next frame
                self.grabbed,frame = self.capture.read()

                # Queue current frame
                self.fifoBuffer.put(frame, block=False)
            end = time.time()
            print(f"VideoStream FPS [{int(1/(end-start))}]")
                   

    def getFrame(self):
        # Return most recent frame
        try:
            frame = self.fifoBuffer.get(block=False)
        except:
            frame = None
        
        return frame

    def stop(self):
        # Stop thread
        self.stopped = True

class PoseDetector:

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
                    model_complexity = 0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)

    
    def calculate(self, frame):
        return self.pose.process(frame)

    def drawPose(self,results,frame):
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        self.mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        #Flip the frame horizontally for a selfie-view display.

        cv.imshow("Results",cv.flip(frame,1))
        cv.waitKey(1)
                
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
            return InputArray, None, None

        candidates = sorted(candidates, key= lambda d: d["area"], reverse=True)


        for c in candidates[:2]:
            cv.circle(InputArray, c["centroid"] , 5,(0,220,10), 2)

        d_cx = candidates[0]["centroid"][0] - candidates[1]["centroid"][0] 
        d_cy = candidates[0]["centroid"][1] - candidates[1]["centroid"][1] 

        angle = np.arctan2(d_cx, d_cy)

        #print(angle*180/np.pi)

        cv.line(InputArray,candidates[0]["centroid"],candidates[1]["centroid"],(0,10,220),2)

        #cv.imshow("blobs", closed)

        c1 = candidates[0]['centroid']
        c2 = candidates[1]['centroid']
            
        return InputArray, c1, c2
                     
    
# Debug for testing the cv pipeline
if __name__ == "__main__":
    
    print("Running computer vision test ...")

    from src.utils.jsonparser import jsonParse

    configs = jsonParse("resources/cv.config.json")

    cap = VideoStream(0).start()
    det = Detector(configs[0])

    # Wait 1 ms until the "esc" key is pressed (ASCII "esc" = 27)
    while (cv.waitKey(1) != 27):

        debug,p1,p2 = det.detect(cap.getFrame())

        cv.imshow("Frame", debug)
    
    cap.stop()
    cv.destroyAllWindows()


