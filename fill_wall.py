import matplotlib.pyplot as plt
import numpy as np
import random
import time

MIN_DIST = 35

def sqr_dist(arr1, arr2):
    return (arr1[0] - arr2[0])**2 + (arr1[1] - arr2[1])**2

height = 720
width = 1280

init_maze = np.zeros(shape=(height, width, 3))

source_list = []

# ------------ test random points
for _ in range(100):
    _x = random.randrange(0, height)
    _y = random.randrange(0, width)

    init_maze[_x, _y] = np.array((1, 1, 1))

    source_list.append(np.array((_x, _y)))


# ---------------- actual program
padding = MIN_DIST // 2

_stop_o = padding + 1 if MIN_DIST & 1 else padding
for coords in source_list:
    for _i in range(coords[0] - padding, coords[0] + _stop_o):
        for _j in range(coords[1] - padding, coords[1] + _stop_o):
            if(0 < _i < height and 0 < _j < width):
                init_maze[_i, _j] = np.array((1, 1, 1))
    




plt.imsave("rfrfr.png", init_maze)
