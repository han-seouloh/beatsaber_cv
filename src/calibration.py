import json
import cv2 as cv
import math

from cv.computervision import Camera

def nothing(x):
    pass

if __name__ == "__main__":

    cap = Camera()

    # Window and trackbar creation for parametrizing segmentation
    hsv_win = "HSV Calibration"
    cv.namedWindow(hsv_win)
    cv.createTrackbar("Hue min",hsv_win, 0, 360, nothing)
    cv.createTrackbar("Hue max",hsv_win, 360,360, nothing)
    cv.createTrackbar("Sat min",hsv_win, 0,100, nothing)
    cv.createTrackbar("Sat max",hsv_win, 100,100, nothing)
    cv.createTrackbar("Val min",hsv_win, 0,100, nothing)
    cv.createTrackbar("Val max",hsv_win, 100,100, nothing)

    # Window and trackbar creation for parametrizing morphological operations
    morph_win = "Morphological operations"
    cv.namedWindow(morph_win)
    cv.createTrackbar("Opening s.e. size",morph_win, 0, 10, nothing)
    cv.createTrackbar("Opening iterations",morph_win, 0, 10, nothing)
    cv.createTrackbar("Closing s.e. size",morph_win, 0, 10, nothing)
    cv.createTrackbar("Closing iterations",morph_win, 0, 10, nothing)

    config_path = 'resources/cv.config.json'
    
    # Read the existing JSON configuration file
    with open(config_path, 'r') as f:
        config = json.load(f)
        f.close()

    # Create tuple placeholders for the HSV ranges
    hsv_min = tuple
    hsv_max = tuple
    

    while (cv.waitKey(1) != 27):
        # Poll the current values of the trackbars and condition the signal values
        h_min = cv.getTrackbarPos("Hue min",hsv_win) / 2
        h_max = cv.getTrackbarPos("Hue max",hsv_win) / 2
        s_min = cv.getTrackbarPos("Sat min",hsv_win) * 2.55
        s_max = cv.getTrackbarPos("Sat max",hsv_win) * 2.55 
        v_min = cv.getTrackbarPos("Val min",hsv_win) * 2.55
        v_max = cv.getTrackbarPos("Val max",hsv_win) * 2.55

        # Pack the values into a tuple
        hsv_min = (h_min, s_min, v_min)
        hsv_max = (h_max, s_max, v_max)

        # Read a new video frame
        ret, frame = cap.read()

        if ret:

            #Segment the image with the given HSV ranges
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            bin = cv.inRange(hsv, hsv_min, hsv_max)

            # Display the result of the callibration
            cv.imshow(hsv_win, bin)
    
    # Convert tuple to string
    separator = ','
    hsv_min_val = separator.join([str(math.ceil(i)) for i in hsv_min])
    hsv_max_val = separator.join([str(math.ceil(i)) for i in hsv_max])
    
    # Update the new HSV range in the JSON object
    config["detection"][0]["HSVmin"] = hsv_min_val
    config["detection"][0]["HSVmax"] = hsv_max_val
    
    # Write the calibration data to the config.json file
    with open(config_path, 'w') as f:
        json.dump(config, f, indent = 4)
        f.close()


            



