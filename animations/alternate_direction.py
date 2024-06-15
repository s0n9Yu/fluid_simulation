import config
import numpy as np

points=[(20, 20, 1500)]
velocity_x = [(20, 20, -50000), (20, 20, 50000),(20, 20, 50000),(20, 20, -50000) ]
velocity_y = [(20, 20, 50000), (20, 20, 50000),(20, 20, -50000), (20, 20, -50000)]

def getSource(timestep):
    mat = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    for x, y, a in points:
        mat[x, y] += a * config.DELTATIME
    return mat

def getAcceleration(timestep):
    u = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    v = np.zeros((config.SIZE+2, config.SIZE+2), dtype=np.float32)
    
    idx = (timestep // int(0.2 / config.DELTATIME)) % len(velocity_x)
    x, y, au = velocity_x[idx]
    av = velocity_y[idx][2]
    u[x, y] += au * config.DELTATIME
    v[x, y] += av * config.DELTATIME
    
    '''
    for x, y, a in velocity_x:
        u[x, y] += a * config.DELTATIME
    for x, y, a in velocity_y:
        v[x, y] += a * config.DELTATIME
    '''
    
    return u, v