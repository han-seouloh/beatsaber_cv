from utils import parser
from model3d import mod3d
from cv.computervision import *

import time

args = parser.init_argparser()

cap = VideoStream(args.camera).start()
poseDetector = PoseDetector()

# map opencv coordinates to ursina coordinates
def map_cv2ur(cv_centroid, factor = 10):


  cx = (cv_centroid[0]- 0.5) * -factor 
  cy = (cv_centroid[1]- 0.5) * -factor

  return (cx,cy)


# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_pose = mp.solutions.pose

# pose = mp_pose.Pose(
# model_complexity = 0,
# min_detection_confidence=0.5,
# min_tracking_confidence=0.5)

# update
def update():
  t1 = time.time()
  frame = cap.getFrame()
  
  if(frame is None): return


  results = poseDetector.calculate(frame)
  # poseDetector.drawPose(results,frame)

    # lm = results.pose_landmarks
    # lmPose = mp_pose.PoseLandmark

    # #print(lm.landmark[lmPose.LEFT_WRIST].x)
    # #$print(type(results.pose_landmarks[0].x))

    # #if pos1 is not None:

    # (cx,cy, cz) = lm.landmark[lmPose.LEFT_WRIST].x, lm.landmark[lmPose.LEFT_WRIST].y, lm.landmark[lmPose.LEFT_WRIST].z
    # #print(f"x:{cx} y:{cy} z:{cz}")
    #mod3d.worldcube.position +=  (0.01,0.01,0.01) #map_cv2ur(, frame.shape, 10)
  print(int(1/(time.time() - t1)))


# Input to quit the game
def input(key):
  if key == "escape":
    cap.stop()
    cv.destroyAllWindows()
    quit()


mod3d.window.vsync = True
mod3d.window.show_ursina_splash = True
mod3d.window.fps_counter.enabled = True



# run game
mod3d.app.run()


