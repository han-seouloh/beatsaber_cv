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


# update
def update():
  frame = cap.getFrame()

  #cv.waitKey(1)
  debug, pos1, pos2 = det.detect(frame)
  #cv.imshow("Frame", debug)
  
  if pos1 is not None:
    mod3d.worldcube.position = map_cv2ur(pos1, frame.shape, 10)

  

# run game
mod3d.app.run()

cap.stop()
cv.destroyAllWindows()