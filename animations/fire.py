import config
import numpy as np
import random
import math

def getSource(timestep):
    mat = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    
    for y in range(10, config.SIZE-10, 2):
        mat[config.SIZE - 3, y] += (random.random() * 0.5 + 0.5) * 1000 * config.DELTATIME
    return mat

def getAcceleration(timestep):
    u = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    v = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    
    for y in range(10, config.SIZE-10, 2):
        u[config.SIZE - 3, y] = (-10000) * config.DELTATIME
    
    #v[config.SIZE - 5, :] += math.sin(timestep * config.DELTATIME * 6) * (5000) * config.DELTATIME
    #v[config.SIZE - 5, :] += (random.random() * (10000) - 5000) * config.DELTATIME
    for x in range(3, config.SIZE - 5, 3):
       for y in range(1, config.SIZE):
            #v[config.SIZE - 5, y] += (random.random() * (200000) - 100000) * config.DELTATIME
            v[x, y] += (random.random() * (100000) - 50000) * config.DELTATIME
    u[:, :config.SIZE - 4] += (-1000) * config.DELTATIME # for floating
      
    
    return u, v