import config
import numpy as np

points=[(10, 20, 1000), (25, 20, 1000), ]
velocity_x = [(10, 20, 15000), (25, 20, -10000)]
velocity_y = [(10, 20, 0), (25, 20, 0)]

def getSource(timestep):
    mat = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    for x, y, a in points:
        mat[x, y] += a * config.DELTATIME
    return mat

def getAcceleration(timestep):
    u = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    v = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    for x, y, a in velocity_x:
        u[x, y] += a * config.DELTATIME
    for x, y, a in velocity_y:
        v[x, y] += a * config.DELTATIME
    return u, v