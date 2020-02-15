import cv2
import time
import numpy as np
import imutils

video = cv2.VideoCapture(0)
while True:
    check, frame = video.read()
    frame = imutils.resize(frame, width=600)
    #Mirrors the frame
    frame = cv2.flip(frame,1)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    
    
    #Setting up corresponding colors for the game
    color1low = np.array([17,100,100])
    color1high = np.array([37,255,255])
    
    color2low = np.array([100,120,125])
    color2high = np.array([120,255,200])
    
    
    csv = cv2.cvtColor(blurred,cv2.COLOR_RGB2HSV)
    mask1 = cv2.inRange(csv,color1low,color1high)
    mask1 = cv2.erode(mask1, None, iterations=2)
    mask1 = cv2.dilate(mask1, None, iterations=2)
    
    mask2 = cv2.inRange(csv,color2low,color2high)
    mask2 = cv2.erode(mask2, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)
    
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)
    
    cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)
    
    
    center1 = None
    center2 = None

    # only proceed if at least one contour was found
    if len(cnts1) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circble and
        # centroid
        c = max(cnts1, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center1 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center1, 5, (0, 0, 255), -1)
            
    if len(cnts2) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circble and
        # centroid
        c = max(cnts2, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center2 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center2, 5, (0, 0, 255), -1)
    
    if center1 != None:
        if center1[0]>300:
            print("right")
        else:
            print("left")
    cv2.imshow("original",frame)
    cv2.imshow("mask",mask1)
    cv2.imshow("mask2",mask2)
    
    key = cv2.waitKey(1)
    if key == ord("q"):
        break


video.release()
cv2.destroyAllWindows()