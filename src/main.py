from utils import parser
from model3d import mod3d
from cv.computervision import *
from utils.jsonparser import jsonParse

args = parser.init_argparser()

configs = jsonParse("resources/cv.config.json")

cap = Camera(args.camera).start()
det = Detector(configs[0])

# map opencv coordinates to ursina coordinates
def map_cv2ur(cv_centroid, frame_shape, factor = 10):

  w,h,c = frame_shape

  cx = (cv_centroid[0]/w - 0.5) * -factor 
  cy = (cv_centroid[1]/h - 0.5) * -factor

  return (cx,cy)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# update
def update():
  frame = cap.getFrame()

  frame.flags.writeable = False
  frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
  mp_pose = cap.getPose()

  results = cap.getResults()
  #   results = pose.process(frame)
  if(results == 0): return
  # Draw the pose annotation on the image.
  frame.flags.writeable = True
  frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
  mp_drawing.draw_landmarks(
      frame,
      results.pose_landmarks,
      mp_pose.POSE_CONNECTIONS,
      landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the frame horizontally for a selfie-view display.

  cv.imshow("a",cv.flip(frame,1))
  cv.waitKey(1)
  #if pos1 is not None:
  #  mod3d.worldcube.position = map_cv2ur(pos1, frame.shape, 10)

# Input to quit the game
def input(key):
  if key == "escape":
    cap.stop()
    quit()

# run game
mod3d.app.run()


cv.destroyAllWindows()