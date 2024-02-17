import numpy as np
import matplotlib.pyplot as plt

PIXEL_SIZE = 144



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

resized_image = scale_img2factor(img, 1/PIXEL_SIZE)

plt.imsave("idekbruh.jpeg", resized_image)