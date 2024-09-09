from controller import Robot,GPS,Camera
import cv2
import numpy as np
timeStep = 32
robot = Robot()
def nothing():
    pass
templateT = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\H.png', cv2.IMREAD_GRAYSCALE)

s1 = robot.getDevice("distance sensor1")
camera = robot.getDevice("camera_centre")
camera.enable(timeStep)
s1.enable(timeStep)
cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
cv2.createTrackbar('x', 'settings', 4,20, nothing)

cv2.createTrackbar('y', 'settings', 800,1000, nothing)
start = robot.getTime()
while robot.step(timeStep) != -1:
    sN1 = s1.getValue()/0.8*100
    print(sN1)
    i = cv2.getTrackbarPos('x','settings')
    threshold = cv2.getTrackbarPos('y','settings')
    frameT = cv2.cvtColor(np.frombuffer(camera.getImage(), np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    templateT=cv2.resize(templateT, (i,i), interpolation = cv2.INTER_AREA)
    w, h = templateT.shape[::-1]
    res = cv2.matchTemplate(cv2.cvtColor(frameT, cv2.COLOR_BGR2GRAY),templateT,cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt,(pt[0] + w, pt[1] + h),color, 5)
    cv2.imshow('frame',frameT)
