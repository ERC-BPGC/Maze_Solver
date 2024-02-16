import numpy as np
import cv2 
import math
import serial
import random
import time
import tensorflow as tf
# from skimage import util

# from img2bitmap import pixelate


PIXELS_PER_GRID = 75

def scale_img2factor(target_img, factor):
    c_height, c_width, _ = target_img.shape
    t_height, t_width = int(c_height*factor), int(c_width*factor)

    new_img_arr = np.zeros(shape=(t_height, t_width, 3))
    img_arr_2 = np.zeros(shape=(t_height, t_width, 3))
    
    for i in range(t_height):
        for j in range(t_width):
            new_img_arr[i , j, 0] = target_img.item((min(c_height-1, round(i/factor)), min(c_width-1, round(j/factor)), 0))
            new_img_arr[i , j, 1] = target_img.item((min(c_height-1, round(i/factor)), min(c_width-1, round(j/factor)), 1))
            new_img_arr[i , j, 2] = target_img.item((min(c_height-1, round(i/factor)), min(c_width-1, round(j/factor)), 2))
            img_arr_2[i,j,0] = 1
            img_arr_2[i,j,1] = 1
            img_arr_2[i,j,2] = 1
            
            
    for i in range(t_height-10):
        for j in range(t_width-10):        
            if (new_img_arr[i, j ,0] > 150/255) and (new_img_arr[i,j,1] < 100) and (new_img_arr[i,j,2] < 100/255):
                for a in range (10):
                    img_arr_2[i,j,0] = 0
                    img_arr_2[i,j,1] = 1
                    img_arr_2[i,j,2] = 1
                    img_arr_2[i-a,j-a,0] = 0
                    img_arr_2[i-a,j-a,1] = 1
                    img_arr_2[i-a,j-a,2] = 1
                    img_arr_2[i+a,j+a,0] = 0
                    img_arr_2[i+a,j+a,1] = 1
                    img_arr_2[i+a,j+a,2] = 1
            
            
                    

    
    return new_img_arr, img_arr_2


    


def grayscale (pic):
    imgray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    ret, pic = cv2.threshold(imgray, 127, 255, 0, cv2.THRESH_BINARY)
    cv2.imshow('grayscale', pic)
  
    return(pic)



vid = cv2.VideoCapture(0)
while (True):
    
    ret, frame = vid.read() 

    # frame = frame[20:415, 20:618]


    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    height, width, _ = rgb_img.shape
    new_frame = np.zeros(shape = (height, width, 3))
    # frame = (255-frame)
    cv2.imshow('abcd',frame)
    frame = frame.astype(float) / 255
    # abc, pixelated = scale_img2factor(frame, 144)
    # cv2.imshow('abcdefg',pixelated)
    frame, frame_2 = scale_img2factor(frame, 1/PIXELS_PER_GRID)
    frame, frame_2 = scale_img2factor(frame, PIXELS_PER_GRID)
    frame = frame.astype(float) * 255
    frame = frame.astype(np.uint8)
    # frame_2 = frame_2.astype(float) * 255
    # frame_2 = frame_2.astype(np.uint8)
    np.clip(frame, 0, 255)
    # np.clip(frame_2, 0, 255)
    cv2.imshow('abcde',frame)
    frame_3 = grayscale(frame)
    # print(type(frame_3))
    '''
    maze_tensor = tf.convert_to_tensor(frame_3, dtype=tf.float32)
   

# # Expand the dimensions of the tensor to match [batch_size, height, width, channels]
    maze_tensor_expanded = tf.expand_dims(maze_tensor, axis=-1)  # Add a channel dimension

#     # Expand the dimensions again to make batch size 1
    maze_tensor_expanded = tf.expand_dims(maze_tensor_expanded, axis=0)  

#     # Perform max pooling
    # pooling_result = tf.nn.max_pool2d(maze_tensor_expanded, ksize=(7, 7), strides=(7, 7), padding='SAME')
    pooling_result = tf.keras.layers.MaxPooling2D(pool_size=(3,3), strides=(3,3), padding='valid')(maze_tensor_expanded)
    # output_array = average_pooling(maze_tensor)
#     # Remove the batch dimension
    pooled_array = tf.squeeze(pooling_result, axis=0)
#     print(pooled_array.shape)
    

    pooled_array_numpy = pooled_array.numpy()

#     # frame_4 = better_gray(frame, 1)
    pooled_array_numpy_scaled = (pooled_array_numpy * 255).astype(np.uint8)
    '''
    frame_3=frame_3[0:450,0:600]
    print(frame_3.shape)
    height, width = frame_3.shape
# Display the pooled array as an image using OpenCV
    '''cv2.imshow('Pooled Array', pooled_array_numpy_scaled)
    python_list = pooled_array_numpy_scaled.reshape(height,width)
    python_list = python_list.tolist()
    cv2.waitKey(10000)
    t1=time.time()
    print(t1)
    class node:
        def __init__(self,col,row):
            self.row=row
            self.col=col
            self.gval=0
            self.hval=0
            self.obs=False
            self.parent=None
            self.goal=False

        def _repr_(self):
            return f"node(row={self.row}, col={self.col}, gval={self.gval}, hval={self.hval}"
    x_lim=(height-1)
    y_lim=(width-1)
    goal_point=node(x_lim,y_lim)
    goal_point.goal=True
    open_list=[]
    closed=[]
    start_point=node(0,0)
    start_point.hval=math.sqrt((start_point.col-goal_point.col)*(start_point.col-goal_point.col)+(start_point.row-goal_point.row)*(start_point.row-goal_point.row))
    solved=False
    open_list.append(start_point)
    # def generate_random_binary_matrix(rows, cols, probability_of_one):
    #     return [[1 if random.random() < probability_of_one else 0 for _ in range(cols)] for _ in range(rows)]
    
    obstacle_matrix= python_list
    obstacle_matrix[0][0]=0
    obstacle_matrix[x_lim][y_lim]=0
    for row in obstacle_matrix:
        print(row)

    def pickcurrent():
        w=None
        c=math.inf
        for a in open_list:
            b=a.gval+a.hval
            if b<c:
                c=b
                w=a
        return w
    def findneighbours(h):
        print(h)
        x=h.row
        y=h.col
        nearby=[]
        if x!=0 and y!=0 and x!=x_lim and y!=y_lim:
            #nearby.append(node(y+1,x+1))
            nearby.append(node(y,x+1))
            nearby.append(node(y+1,x))
            #nearby.append(node(y-1,x+1))
            #nearby.append(node(y+1,x-1))
            #nearby.append(node(y-1,x-1))
            nearby.append(node(y,x-1))
            nearby.append(node(y-1,x))
        elif x==0 and 0<y<y_lim:
            nearby.append(node(y,x+1))
            nearby.append(node(y+1,x))
            nearby.append(node(y-1,x))
            #nearby.append(node(y + 1, x + 1))
            #nearby.append(node(y - 1, x + 1))
        elif y==0 and 0<x<x_lim:
            #nearby.append(node(y + 1, x + 1))
            nearby.append(node(y, x + 1))
            nearby.append(node(y + 1, x))
            #nearby.append(node(y + 1, x - 1))
            nearby.append(node(y, x - 1))
        elif x==x_lim and 0<y<y_lim:
            nearby.append(node(y + 1, x))
            #nearby.append(node(y + 1, x - 1))
            #nearby.append(node(y - 1, x - 1))
            nearby.append(node(y, x - 1))
            nearby.append(node(y - 1, x))
        elif y==y_lim and 0<x<x_lim:
            nearby.append(node(y, x + 1))
            #nearby.append(node(y - 1, x + 1))
            #nearby.append(node(y - 1, x - 1))
            nearby.append(node(y, x - 1))
            nearby.append(node(y - 1, x))
        elif x==0 and y==0:
            nearby.append(node(y + 1, x))
            nearby.append(node(y, x + 1))
            #nearby.append(node(y + 1, x + 1))
        elif x==0 and y==y_lim:
            nearby.append(node(y, x + 1))
            #nearby.append(node(y - 1, x + 1))
            nearby.append(node(y - 1, x))
        elif x==x_lim and y==0:
            nearby.append(node(y + 1, x))
            #nearby.append(node(y + 1, x - 1))
            nearby.append(node(y, x - 1))
        else:
            nearby.append(node(y, x - 1))
            nearby.append(node(y - 1, x))
            #nearby.append(node(y - 1, x - 1))
        return nearby
    def findgval(o,p):
        if o.row==p.row:
            j=p.gval+10
        elif o.col==p.col:
            j= p.gval + 10
        else:
            j=p.gval+math.sqrt(2)*10
        return j

    def findhval(o):
        a=o.row
        b=o.col
        h=math.sqrt((x_lim-a)*(x_lim-a)+(y_lim-b)*(y_lim-b))*10
        return h
    c=0
    rob_size = 2
    # def check_obstacle(d):
    #     for i in range(d.row - rob_size, d.row):
    #         for j in range(d.col - rob_size, d.col):
    #             # Check if the current cell is within the range of the robot's size
    #             if abs(i - d.row) <= rob_size and abs(j - d.col) <= rob_size:
    #                 # Check for obstacles only if the cell is within the square region
    #                 if obstacle_matrix[i][j] == 1:
    #                     return True
    #     return False
    def check_obstacle(d):
        a=d.col
        b=d.row
        if obstacle_matrix[b][a]==1:
            return True
        else:
            return False
    while solved==False:
        current=pickcurrent()
        for i in range(len(open_list)):
            if open_list[i] == current:
                open_list.pop(i)
                break

        print(c,current)
        c+=1
        closed.append(current)
        neighbours=findneighbours(current)
        for d in neighbours:
            if check_obstacle(d)==True or any(cell.row == d.row and cell.col == d.col for cell in closed):
                continue
            if findgval(d,current)<d.gval or not any(cell.row == d.row and cell.col == d.col for cell in open_list):
                d.gval=findgval(d,current)
                d.hval=findhval(d)
                d.parent=current
                
                print(d.gval,d.hval,d.row,d.col,check_obstacle(d))
                if d.hval==0:
                    goal_point.parent=d
                    solved=True
                    break
                if d not in open_list:
                    open_list.append(d)
    path = []
    current = goal_point

    visual = obstacle_matrix


    while current != start_point:
        path.append([current.row , current.col])
        current = current.parent

    path.append([start_point.row , start_point.col])
    path.reverse()'''
    '''
    for i in path:
        visual[i[0]][i[1]] = 2

    for i in visual:
        print(i)
    '''
    # print(path)

    '''
    Row is increasing -> forward
    Column is increasing -> left
    '''

    '''dir = []

    for i in range(1 , len(path)-1):
        if path[i][0] > path[i - 1][0]:
            dir.append(b"F")
        elif path[i][0] < path[i - 1][0]:
            dir.append(b"B")

        if path[i][1] > path[i - 1][1]:
            dir.append(b"L")
        elif path[i][1] < path[i - 1][1]:
            dir.append(b"R")
    if solved==True:
        t2=time.time()
        print(t2-t1)
    print(dir)'''

    '''
    port = "COM4"
    bluetooth = serial.Serial(port , 9600)
    print("Works")
    bluetooth.flushInput()

    for i in dir:
        bluetooth.write(str.encode(i))
        time.sleep(2)

    bluetooth.close()
    print("Done")
    '''

    # with serial.Serial('/dev/ttyS1' , 9600  , timeout = 1) as ser:
    #     for i in dir:
    #         ser.write(i)
    #         time.sleep(2)
    #     ser.close()


        # cv2.imshow('123', frame)
        # cv2.imshow('xyz', frame_2)
        # cv2.imshow('abc',frame_3)

        #cv2.imwrite('xyz'+str(i)+str(i)+'.jpg', frame)
        
        # cv2.waitKey(200)

        

 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
       break

vid.release() 
cv2.destroyAllWindows() 