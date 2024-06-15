import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

from util import showArrayHeatmap, drawVel, output_video
from fix_simulate import *
import config
import circularflow
import randomflow
import constantflow

vec = [
    [100, 0],
    [0, 100],
    [100, 0],
    [0, 100],
]

np.random.seed(0)

density = np.zeros((config.SIZE+2, config.SIZE+2), np.float32)
u = np.zeros((config.SIZE+2, config.SIZE+2), np.float32)
v = np.zeros((config.SIZE+2, config.SIZE+2), np.float32)

cnt = 0

frames = []

while True:
    if cnt % 10 == 0: # for debugging
        #drawVel(u, v, density)
        pass
    if cv2.waitKey(10) == 27: # <Esc>
        break
    
    # generate source, acceleration field
    density_prev = np.zeros((config.SIZE+2, config.SIZE+2), np.float32)
    u_prev = np.zeros((config.SIZE+2, config.SIZE+2), np.float32)
    v_prev = np.zeros((config.SIZE+2, config.SIZE+2), np.float32)
    update(config.SIZE, density_prev, density, u_prev, u, v_prev, v, cnt)
    frames.append(showArrayHeatmap(density))
    cnt += 1
        
cv2.destroyAllWindows()

output_video(frames, "output.mp4")