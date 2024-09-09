from controller import Robot,GPS,Camera
import cv2
import numpy as np
import random
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
s1 = robot.getDevice("distance sensor1")
s2 = robot.getDevice("distance sensor2")
s3 = robot.getDevice("distance sensor3")
scolor = robot.getDevice("colour_sensor")
camera = robot.getDevice("camera_centre")
cameraR = robot.getDevice("camera_left")
cameraL = robot.getDevice("camera_right")
gps = robot.getDevice("gps sensor")

#enabling sensors
s1.enable(timeStep)
s2.enable(timeStep)
s3.enable(timeStep)
scolor.enable(timeStep)
camera.enable(timeStep)
cameraR.enable(timeStep)
cameraL.enable(timeStep)
gps.enable(timeStep)

#windows setup
cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
cv2.createTrackbar('x', 'settings', 4,20, nothing)
cv2.createTrackbar('y', 'settings', 800,1000, nothing)
cv2.createTrackbar('scale', 'settings', 6,10, nothing)
start = robot.getTime()

#templates setup
if(False):
    templateU = cv2.imread('C:\\Users\\user\\Downloads\\robocup\\U.png', cv2.IMREAD_GRAYSCALE)
    templateH = cv2.imread('C:\\Users\\user\\Downloads\\robocup\\H.png', cv2.IMREAD_GRAYSCALE)
    templateS = cv2.imread('C:\\Users\\user\\Downloads\\robocup\\S.png', cv2.IMREAD_GRAYSCALE)
    templateCOR = cv2.imread('C:\\Users\\user\\Downloads\\robocup\\COR.png', cv2.IMREAD_GRAYSCALE)
    templateOP = cv2.imread('C:\\Users\\user\\Downloads\\robocup\\OP.png', cv2.IMREAD_GRAYSCALE)
    templateFG = cv2.imread('C:\\Users\\user\\Downloads\\robocup\\FG.png', cv2.IMREAD_GRAYSCALE)
    templatePOI = cv2.imread('C:\\Users\\user\\Downloads\\robocup\\POI.png', cv2.IMREAD_GRAYSCALE)
else:
    templateU = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\U.png', cv2.IMREAD_GRAYSCALE)
    templateH = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\H.png', cv2.IMREAD_GRAYSCALE)
    templateS = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\S.png', cv2.IMREAD_GRAYSCALE)
    templateCOR = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\COR.png', cv2.IMREAD_GRAYSCALE)
    templateOP = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\OP.png', cv2.IMREAD_GRAYSCALE)
    templateFG = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\FG.png', cv2.IMREAD_GRAYSCALE)
    templatePOI = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\POI.png', cv2.IMREAD_GRAYSCALE)    
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
cellPerCoord = 12
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
        print("None")
        recognizedColor = 'none'
def templateRec():
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
    print(leastScale)
    print(recognizedSighn)  
                        
while robot.step(timeStep) != -1:
    
    sN1 = s1.getValue()/0.8*100
    sN2 = s2.getValue()/0.8*100
    sN3 = s3.getValue()/0.8*100
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
    print(xCell,zCell)
    print(len(mapList[0]),len(mapList))
    print(startPosX,startPosZ)
    #rgb read
    imageRGBSensor = scolor.getImage()
    sensColor = [scolor.imageGetRed(imageRGBSensor, 1, 0, 0),scolor.imageGetGreen(imageRGBSensor, 1, 0, 0),scolor.imageGetBlue(imageRGBSensor, 1, 0, 0)]
    colorRec()
    if(mapList[zCell][xCell] == '0'):
        mapList[zCell][xCell] = '█'
    
    for i in range(len(mapList)):
        print(mapList[i])
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
    
    errold=err    
    err=targetLength-s1.getValue()
    
    p=err*k1
    d=0#(err-errold)*k2
    q=p+d
    
    speed1 = 0
    speed2 = 0
    #speed1 = 4.71-q
    #speed2 = 4.71+q
    if(speed1>max_velocity):speed1=max_velocity
    if(speed2>max_velocity):speed2=max_velocity
    if(speed1<-max_velocity):speed1=-max_velocity
    if(speed2<-max_velocity):speed2=-max_velocity
    #stenkaa
    if(s2.getValue()<0.06):
        wallTime = robot.getTime()
    if(robot.getTime() < wallTime + 0.3):
        speed1 = -3.14*kMod
        speed2 = 3.14*kMod
    if(robot.getTime() > wallTime + 0.3):
        wallTime = 0
    #failsave
    if(z == zOld and x == xOld): cntStop+=1
    else: cntStop = 0
    if(cntStop>100):
        goBackTime = robot.getTime()
    if(robot.getTime() < goBackTime + 0.6):
        speed1 = -6.28
        speed2 = -6.28
    if(robot.getTime() > goBackTime + 0.6):
        goBackTime = 0
    xOld = x
    zOld = z
    #black hole  
    if(recognizedColor == 'black'):
        print("BLACK)))")
        blackTime = robot.getTime()
    if(robot.getTime() < blackTime+0.6):
        speed1 = -3.14
        speed2 = -3.14
    if(robot.getTime() > blackTime+0.6):
        blackTime = 0
    #random
    if(int(robot.getTime()) % 50 ==0):kMod = random.choice([1,-1])
    if(int(robot.getTime())%10==0 and random.randint(0,9)==5):
        wall = True
        wallTime = robot.getTime()
    #recognizing signs
    templateRec()
    
    wheel1.setVelocity(0)#speed1)              
    wheel2.setVelocity(0)#speed2)
    
    #imshow
    cv2.imshow("frame", frame)
    cv2.imshow("frameR", frameR)
    cv2.imshow("frameL", frameL)
    cv2.imshow("MAP", mapping_img)
    
