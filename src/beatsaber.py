from utils import parser
from cv.computervision import *

import time

args = parser.init_argparser()

cap = VideoStream(args.camera).start()
poseDetector = PoseDetector()

while True:
    t1 = time.time()
    frame = cap.getFrame()

    if(frame is None): continue


    results = poseDetector.calculate(frame)
    poseDetector.drawPose(results,frame)

    print(int(1/(time.time() - t1)))