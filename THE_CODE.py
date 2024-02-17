import numpy as np
import cv2 
import math
import serial
import random
import time
import tensorflow as tf
import matplotlib.pyplot as plt
# from skimage import util

# from img2bitmap import pixelate

PIXEL_SIZE = 60
THRESHOLD = 0.3

def arduino(data):
    try:
        print("Connecting to arduino")
        # Replace 'COM9' with the actual COM port of your Arduino
        with serial.Serial('COM9', 9600, timeout=1) as ser:
            time.sleep(2)  # Wait for the Arduino to initialize (increased to 2 seconds)
            ser.write(str(data).encode())
        print(f"Sent data to Arduino: {data}")

    except Exception as e:
        print(f"Error: {e}")

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

vid = cv2.VideoCapture(0)
while True:
    pic = cv2.imread(vid)



    img = plt.imread("abclol.jpeg")
    img = img/255
    height, width, _ = img.shape

    final_img = scale_img2factor(img, 1/PIXEL_SIZE)

    final_img = rgb2gray(final_img)
    plt.imsave("idekbruh.jpg", final_img, cmap = 'gray')
    final_img_t = threshold(final_img, THRESHOLD)

    plt.imsave("idekbruht.jpg", final_img_t, cmap = 'gray')
    height, width = final_img_t.shape
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

    obstacle_matrix= final_img_t
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
    path.reverse()
    '''
    for i in path:
        visual[i[0]][i[1]] = 2

    for i in visual:
        print(i)
    '''
    print(path)

    '''
    Row is increasing -> forward
    Column is increasing -> left
    '''

    dir = []

    for i in range(1 , len(path)-1):
        if path[i][0] > path[i - 1][0]:
            dir.append("F")
        elif path[i][0] < path[i - 1][0]:
            dir.append("B")

        if path[i][1] > path[i - 1][1]:
            dir.append("LF")
        elif path[i][1] < path[i - 1][1]:
            dir.append("RF")
    if solved==True:
        t2=time.time()
        print(t2-t1)
    dir = dir.tostring()
    print(dir)

    for char in dir:
        if char.lower() == 'f':
            arduino('7')  # Pass the command as a string
        elif char.lower() == 'b':
            arduino('6')  # Pass the command as a string
        elif char.lower() == 'l':
            arduino('5')  # Pass the command as a string
        elif char.lower() == 'r':
            arduino('4')  # Pass the command as a string
        elif char.lower() == 's':
            arduino('3')  # Pass the command as a string
        time.sleep(0.3)  # Introduce a small delay between commands to avoid potential issues


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

        

    key = cv2.waitKey(0)
    if key ==ord('q'):
        break
vid.release() 
cv2.destroyAllWindows() 