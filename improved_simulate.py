import numpy as np
import config

def divergence(vel):
    divergence = np.zeros(vel.shape[:2], np.float32)
    pressure = np.zeros(vel.shape[:2], np.float32)
    h = 1.0 / config.SIZE
    for i in range(1, config.SIZE+1):
        for j in range(1, config.SIZE+1):
            divergence[i][j] = -h * 0.5 * (vel[i][j+1][1] - vel[i][j-1][1] + vel[i+1][j][0] - vel[i-1][j][0])
    print("sum of divergence: ", np.sum(divergence))

def project(velocity):
    divergence = np.zeros(velocity.shape[:2], np.float32)
    pressure = np.zeros(velocity.shape[:2], np.float32)
    h = 1.0 / config.SIZE
    for i in range(1, config.SIZE+1):
        for j in range(1, config.SIZE+1):
            divergence[i][j] = -h * 0.5 * (velocity[i][j+1][0] - velocity[i][j-1][0] + velocity[i+1][j][1] - velocity[i-1][j][1])
    for it in range(config.ITERATION):
        for i in range(1, config.SIZE+1):
            for j in range(1, config.SIZE+1):
                pressure[i][j] = ( divergence[i][j] \
                + (pressure[i+1][j] + pressure[i-1][j] + pressure[i][j+1] + pressure[i][j-1]) ) / 4
    new_velocity = velocity.copy()
    #print("divergence: max:", np.max(divergence), "min: ", np.min(divergence))
    #print("pressure: max: ", np.max(pressure), "min: ", np.min(pressure))
    for i in range(1, config.SIZE+1):
        for j in range(1, config.SIZE+1):
            new_velocity[i][j][0] -= 0.5 * (pressure[i][j+1] - pressure[i][j-1]) / h
            new_velocity[i][j][1] -= 0.5 * (pressure[i+1][j] - pressure[i-1][j]) / h
            
    return new_velocity
    
                

def diffusion(density):
    new_density = density.copy().astype(np.float32)
    for it in range(config.ITERATION):
        for i in range(1, config.SIZE + 1):
            for j in range(1, config.SIZE + 1):
                a = config.DELTATIME*config.DIFFUSION_FACTOR
                '''
                new_density[i][j] = \
                    (
                        density[i][j] \
                        + config.DIFFUSION_FACTOR * config.DELTATIME * 
                        (new_density[i-1][j] + new_density[i+1][j] + new_density[i][j-1] + new_density[i][j+1])
                    ) / (1 + 4 * config.DELTATIME * config.DIFFUSION_FACTOR)
                '''
                new_density[i][j] = \
                    (
                        density[i][j] \
                        + a * 
                        (new_density[i-1][j] + new_density[i+1][j] + new_density[i][j-1] + new_density[i][j+1])
                    ) / (1 + 4 * a)
                
                    
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
    
def addsource(density, s, set=False):
    new_density = density.copy()
    for y, x, a in s:
        if not set:
            new_density[y][x] += config.DELTATIME * a
        else:
            new_density[y][x] = a
    return new_density

def update(density, velocity):
    new_density = density.copy().astype(np.float32)
    new_velocity = velocity.copy().astype(np.float32)
    
    #stepvel
    new_velocity[:, :, :] = addsource(new_velocity[:, :, :], config.velocity_x)
    print("add maxx: ", np.max(new_velocity[:,:,0]))
    print("add maxy: ", np.max(new_velocity[:,:,1]))
    new_velocity[:, :, :] = diffusion(new_velocity[:,:,:])
    add_velocity = new_velocity.copy()
    new_velocity_tmp = project(new_velocity)  
    new_velocity[:, :, :] = avection(add_velocity[:,:,:], new_velocity_tmp)
    new_velocity = project(new_velocity)
    divergence(new_velocity)
    print("proj maxx: ", np.max(new_velocity[:,:,0]))
    print("proj maxy: ", np.max(new_velocity[:,:,1]))
    
    #stepdense
    new_density = addsource(new_density, config.points)
    new_density = diffusion(new_density)
    new_density = avection(new_density, new_velocity)
    
    return new_density, new_velocity