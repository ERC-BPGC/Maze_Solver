import numpy as np
import matplotlib.pyplot as plt

PIXEL_SIZE = 144
THRESHOLD = 0.3


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
            img[i, j] = 1 if img[i, j] > threshold else 0
    
    return img



def scale_img2factor(target_img, factor):
    c_height, c_width, _ = target_img.shape
    t_height, t_width = int(c_height*factor), int(c_width*factor)

    new_img_arr = np.zeros(shape=(t_height, t_width, 3))

    for i in range(t_height):
        for j in range(t_width):
            new_img_arr[i , j, 0] = target_img.item((min(c_height-1, round(i/factor)), min(c_width-1, round(j/factor)), 0))
            new_img_arr[i , j, 1] = target_img.item((min(c_height-1, round(i/factor)), min(c_width-1, round(j/factor)), 1))
            new_img_arr[i , j, 2] = target_img.item((min(c_height-1, round(i/factor)), min(c_width-1, round(j/factor)), 2))
    
    return new_img_arr


img = plt.imread("abclol.jpeg")
img = img/255
height, width, _ = img.shape

final_img = scale_img2factor(img, 1/PIXEL_SIZE)
final_img = rgb2gray(final_img)
plt.imsave("idekbruh.jpeg", final_img, cmap = 'gray')
final_img_t = threshold(final_img, THRESHOLD)

plt.imsave("idekbruht.jpeg", final_img_t, cmap = 'gray')