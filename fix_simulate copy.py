import numpy as np
import config
import util

def set_bound(target, flag):
    target = target.copy()
    for i in range(1, config.SIZE+1):
        if flag == 1:
            target[0][i] = -target[1][i]
            target[config.SIZE+1][i] = -target[config.SIZE][i]
        else:
            target[0][i] = target[1][i]
            target[config.SIZE+1][i] = target[config.SIZE][i]
        if flag == 2:
            target[i][0] = -target[i][1]
            target[i][config.SIZE+1] = -target[i][config.SIZE]
        else:
            target[i][0] = target[i][1]
            target[i][config.SIZE+1] = target[i][config.SIZE]
            
    target[0][0] = 0.5 * (target[1][0] + target[0][1])
    target[0][config.SIZE+1] = 0.5 * (target[1][config.SIZE+1] + target[0] [config.SIZE])
    target[config.SIZE+1][0] = 0.5 * (target[config.SIZE][0] + target[config.SIZE+1][1])
    target[config.SIZE+1][config.SIZE+1] = 0.5 * (target[config.SIZE][config.SIZE+1] + target[config.SIZE+1][config.SIZE])
    return target    
    

def project(u, v):
    u = u.copy()
    v = v.copy()
    h = 1.0 / config.SIZE
    div = np.zeros(u.shape).astype(np.float32)
    for i in range(1, config.SIZE+1):
        for j in range(1, config.SIZE+1):
            div[i][j] = -0.5 * h * (u[i+1][j] - u[i-1][j] + v[i][j+1] - v[i][j-1])
    
    pressure = np.zeros(u.shape).astype(np.float32)
    div = set_bound(div, 0)
    pressure = set_bound(pressure, 0)
    for it in range(config.ITERATION):
        for i in range(1, config.SIZE+1):
            for j in range(1, config.SIZE+1):
                pressure[i][j] = (div[i][j] + pressure[i-1][j] + pressure[i+1][j] + pressure[i][j-1] + pressure[i][j+1]) \
                    / 4
                    
        pressure = set_bound(pressure, 0)
    for i in range(1, config.SIZE+1):
        for j in range(config.SIZE+1):
            u[i][j] -= 0.5 * (pressure[i+1][j] - pressure[i-1][j]) / h
            v[i][j] -= 0.5 * (pressure[i][j+1] - pressure[i][j-1]) / h
    u = set_bound(u, 1)
    v = set_bound(v, 2)
    return u, v
    
    
def diffusion(N, b, x, x0):
    a = config.DELTATIME * config.DIFFUSION_FACTOR * N * N
    for k in range(config.ITERATION):
        for i in range(1, config.SIZE+1):
            for j in range(1, config.SIZE+1):
                x[i, j] = (x0[i, j] + a * (x[i-1, j] + x[i+1, j] + x[i, j-1] + x[i, j+1])) / (1 + 4*a)
        set_bound(N, b, x)
            

def advection(N, b, d, d0, u, v):
    dt0 = N*config.DELTATIME
    for i in range(1, config.SIZE+1):
        for j in range(1, config.SIZE+1):
            x = i - dt0 * u[i, j]
            y = j - dt0 * v[i, j]
            if x < 0.5:
                x = 0.5
            elif x > config.SIZE + 0.5:
                x = config.SIZE + 0.5
            if y < 0.5:
                y = 0.5
            elif y > config.SIZE + 0.5:
                y = config.SIZE + 0.5
                
            i0 = int(x)
            i1 = int(x) + 1
            j0 = int(y)
            j1 = int(y) + 1
            
            s1 = x - i0
            s0 = 1.0 - s1
            t1 = y - j0
            t0 = 1.0 - t1
            
            d[i, j] = s0 * (t0 * d0[i0, j0] + t1 * d0[i0, j1]) + \
                      s1 * (t0 * d0[i1, j0] + t1 * d0[i1, j1])
    set_bound(N, b, d)                
    
            
            
def addSource(N, x, s):
    for x, y, a in s:
        x[x][y] += a * config.DELTATIME

def vel_step(N, u, v, u0, v0):
    addSource(N, u, u0)
    addSource(N, v, v0)
    u, u0 = u0, u
    diffusion(N, 1, u, u0)
    v, v0 = v0, v
    diffusion(N, 2, v, v0)
    project(N, u, v, u0, v0)
    u, u0, v, v0 = u0, u, v0, v
    advect(N, 1, u, u0, u0, v0)
    advect(N, 2, v, v0, u0, v0)
    project(N, u, v, u0, v0)
def den_step(N, x, x0, u, v):
    addsource(N, x, x0)
    x0, x = x, x0
    diffusion(N, 0, x, x0)
    x0, x = x, x0
    advect(N, 0, x, x0, u, v)


def update(N, den_prev, den, u_prev, u, v_prev, v):
    # vel step
    vel_step(N, u, v, u_prev, v_prev)
    # dense step
    den_step(N, den, den_prev, u, v)
