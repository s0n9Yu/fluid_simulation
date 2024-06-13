import numpy as np
import config
import math

Randomflow = 2 * np.random.random((config.SIZE+2, config.SIZE+2, 2)).astype(np.float32) - 1

for i in range(1, config.SIZE + 1):
    for j in range(1, config.SIZE + 1):
        Randomflow[i][j] = Randomflow[i][j] / np.linalg.norm(Randomflow[i][j])
        pass

