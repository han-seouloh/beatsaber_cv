import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Could not access camera")
    exit()

while (cv.waitKey(1) != 27):
    ret, frame = cap.read()
    
    if ret:
        cv.imshow("Frame",frame)