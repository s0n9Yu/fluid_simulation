import numpy as np
import config
import math

Circularflow = 2 * np.random.random((config.SIZE+2, config.SIZE+2, 2)).astype(np.float32) - 1

for i in range(1, config.SIZE + 1):
    for j in range(1, config.SIZE + 1):
        X = (j - config.SIZE // 2) / config.SIZE
        Y = (i - config.SIZE // 2) / config.SIZE
        if math.sqrt(X**2+Y**2) != 0:
            Y, X = -X/math.sqrt(X**2+Y**2), Y/math.sqrt(X**2+Y**2)
        Circularflow[i][j] = np.array([X, Y], np.float32)
        Circularflow[i][j] = 3 * Circularflow[i][j]
        pass

