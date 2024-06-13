import numpy as np
import config
from improved_simulate import *
import matplotlib.pyplot as plt
import randomflow

def divergence(velocity):
    divergence = np.zeros(velocity.shape[:2], np.float32)
    h = 1.0 / config.SIZE
    for i in range(1, config.SIZE+1):
        for j in range(1, config.SIZE+1):
            divergence[i][j] = h * 0.5 * (velocity[i][j+1][0] - velocity[i][j-1][0] + velocity[i+1][j][1] - velocity[i-1][j][1])
    return divergence

velocity = randomflow.Randomflow



    

    
before = velocity
after = project(velocity)
more_after = project(after)
    
print("before: " , "max: ", np.max(divergence(before)), "min: ", np.min(divergence(before)))
print("after: " , "max: ", np.max(divergence(after)), "min: ", np.min(divergence(after)))
print("moreafter: " , "max: ", np.max(divergence(more_after)), "min: ", np.min(divergence(more_after)))
