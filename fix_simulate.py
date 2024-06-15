import numpy as np
import config
import util
from default_animation import getAcceleration, getSource
from default_animation import getAcceleration, getSource

def set_bound(N, b, x):
    for i in range(1, N+1):
        if b == 1:
            x[0][i] = -x[1][i]
            x[N+1][i] = -x[N][i]
        else:
            x[0][i] = x[1][i]
            x[N+1][i] = x[N][i]
        if b == 2:
            x[i][0] = -x[i][1]
            x[i][N+1] = -x[i][N]
        else:
            x[i][0] = x[i][1]
            x[i][N+1] = x[i][N]
            
    x[0][0] = 0.5 * (x[1][0] + x[0][1])
    x[0][N+1] = 0.5 * (x[1][N+1] + x[0][N])
    x[N+1][0] = 0.5 * (x[N][0] + x[N+1][1])
    x[N+1][N+1] = 0.5 * (x[N][N+1] + x[N+1][N])  
    

def project(N, u, v, p, div):
    h = 1.0 / N
    for i in range(1, N+1):
        for j in range(1, N+1):
            div[i, j] = -0.5 * h * (u[i+1, j] - u[i-1, j] + v[i, j+1] - v[i, j-1])
            p[i, j] = 0
    set_bound(N, 0, div)
    set_bound(N, 0, p)
    
    for k in range(config.ITERATION):
        for i in range(1, N+1):
            for j in range(1, N+1):
                p[i, j] = (div[i, j] + p[i-1, j] + p[i+1, j] + p[i, j-1] + p[i, j+1]) / 4
        set_bound(N, 0, p)
        
    for i in range(1, N+1):
        for j in range(1, N+1):
            u[i][j] -= 0.5 * (p[i+1, j] - p[i-1, j]) / h
            v[i][j] -= 0.5 * (p[i, j+1] - p[i, j-1]) / h
    set_bound(N, 1, u)
    set_bound(N, 2, v)
            
    
    
    
def diffusion(N, b, x, x0):
    a = config.DELTATIME * config.DIFFUSION_FACTOR * N * N
    for k in range(config.ITERATION):
        for i in range(1, N+1):
            for j in range(1, N+1):
                x[i, j] = (x0[i, j] + a * (x[i-1, j] + x[i+1, j] + x[i, j-1] + x[i, j+1])) / (1 + 4*a)
        set_bound(N, b, x)
            

def advect(N, b, d, d0, u, v):
    dt0 = N*config.DELTATIME
    for i in range(1, N+1):
        for j in range(1, N+1):
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
    for i in range(N+2):
        for j in range(N+2):
            x[i][j] += config.DELTATIME * s[i][j]

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
    addSource(N, x, x0)
    x0, x = x, x0
    diffusion(N, 0, x, x0)
    x0, x = x, x0
    advect(N, 0, x, x0, u, v)

def addVelocity(u, v, timestep):
    accu, accv = getAcceleration(timestep)
    u += accu
    v += accv

def addDensity(dens, timestep):
    adds = getSource(timestep)
    dens += adds
    
def update(N, den_prev, den, u_prev, u, v_prev, v, timestep):
    addDensity(den_prev, timestep)
    addVelocity(u_prev, v_prev, timestep)
    # vel step
    vel_step(N, u, v, u_prev, v_prev)
    # dense step
    den_step(N, den, den_prev, u, v)
