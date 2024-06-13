import numpy as np
import config

def diffusion(density):
    new_density = density.copy().astype(np.float32)
    for i in range(1, config.SIZE + 1):
        for j in range(1, config.SIZE + 1):
            new_density[i][j] -= \
                ( density[i][j-1] \
                + density[i][j+1] \
                + density[i-1][j] \
                + density [i+1][j] \
                - 4 * density[i][j] ) \
                * config.DELTATIME \
                * config.DIFFUSION_FACTOR
                
    return new_density        
        
def avection(density, velocity):
    points = []
    for i in range(1, config.SIZE + 1):
        for j in range(1, config.SIZE + 1):
            points.append((i, j, density[i][j], velocity[i][j]))
        
    new_points = []    
    for y, x, d, v in points:
        new_points.append((y+v[1]*config.DELTATIME, x+v[0]*config.DELTATIME, d))
        
    new_density = np.zeros(density.shape, np.float32)
    for y, x, d in new_points:
        X, Y = x - int(x), y - int(y)
        x1, y1 = int(x), int(y)
        x2, y2 = int(x)+1, int(y)
        x3, y3 = int(x), int(y)+1
        x4, y4 = int(x)+1, int(y)+1
        try:
            new_density[y1][x1] += d * (1-X) * (1-Y)
        except:
            pass
        try:
            new_density[y2][x2] += d * (X) * (1-Y)
        except:
            pass
        try:
            new_density[y3][x3] += d * (1-X) * (Y)
        except:
            pass
        try:
            new_density[y4][x4] += d * (X) * (Y)
        except:
            pass
        
    return new_density
    
def addsource(density):
    new_density = density.copy()
    new_density[64][30] = 1.0
    return new_density

def update(density, velocity):
    new_density = density.copy().astype(np.float32)
    new_density = diffusion(new_density)
    #new_density = avection(new_density, velocity)
    new_density = addsource(new_density)
    return new_density