from controller import Robot,GPS,Camera,Emitter
import cv2
import numpy as np
import random
import struct
timeStep = 32
max_velocity = 6.28
robot = Robot()
def nothing():
    pass

#wheels setup
wheel1 = robot.getDevice("wheel1 motor")
wheel2 = robot.getDevice("wheel2 motor") 
wheel1.setPosition(float("inf"))       
wheel2.setPosition(float("inf"))

#sensors setup
s0 = robot.getDevice("distance sensor0")
s1 = robot.getDevice("distance sensor1")
s2 = robot.getDevice("distance sensor2")
s3 = robot.getDevice("distance sensor3")
scolor = robot.getDevice("colour_sensor")
camera = robot.getDevice("camera_centre")
cameraR = robot.getDevice("camera_left")
cameraL = robot.getDevice("camera_right")
gps = robot.getDevice("gps sensor")
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
imu = robot.getDevice("inertial_unit")

#enabling sensors
s1.enable(timeStep)
s2.enable(timeStep)
s3.enable(timeStep)
scolor.enable(timeStep)
camera.enable(timeStep)
cameraR.enable(timeStep)
cameraL.enable(timeStep)
gps.enable(timeStep)
receiver.enable(timeStep)
imu.enable(timeStep)
#windows setup
cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
cv2.createTrackbar('x', 'settings', 4,20, nothing)
cv2.createTrackbar('y', 'settings', 800,1000, nothing)
cv2.createTrackbar('scale', 'settings', 6,10, nothing)
start = robot.getTime()

#templates setup

templateU = cv2.imread('C://Users//TBG//Documents//robocup rescue maze simulation//U.png', cv2.IMREAD_GRAYSCALE)
templateH = cv2.imread('C://Users//TBG//Documents//robocup rescue maze simulation//H.png', cv2.IMREAD_GRAYSCALE)
templateS = cv2.imread('C://Users//TBG//Documents//robocup rescue maze simulation//S.png', cv2.IMREAD_GRAYSCALE)
templateCOR = cv2.imread('C://Users//TBG//Documents//robocup rescue maze simulation//COR.png', cv2.IMREAD_GRAYSCALE)
templateOP = cv2.imread('C://Users//TBG//Documents//robocup rescue maze simulation//OP.png', cv2.IMREAD_GRAYSCALE)
templateFG = cv2.imread('C://Users//TBG//Documents//robocup rescue maze simulation//FG.png', cv2.IMREAD_GRAYSCALE)
templatePOI = cv2.imread('C://Users//TBG//Documents//robocup rescue maze simulation//POI.png', cv2.IMREAD_GRAYSCALE)    
templateT = templateS


#map setup
mapping_img = np.zeros((100,100))
mapping_img = np.uint8(mapping_img)
mapping_img=cv2.cvtColor(mapping_img, cv2.COLOR_GRAY2BGR)
startX = 0
startZ = 0
startPosX = 0
startPosZ = 0
mapList = [['5']]
def expandRight():
    for i in range(len(mapList)):
        mapList[i].append('0')
def expandLeft():
    for i in range(len(mapList)):
        mapList[i].insert(0,'0')
def expandDown():
    addList = ['0']*len(mapList[0])
    mapList.append(addList)
def expandUp():
    addList = ['0']*len(mapList[0])
    mapList.insert(0,addList)
#variables
cellPerCoord = 3
black = [41,41,41]
blue = [63,63,252]
purple = [145,63,226]
brown = [209,175,101]
silverMin = [246,246,246]
silverMax = [252,252,252]
green = [33,249,33]
red = [252,63,63]
k1=10.0#p koeff
k2=50.0#d koeff
targetLength=0.06
err=0.0
errold=0.0
p=0.0
d=0.0
cntStop = 0
xOld = 0
zOld = 0
sN1 = 0
sN2 = 0
sN3 = 0
goBackTime = 0
blackTime = 0
onStart = True
wallBackTime = 0
kMod = 1
wallTime = 0
recognizedColor = ''
angleDeltaZ = 0
angleDeltaX = 0
angleStartX = 0
angleStartZ = 0
alpha = 0
angleTime = 0
defineAngle = True
speed1 = 0
speed2 = 0
mapShow = mapList
recognizedSighn = 'none'
lastRequestTime = robot.getTime()
turnRightTimer = 0
turnLeftTimer = 0
goForwardTimer = 0
turnTimer = 0.6
#color def

   
while robot.step(timeStep) != -1:
    #reading and normalising distance sensors
    
    sN1 = s1.getValue()/0.8*100
    sN2 = s2.getValue()/0.8*100
    sN3 = s3.getValue()/0.8*100
    if(robot.getTime()%1 == 0):print(".")

    k1 = cv2.getTrackbarPos('x','settings')
    k2=10*k1
    threshold = cv2.getTrackbarPos('y','settings')/1000+0.001
    targetLength= cv2.getTrackbarPos('scale','settings')/100
    #reading camera frames
    frame = cv2.cvtColor(np.frombuffer(camera.getImage(), np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    frameR = cv2.cvtColor(np.frombuffer(cameraR.getImage(), np.uint8).reshape((cameraR.getHeight(), cameraR.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    frameL = cv2.cvtColor(np.frombuffer(cameraL.getImage(), np.uint8).reshape((cameraL.getHeight(), cameraL.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    #
    hsv_min = np.array((53, 0, 0), np.uint8)
    hsv_max = np.array((83, 255, 255), np.uint8)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV )
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)
    cv2.imwrite(r"C://Users//TBG//Documents//frame.png",frame)

    wheel1.setVelocity(0)              
    wheel2.setVelocity(0)
    #imshow
    cv2.imshow("frame", frame)
    cv2.imshow("frameR", frameR)
    cv2.imshow("frameL", frameL)
    cv2.imshow("MAP", mapping_img)
    
