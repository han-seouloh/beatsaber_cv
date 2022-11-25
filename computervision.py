import numpy as np
import cv2 as cv

cap = cv.VideoCapture()

cap.open(0)

while(1):
    ret, frame = cap.read()
    
    cv.imshow(frame)