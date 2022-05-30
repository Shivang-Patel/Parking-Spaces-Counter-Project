##############################################

# This file will be used to train data to get the regions of interest
# Manually select the parking spaces on a pictures from any instance in the testing video


##############################################
import cv2
import pickle


# Initialising the dimensions of the rectangle over the parking space
width, height= 70, 30


# The selected parking spaces are saved in a text file so we open that file in case it exists in order to prevent overwriting and loading the existing details into a list
try:
    with open('CarParkPos', 'rb') as f:
            posList= pickle.load(f)
except:
    posList= []


# Left click will draw a rectangle from the point and add the details to posList and left click in the seleted area will remove the rectangle and the corresponding details from posList
def mouseClick(events, x, y, flags, params):
    if events== cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events== cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1= pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList,f)


# Reading the training image from the file and showing the rectangles
while True:
    img= cv2.imread('carParkImg.jpg')

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (0,0,255), 2)

    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mouseClick)
    cv2.waitKey(1)