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
    lowerRed = np.array([100,150,125])
    higherRed = np.array([120,255,200])
    
    csv = cv2.cvtColor(blurred,cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(csv,lowerRed,higherRed)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    if center != None:
        if center[0]>300:
            print("right")
        else:
            print("left")
    cv2.imshow("original",frame)
    cv2.imshow("mask",mask)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break


video.release()
cv2.destroyAllWindows()