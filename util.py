import cv2
import numpy as np
import config
import matplotlib.pyplot as plt

def showArrayHeatmap(arr, title="out"):
    heat = arr.copy()
    print("sum", np.sum(heat), "max", np.max(heat),"min", np.min(heat))
    heat = ((3 * heat) * 255)
    heat = heat.astype(np.uint8)
    print("after", "sum", np.sum(heat), "max", np.max(heat),"min", np.min(heat))
    #heat = cv2.normalize(heat, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    heat = cv2.applyColorMap(heat, cv2.COLORMAP_JET)
    heat = cv2.resize(heat, (config.WINDOW_SIZE, config.WINDOW_SIZE), cv2.INTER_NEAREST)

    cv2.imshow(title, heat)
def drawVel(u0, v0, den):
    #draw velocity
    x, y = range(config.SIZE+2), range(config.SIZE+2)
    u = u0
    v = v0
    print("draw maxx: ", np.max(np.abs(u)))
    print("draw maxy: ", np.max(np.abs(v)))
    plt.imshow(den)
    plt.quiver(x,y,u,v, scale = 10)
    plt.show()
    
    
def sumOfDivergence(u, v):
    u = u.copy()
    v = v.copy()
    h = 1 / config.SIZE
    div = np.zeros(u.shape).astype(np.float32)
    for i in range(1, config.SIZE+1):
        for j in range(1, config.SIZE+1):
            div[i][j] = -0.5 * h * (u[i+1][j] - u[i-1][j] + v[i][j+1] - v[i][j-1])
    return np.sum(div)