import numpy as np
import cv2 as cv

cap = cv.VideoCapture()

cap.open(0)

if not cap.isOpened():
    print("Could not access camera")
    exit()

while(cap.isOpene):
    ret, frame = cap.read()
    
    if ret:
        cv.imshow("Frame",frame)