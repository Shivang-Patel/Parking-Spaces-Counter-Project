import cv2
import pickle
import cvzone
import numpy as np

cap= cv2.VideoCapture('carPark.mp4')


# Opening the file saved from the parking space picker and loading the files in a posList[]
with open('CarParkPos', 'rb') as f:
    posList= pickle.load(f)

width, height= 70, 30

# Function to check if the parking space is empty or not. It puts red and green rectangles over taken and free spaces. It also displays the fraction of empty spaces available
def checkParkingSpace(imgPro):
    freeSpace=0
    for pos in posList:
        x,y = pos
        # cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (0,0,255), 2)
        
        imgCrop= imgPro[y:y+height, x:x+width]
        count= cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x,y+height-10), scale=1, thickness=1, offset=0, colorR=(0,0,255))

        if count< 700:
            color= (0,255, 0)
            thickness=5
            freeSpace+= 1
        else:
            color= (0,0,255)
            thickness=1
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, thickness)
    cvzone.putTextRect(img, f'Free Spaces: {str(freeSpace)}/{str(len(posList))}', (50, 150), scale=9, thickness=11, offset=20, colorR=(0,0,0))
    # cv2.imshow('imgCrop', imgCrop)
    



while True:
    
    # Reading video frame by frame
    success, img= cap.read()
    # Processing the image to check for free spaces
    imgGray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur= cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold= cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian= cv2.medianBlur(imgThreshold, 5)
    kernel= np.ones((3,3), np.uint8)
    imgDilate= cv2.dilate(imgMedian, kernel, iterations=1)

    if cap.get(cv2.CAP_PROP_POS_FRAMES)== cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    checkParkingSpace(imgDilate)
    
    # Displaying frame by frame
    cv2.imshow('Image', img)
    # cv2.imshow('Blur', imgBlur)
    # cv2.imshow('Dilate', imgDilate)
    cv2.waitKey(1)
