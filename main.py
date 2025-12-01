import cv2
import numpy as np
import time
import HandTracking as ht
import autopy

# Install using pip install autopy

# TITLE Variables Declaration
pTime = 0  # Used to calculate frame rate
width = 640  # Width of Camera
height = 480  # Height of Camera
frameR = 100  # Frame Rate
smoothening = 8  # Smoothening Factor
prevx, prevy = 0, 0  # Previous coordinates
currx, curry = 0, 0  # Current coordinates

cap = cv2.VideoCapture(0)  # Getting video feed from the webcam
cap.set(3, width)  # Adjusting size
cap.set(4, height)

detector = ht.handDetector(maxHands=1)  # Detecting one hand at max
screenwidth, screenheight = autopy.screen.size()  # Getting the screen size

while True:
    success, img = cap.read()
    img = detector.findHands(img)  # Finding the hand
    lmlist, bbox = detector.findPosition(img)  # Getting position of hand
    
    if len(lmlist) != 0:
        x1, y1 = lmlist[8]  # Index finger tip
        x2, y2 = lmlist[12]  # Middle finger tip
        fingers = detector.fingersUp()  # Checking if fingers are upwards
        
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)  # Creating boundary box
        
        if fingers[1] == 1 and fingers[2] == 0:  # If fore finger is up and middle finger is down
            x3 = np.interp(x1, (frameR, width - frameR), (0, screenwidth))
            y3 = np.interp(y1, (frameR, height - frameR), (0, screenheight))
            currx = prevx + (x3 - prevx) / smoothening
            curry = prevy + (y3 - prevy) / smoothening
            autopy.mouse.move(screenwidth - currx, curry)  # Moving the cursor
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prevx, prevy = currx, curry
        
        if fingers[1] == 1 and fingers[2] == 1:  # If fore finger middle finger both are up
            length, img, lineInfo = detector.findDistance(8, 12, img)
            
            if length < 40:  # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()  # Perform Click
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow('Image', img)
    cv2.waitKey(1)
