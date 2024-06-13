import util
import cv2
import numpy as np

arr = np.zeros((64, 64)).astype(np.float32)
for i in range(64):
    for j in range(64):
        if (i+j)%2 == 1:
            arr[i][j] = 1
while True:
    util.showArrayHeatmap(arr)
    if cv2.waitKey(10) == 27: # <Esc>
        break
 

cv2.destroyAllWindows()      