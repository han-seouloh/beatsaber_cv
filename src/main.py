from utils import parser
from model3d import mod3d
from cv.computervision import *
from utils.jsonparser import jsonParse

args = parser.init_argparser()

configs = jsonParse("resources/cv.config.json")

cap = Camera(args.camera)
det = Detector(configs[0])

# update
def update():
  _, frame = cap.read()
  if _:
    debug, pos1, pos2 = det.detect(frame)
    cv.imshow("Frame", debug)
  
  if pos1[0] != 0 and pos1[1] != 0:
    mod3d.worldcube.x = (pos1[0]/frame.shape[0]-0.5) * -10
    mod3d.worldcube.y = (pos1[1]/frame.shape[1]-0.5) * -10
  

# run game
mod3d.app.run()