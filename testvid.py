import numpy as np
import cv2 
# from skimage import util

# from img2bitmap import pixelate


# PIXELS_PER_GRID = 1

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


### To take input image, blur it to reduce noise and then grayscale it (also save it)
### Issues- Noise from shadows not completely removed/dependent on light. (Threshhold changes were useful so may be fixed after IRL Test)
def grayscale (pic):
    imgray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    ret, pic = cv2.threshold(imgray, 127, 255, 0, cv2.THRESH_BINARY)
    cv2.imshow('grayscale', pic)
  
    return(pic)


vid = cv2.VideoCapture(0)
while (True):
      
    
    ret, frame = vid.read() 

    # h, w, d = frame.shape
    # print(h, w ,d)

  
    # print(frame)
    # break
   
    cv2.imshow('frame', frame) 
    # cv2.imwrite('xyz'+str(i)+'.jpg', frame)

    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    height, width, _ = rgb_img.shape
    new_frame = np.zeros(shape = (height, width, 3))

    '''#for i in range(height):
        for j in range(width):
            r_color = rgb_img[i, j, 0]
            g_color = rgb_img[i, j, 1]
            b_color = rgb_img[i, j, 2]
            if (r_color > 190) and (g_color < 170) and (b_color < 170):
                new_frame[i, j, 2] = r_color # for displaying, use BGR, for processing, use RGB
    
    # rgb_img = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
'''
    # cv2.imshow('frame xy', new_frame)

    # new_frame = pixelate(frame, PIXELS_PER_GRID)
    frame = frame.astype(float) / 255
    frame = scale_img2factor(frame, 1/20)
    frame = scale_img2factor(frame, 20)
    frame = frame.astype(float) * 255
    frame = frame.astype(np.uint8)
    np.clip(frame, 0, 255)
    # new_frame = scale_img2factor(frame, 2)
    
    # frame = grayscale(frame)
    cv2.imshow('123', frame)
    #cv2.imwrite('xyz'+str(i)+str(i)+'.jpg', frame)
    
    # cv2.waitKey(200)

    

 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
       break

vid.release() 
cv2.destroyAllWindows() 