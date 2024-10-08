from controller import Robot,GPS,Camera,InertialUnit
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
def colorRec():
    if(sensColor[0] == black[0] and sensColor[1] == black[1] and sensColor[2] == black[2]):
        print("BLACK)))")
        recognizedColor = 'black'
        mapList[zCell][xCell] = '2'
    elif(sensColor[0] == green[0] and sensColor[1] == green[1] and sensColor[2] == green[2]):
        print("green")
        recognizedColor = 'green'
        mapList[zCell][xCell] = '9'
    elif(sensColor[0] == red[0] and sensColor[1] == red[1] and sensColor[2] == red[2]):
        print("red")
        recognizedColor = 'red'
        mapList[zCell][xCell] = '8'
    elif(sensColor[0] >= silverMin[0] and sensColor[1] >= silverMin[1] and sensColor[2] >= silverMin[2] and sensColor[0] <= silverMax[0] and sensColor[1] <= silverMax[1] and sensColor[2] <= silverMax[2]):
        print("silver")
        recognizedColor = 'silver'
        mapList[zCell][xCell] = '4'
    elif(sensColor[0] == brown[0] and sensColor[1] == brown[1] and sensColor[2] == brown[2]):
        print("brown")
        recognizedColor = 'brown'
        mapList[zCell][xCell] = '3'
    elif(sensColor[0] == blue[0] and sensColor[1] == blue[1] and sensColor[2] == blue[2]):
        print("blue")
        recognizedColor = 'blue'
        mapList[zCell][xCell] = '6'
    elif(sensColor[0] == purple[0] and sensColor[1] == purple[1] and sensColor[2] == purple[2]):
        print("purple")
        recognizedColor = 'purple'
        mapList[zCell][xCell] = '7'
    else:
        #print("None")
        recognizedColor = 'none'
recognizedCamera = 4
def templateRec():
    global recognizedCamera
    recognizedCamera = 4
    leastScale = 30
    for t in range(6):
        if(t==0):
            templateT = templateU
            text = 'U'
            color = (255,0,0)
        if(t==1):
            templateT = templateH
            text = 'H'
            color = (0,255,0)
        if(t==2):
            templateT = templateS
            text = 'S'
            color = (0,0,255)
        if(t==3):
            templateT = templateCOR
            text = 'C'
            color = (0,255,255)
        if(t==4):
            templateT = templateOP
            text = 'O'
            color = (255,0,255)
        if(t==5):
            templateT = templateFG
            text = 'F'
            color = (255,255,0)
        if(t==6):
            templateT = templatePOI
            text = 'P'
            color = (255,0,0)
            
        for i in 27,23,17,14,10:
            templateT=cv2.resize(templateT, (i,i), interpolation = cv2.INTER_AREA)
            w, h = templateT.shape[::-1]
            for j in range(3):
                if(j==0):
                    frameT = frame
                elif(j==1):
                    frameT = frameR
                elif(j==2):
                    frameT = frameL
                res = cv2.matchTemplate(cv2.cvtColor(frameT, cv2.COLOR_BGR2GRAY),templateT,cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)
                recognizedSighn = 'none'
                for pt in zip(*loc[::-1]):
                    print(text)
                    recognizedSighn = text
                    mapList[zCell][xCell] = text
                    recognizedCamera = j
                    if(leastScale>i):leastScale = i
                    posX = int(gps.getValues()[0] * 100)
                    posZ = int(gps.getValues()[2] * 100)
                    message = struct.pack("i i c", posX, posZ, bytes(text, "utf-8"))
                    print('reported!')
                    emitter.send(message)
    print(leastScale)
    print(recognizedSighn)  
    print(recognizedCamera)
           
while robot.step(timeStep) != -1:
    #reading and normalising distance sensors
    
    sN1 = s1.getValue()/0.8*100
    sN2 = s2.getValue()/0.8*100
    sN3 = s3.getValue()/0.8*100
    if(robot.getTime()%1 == 0):print(".")

    #gps read
    x = int(gps.getValues()[0]*100)
    z = int(gps.getValues()[2]*100)
    if(onStart): 
        onStart = False
        startX = round(x/cellPerCoord)
        startZ = round(z/cellPerCoord)
    xCell = round(x/cellPerCoord) - startX
    zCell = round(z/cellPerCoord) - startZ
    xCellRaw = x/cellPerCoord
    zCellRaw = z/cellPerCoord
    if(xCell>len(mapList[0])-startPosX-1):
        expandRight()
        print("expanded right")
    if(xCell<-startPosX):
       expandLeft()
       startPosX+=1
       print("expanded left")
    if(zCell>len(mapList)+startPosZ-1):
        expandDown()
        print("expanded down")
    if(zCell<-startPosZ):
       expandUp()
       startPosZ+=1
       print("expanded up")
    
    #rgb read
    imageRGBSensor = scolor.getImage()
    sensColor = [scolor.imageGetRed(imageRGBSensor, 1, 0, 0),scolor.imageGetGreen(imageRGBSensor, 1, 0, 0),scolor.imageGetBlue(imageRGBSensor, 1, 0, 0)]
    colorRec()
    #marking passed cells
    # if(mapList[zCell][xCell] == '0'):
    #     mapList[zCell][xCell] = '█'
    #printing mapList
    # for i in range(len(mapList)):
    #     print(mapList[i])
    #settings read
    k1 = cv2.getTrackbarPos('x','settings')
    k2=10*k1
    threshold = cv2.getTrackbarPos('y','settings')/1000+0.001
    targetLength= cv2.getTrackbarPos('scale','settings')/100
    #reading camera frames
    frame = cv2.cvtColor(np.frombuffer(camera.getImage(), np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    frameR = cv2.cvtColor(np.frombuffer(cameraR.getImage(), np.uint8).reshape((cameraR.getHeight(), cameraR.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    frameL = cv2.cvtColor(np.frombuffer(cameraL.getImage(), np.uint8).reshape((cameraL.getHeight(), cameraL.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    #
    min_p = (0, 0, 150)
    max_p = (215, 215, 215)
    # применяем фильтр, делаем бинаризацию
    img_g = cv2.inRange(frame, min_p, max_p)

    cv2.imshow('img', img_g)
    frameN = cv2.bitwise_and(frame, frame, mask = img_g)
    frameN = cv2.cvtColor(frameN, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(frameN, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    signN = 'none'
    minArea = 100000
   
    for i in contours:
        
        try:
            pixelColor = frame[i[0][0][1],i[0][0][0]-1]
            pixelColor2 = frame[i[3][0][1]+1,i[3][0][0]]
        except:
            pixelColor  = [0,0,0]
            pixelColor2 = [0,0,0]
        if(i[0][0][0] != 0 and 
           ((pixelColor[0] == 32 and pixelColor[1] == 30 and pixelColor[2] == 18) or (pixelColor[0] == 139 and pixelColor[1] == 127 and pixelColor[2] == 61))
           and ((pixelColor2[0] == 32 and pixelColor2[1] == 30 and pixelColor2[2] == 18) or (pixelColor2[0] == 139 and pixelColor2[1] == 127 and pixelColor2[2] == 61))):
            cv2.drawContours(frame, i, -1, (0,255,0), 1)
          
    
    cv2.imwrite(r"C://Users//TBG//Documents//frame.png",frame)


    
    speed1 = 0
    speed2 = 0

    #templateRec()
    if(recognizedCamera == 2):
        turnRightTimer = robot.getTime()
    if(robot.getTime()<turnRightTimer+turnTimer):
        speed1 = -3.14
        speed2 = 3.14
    if(recognizedCamera == 1):
        turnLeftTimer = robot.getTime()
    if(robot.getTime()<turnLeftTimer+turnTimer):
        speed1 = 3.14
        speed2 = -3.14
    if(recognizedCamera == 0):
        goForwardTimer = robot.getTime()
    if(robot.getTime()<goForwardTimer+0.4):
        speed1 = 0
        speed2 = 0
        
        
        
    #failsave
    # if(z == zOld and x == xOld): cntStop+=1
    # else: cntStop = 0
    # if(cntStop>100):
    #     goBackTime = robot.getTime()
    # if(robot.getTime() < goBackTime + 0.6):
    #     speed1 = -6.28
    #     speed2 = -6.28
    # if(robot.getTime() > goBackTime + 0.6):
    #     goBackTime = 0
    # xOld = x
    # zOld = z
    #black hole  

    #random
    # if(int(robot.getTime()) % 50 ==0):kMod = random.choice([1,-1])
    # if(int(robot.getTime())%10==0 and random.randint(0,9)==5):
    #     wall = True
    #     wallTime = robot.getTime()
    #recognizing signs
    
    
    wheel1.setVelocity(speed1)              
    wheel2.setVelocity(speed2)
    #print(mapList)
    #imshow
    cv2.imshow("frame", frame)
    cv2.imshow("frameR", frameR)
    cv2.imshow("frameL", frameL)
    cv2.imshow("MAP", mapping_img)
    
