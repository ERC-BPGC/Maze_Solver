import matplotlib.pyplot as plt
import numpy as np
import time

PIXELS_PER_GRID = 25
THRESHOLD = 0.95
 

def pixelate(img, pixelate_amount):

    height, width, _ = img.shape

    padding = pixelate_amount//2

    new_img_arr = np.zeros(shape=(height, width, 3))

    for i in range(padding, height + padding, pixelate_amount):
        for j in range(padding, width + padding, pixelate_amount):

            # finding average color
            _stop = (padding + 1) if pixelate_amount & 1 else padding # in grid

            total_pixels = 0
            r_total = 0
            g_total = 0
            b_total = 0
            
            for _i in range(-padding, _stop):
                for _j in range(-padding, _stop):
                    
                    _x = i + _i
                    _y = j + _j

                    if 0<= _x < height and 0 <= _y < width: # and (_x, _y) != (i, j):
                        r_total += img.item((_x, _y, 0))
                        g_total += img.item((_x, _y, 1))
                        b_total += img.item((_x, _y, 2))
                        total_pixels += 1
            
            color = np.array((r_total, g_total, b_total)) / total_pixels

            # applying color to all pixels
            for _i in range(-padding, _stop):
                for _j in range(-padding, _stop):
                    
                    _x = i + _i
                    _y = j + _j

                    if 0<= _x < height and 0 <= _y < width: # and (_x, _y) != (i, j):
                            new_img_arr[_x, _y] = color

    return new_img_arr

def rgb2gray(img):
    height, width, _ = img.shape
    gray_img_arr = np.zeros(shape=(height, width))

    for i in range(height):
        for j in range(width):
            r_gray = img.item((i, j, 0)) * 0.299
            g_gray = img.item((i, j, 1)) * 0.587
            b_gray = img.item((i, j, 2)) * 0.114

            gray_img_arr[i, j] = r_gray + g_gray + b_gray

    return gray_img_arr

def threshold(img, threshold):
    height, width = img.shape

    for i in range(height):
        for j in range(width):
            img[i, j] = 0 if img[i, j] > threshold else 1
    
    return img

def compress_img(img, pixelate_amt):
    height, width = img.shape

    new_img_arr = np.zeros(shape=(height//pixelate_amt, width//pixelate_amt))

    for i in range(0, height, pixelate_amt):
        for j in range(0, width, pixelate_amt):
            new_img_arr[int(i/pixelate_amt), int(j/pixelate_amt)] = img[i, j]

    return new_img_arr


def process(img, pixelate_amount, threshold):
    height, width, _ = img.shape

    padding = pixelate_amount//2

    new_img_arr = np.zeros(shape=(height//pixelate_amount, width//pixelate_amount))

    for i in range(padding, height + padding, pixelate_amount):
        for j in range(padding, width + padding, pixelate_amount):

            # finding average color
            _stop = (padding + 1) if pixelate_amount & 1 else padding # in grid

            total_pixels = 0
            r_total = 0
            g_total = 0
            b_total = 0
            
            for _i in range(-padding, _stop):
                for _j in range(-padding, _stop):
                    
                    _x = i + _i
                    _y = j + _j

                    if 0<= _x < height and 0 <= _y < width: 
                        r_total += img.item((_x, _y, 0))
                        g_total += img.item((_x, _y, 1))
                        b_total += img.item((_x, _y, 2))
                        total_pixels += 1
            
            color = 0 if ((r_total * 0.299 + g_total * 0.587 + b_total * 0.114) / total_pixels) > threshold else 1

            new_img_arr[i//pixelate_amount, j//pixelate_amount] = color
    
    return new_img_arr


# s0 = "maze.png"
# s1 = "maze1.png"
# s2 = "maze2.png"

# img_arr = [s0, s1, s2]

# start_time = time.time()

# for i in img_arr:
#     # img1 = plt.imread(i)
#     # img = pixelate(img1, PIXELS_PER_GRID)
#     # img = rgb2gray(img)
#     # img = threshold(img, THRESHOLD)
#     # img = compress_img(img, PIXELS_PER_GRID)
#     # plt.imsave("finished" + i, img, cmap = 'gray')

#     img1 = plt.imread(i)
#     fimg = process(img1, PIXELS_PER_GRID, THRESHOLD)
#     plt.imsave("finished" + i, process(img1, PIXELS_PER_GRID, THRESHOLD), cmap = 'gray')



# print(time.time() - start_time)
