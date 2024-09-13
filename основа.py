from controller import Robot,GPS,Camera
import cv2
import numpy as np
import struct
import random
import time

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
s4 = robot.getDevice("distance sensor4")
s5 = robot.getDevice("distance sensor5")
s6 = robot.getDevice("distance sensor6")
s7 = robot.getDevice("distance sensor6")
scolor = robot.getDevice("colour_sensor")
camera = robot.getDevice("camera_centre")
cameraR = robot.getDevice("camera_left")
cameraL = robot.getDevice("camera_right")
gps = robot.getDevice("gps sensor")
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
imu = robot.getDevice("inertial_unit")


#enabling sensors
s0.enable(timeStep)
s1.enable(timeStep)
s2.enable(timeStep)
s3.enable(timeStep)
s4.enable(timeStep)
s5.enable(timeStep)
s6.enable(timeStep)
s7.enable(timeStep)
scolor.enable(timeStep)
camera.enable(timeStep)
cameraR.enable(timeStep)
cameraL.enable(timeStep)
gps.enable(timeStep)
#emitter.enable(timeStep)
receiver.enable(timeStep)
imu.enable(timeStep)


#windows setup
cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
cv2.createTrackbar('x', 'settings', 4,20, nothing)
cv2.createTrackbar('y', 'settings', 800,1000, nothing)
cv2.createTrackbar('scale', 'settings', 6,10, nothing)
start = robot.getTime()


#templates setup
if (False):
    templateU = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\U.png', cv2.IMREAD_GRAYSCALE)
    templateH = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\H.png', cv2.IMREAD_GRAYSCALE)
    templateS = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\S.png', cv2.IMREAD_GRAYSCALE)
    templateCOR = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\COR.png', cv2.IMREAD_GRAYSCALE)
    templateOP = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\OP.png', cv2.IMREAD_GRAYSCALE)
    templateFG = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\FG.png', cv2.IMREAD_GRAYSCALE)
    templatePOI = cv2.imread('C:\\Users\\bolshakovae.25\\Downloads\\robocup\\POI.png', cv2.IMREAD_GRAYSCALE)
elif (False):
    templateU = cv2.imread('C:\\Users\\User\\Desktop\\robocup\\U.png', cv2.IMREAD_GRAYSCALE)
    templateH = cv2.imread('C:\\Users\\User\\Desktop\\robocup\\H.png', cv2.IMREAD_GRAYSCALE)
    templateS = cv2.imread('C:\\Users\\User\\Desktop\\robocup\\S.png', cv2.IMREAD_GRAYSCALE)
    templateCOR = cv2.imread('C:\\Users\\User\\Desktop\\robocup\\COR.png', cv2.IMREAD_GRAYSCALE)
    templateOP = cv2.imread('C:\\Users\\User\\Desktop\\robocup\\OP.png', cv2.IMREAD_GRAYSCALE)
    templateFG = cv2.imread('C:\\Users\\User\\Desktop\\robocup\\FG.png', cv2.IMREAD_GRAYSCALE)
    templatePOI = cv2.imread('C:\\Users\\User\\Desktop\\robocup\\POI.png', cv2.IMREAD_GRAYSCALE)
else:
    templateU = cv2.imread('C:\\Users\\user\\Desktop\\robocup rescue maze simulation\\U.png', cv2.IMREAD_GRAYSCALE)
    templateH = cv2.imread('C:\\Users\\user\\Desktop\\robocup rescue maze simulation\\H.png', cv2.IMREAD_GRAYSCALE)
    templateS = cv2.imread('C:\\Users\\user\\Desktop\\robocup rescue maze simulation\\S.png', cv2.IMREAD_GRAYSCALE)
    templateCOR = cv2.imread('C:\\Users\\user\\Desktop\\robocup rescue maze simulation\\COR.png', cv2.IMREAD_GRAYSCALE)
    templateOP = cv2.imread('C:\\Users\\user\\Desktop\\robocup rescue maze simulation\\OP.png', cv2.IMREAD_GRAYSCALE)
    templateFG = cv2.imread('C:\\Users\\user\\Desktop\\robocup rescue maze simulation\\FG.png', cv2.IMREAD_GRAYSCALE)
    templatePOI = cv2.imread('C:\\Users\\user\\Desktop\\robocup rescue maze simulation\\POI.png', cv2.IMREAD_GRAYSCALE)
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
ublack = [110, 110, 110]
black = [41,41,41]
blue = [63,63,252]
purple = [145,63,226]
brown = [209,175,101]
silverMin = [246,246,246]
silverMax = [252,252,252]
green = [33,249,33]
red = [252,63,63]
recognizedColor = ''
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
lst = []
lstt = []
q = 0


speed1 = max_velocity
speed2 = max_velocity


#color def
def colorRec():
    if(sensColor[0] == black[0] and sensColor[1] == black[1] and sensColor[2] == black[2]):
        recognizedColor = 'black'
        mapList[zCell][xCell] = '2'
    elif(sensColor[0] == ublack[0] and sensColor[1] == ublack[1] and sensColor[2] == ublack[2]):
        recognizedColor = 'ublack'
    elif(sensColor[0] == green[0] and sensColor[1] == green[1] and sensColor[2] == green[2]):
        #print("green")
        recognizedColor = 'green'
        mapList[zCell][xCell] = '9'
    elif(sensColor[0] == red[0] and sensColor[1] == red[1] and sensColor[2] == red[2]):
        #print("red")
        recognizedColor = 'red'
        mapList[zCell][xCell] = '8'
    elif(sensColor[0] >= silverMin[0] and sensColor[1] >= silverMin[1] and sensColor[2] >= silverMin[2] and sensColor[0] <= silverMax[0] and sensColor[1] <= silverMax[1] and sensColor[2] <= silverMax[2]):
        #print("silver")

        recognizedColor = 'silver'
        try:
            mapList[zCell][xCell] = '4'
        except:
            print('Саша мудак')
    elif(sensColor[0] == brown[0] and sensColor[1] == brown[1] and sensColor[2] == brown[2]):
        #print("brown")
        recognizedColor = 'brown'
        mapList[zCell][xCell] = '3'
    elif(sensColor[0] == blue[0] and sensColor[1] == blue[1] and sensColor[2] == blue[2]):
        #print("blue")
        recognizedColor = 'blue'
        mapList[zCell][xCell] = '6'
    elif(sensColor[0] == purple[0] and sensColor[1] == purple[1] and sensColor[2] == purple[2]):
        #print("purple")
        recognizedColor = 'purple'
        mapList[zCell][xCell] = '7'
    else:
        ##print("None")
        recognizedColor = 'none'
    return recognizedColor


lstfind = []
lstU = []
lstH = []
lstS = []
lstC = []
lstO = []
lstF = []
lstP = []
recognizedCamera = 4
def templateRec(x, y, z):
    global recognizedCamera
    recognizedCamera = 4
    leastScale = 30
    for t in range(6):
        if(t==0):
            templateT = templateU
            text1 = 'Найдена Невредимая жертва. Координаты: ' + "x: " + str(x) + " y: " + str(y) + " z: " + str(z)
            color = (255,0,0)
            text = 'U'
        if(t==1):
            templateT = templateH
            text1 = 'Найдена Поврежденная жертва. Координаты: ' + "x: " + str(x) + " y: " + str(y) + " z: " + str(z)
            color = (0,255,0)
            text = 'H'
        if(t==2):
            templateT = templateS
            text1 = 'Найдена Стабильная жертва. Координаты: ' + "x: " + str(x) + " y: " + str(y) + " z: " + str(z)
            color = (0,0,255)
            text = 'S'
        if(t==3):
            templateT = templateCOR
            text1 = '!ОПАСНО! КОРРОЗИОННЫЙ. Координаты: ' + "x: " + str(x) + " y: " + str(y) + " z: " + str(z)
            color = (0,255,255)
            text = 'C'
        if(t==4):
            templateT = templateOP
            text1 = '!ОПАСНО! ОРГАНИЧЕСКИЙ ПЕРОКСИД. Координаты: ' + "x: " + str(x) + " y: " + str(y) + " z: " + str(z)
            color = (255,0,255)
            text = 'O'
        if(t==5):
            templateT = templateFG
            text1 = '!ОПАСНО! ГОРЮЧИЙ ГАЗ. Координаты: ' + "x: " + str(x) + " y: " + str(y) + " z: " + str(z)
            color = (255,255,0)
            text = 'F'
        if(t==6):
            templateT = templatePOI
            text1 = '!ОПАСНО! ЯД. Координаты: ' + "x: " + str(x) + " y: " + str(y) + " z: " + str(z)
            color = (255,0,0)
            text = 'P'

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
                    #print(text1)
                    recognizedSighn = text
                    mapList[zCell][xCell] = text
                    recognizedCamera = j
                    if(leastScale>i):leastScale = i
                    rt = 0
                    lstfind.append(x)
                    lstfind.append(z)
                    if text == 'H':
                        for v in range(len(lstH)):
                            if x in lstH[v][0] and z in lstH[v][1]:
                                rt = 1
                                break
                        if rt == 0:        
                            lstH.append([list(range(x-3, x+4)), list(range(z-3, z+4))])
                            print(text1)
                            time.sleep(1)
                            
                    elif text == 'S':
                        for v in range(len(lstS)):
                            if x in lstS[v][0] and z in lstS[v][1]:
                                rt = 1
                                break
                        if rt == 0:        
                            lstS.append([list(range(x-3, x+4)), list(range(z-3, z+4))])
                            print(text1)
                            time.sleep(1)
                            
                    elif text == 'U':
                        for v in range(len(lstU)):
                            if x in lstU[v][0] and z in lstU[v][1]:
                                rt = 1
                                break
                        if rt == 0:        
                            lstU.append([list(range(x-3, x+4)), list(range(z-3, z+4))])
                            print(text1)
                            time.sleep(1)
                            
                    elif text == 'F':
                        for v in range(len(lstF)):
                            if x in lstF[v][0] and z in lstF[v][1]:
                                rt = 1
                                break
                        if rt == 0:        
                            lstF.append([list(range(x-3, x+4)), list(range(z-3, z+4))])
                            print(text1)
                            time.sleep(1)
                            
                    elif text == 'P':
                        for v in range(len(lstP)):
                            if x in lstP[v][0] and z in lstP[v][1]:
                                rt = 1
                                break
                        if rt == 0:        
                            lstP.append([list(range(x-3, x+4)), list(range(z-3, z+4))])
                            print(text1)
                            time.sleep(1)

                            
                    elif text == 'C':
                        for v in range(len(lstC)):
                            if x in lstC[v][0] and z in lstC[v][1]:
                                rt = 1
                                break
                        if rt == 0:        
                            lstC.append([list(range(x-3, x+4)), list(range(z-3, z+4))])
                            print(text1)
                            time.sleep(1)
                            
                    elif text == 'O':
                        for v in range(len(lstO)):
                            if x in lstO[v][0] and z in lstO[v][1]:
                                rt = 1
                                break
                        if rt == 0:        
                            lstO.append([list(range(x-3, x+4)), list(range(z-3, z+4))])
                            print(text1)
                            time.sleep(1)

    #print(leastScale)
    #print(recognizedSighn)  
    p#rint(recognizedCamera)

while robot.step(timeStep) != -1:

    if(robot.getTime()%1 == 0):print(".")
    
    speed1 = 4
    speed2 = 4


#получение координат рoбота
    x = int(gps.getValues()[0]*100)
    y = int(gps.getValues()[1]*100)
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
        #print("expanded right")
    if(xCell<-startPosX):
       expandLeft()
       startPosX+=1
       #print("expanded left")
    if(zCell>len(mapList)+startPosZ-1):
        expandDown()
        #print("expanded down")
    if(zCell<-startPosZ):
       expandUp()
       startPosZ+=1
       #print("expanded up")



#определение цвета с датчика
    imageRGBSensor = scolor.getImage()
    sensColor = [scolor.imageGetRed(imageRGBSensor, 1, 0, 0),scolor.imageGetGreen(imageRGBSensor, 1, 0, 0),scolor.imageGetBlue(imageRGBSensor, 1, 0, 0)]
    recognizedColor = colorRec()
    #print(sensColor)
    #print(recognizedColor)
        #print('s0:', s0.getValue()//0.001/1000, 's1:', s1.getValue()//0.001/1000, 's2:', s2.getValue()//0.001/1000, 's3:', s3.getValue()//0.001/1000, 's4:', s4.getValue()//0.001/1000, 's5:', s5.getValue()//0.001/1000, 's6:', s6.getValue()//0.001/1000, 's7:', s7.getValue()//0.001/1000)

    #settings read
    k1 = cv2.getTrackbarPos('x','settings')
    k2=10*k1
    threshold = cv2.getTrackbarPos('y','settings')/1000+0.001
    targetLength= cv2.getTrackbarPos('scale','settings')/100

    
    #reading camera frames
    frame = cv2.cvtColor(np.frombuffer(camera.getImage(), np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    frameR = cv2.cvtColor(np.frombuffer(cameraR.getImage(), np.uint8).reshape((cameraR.getHeight(), cameraR.getWidth(), 4)), cv2.COLOR_BGRA2BGR)
    frameL = cv2.cvtColor(np.frombuffer(cameraL.getImage(), np.uint8).reshape((cameraL.getHeight(), cameraL.getWidth(), 4)), cv2.COLOR_BGRA2BGR)

    #print(frame.shape)
    if (False):
        cv2.imwrite(r"C://Users//TBG//Downloads",frame)
    #else:
        #cv2.imwrite(r"C:\\Users\\user\\Downloads",frame)

#распознавание изображений на стенах
    templateRec(x, y, z)

    
#процесс движения
    if s0.getValue() < 0.1 or s1.getValue() < 0.1 or s7.getValue() < 0.04:
        speed1 = 6
        speed2 = -6
    if s1.getValue() > 0.14 and s2.getValue() > 0.14 and s3.getValue() > 0.08:
        speed1 = -6
        speed2 = 6

    if recognizedColor == 'black' or recognizedColor == 'green':
        ss2 = (s2.getValue() * 100000 // 1000)
        while robot.step(timeStep) != -1:
            #print(s3.getValue() * 100000 // 1000)
            if (s3.getValue() * 100000 // 1000) == ss2:
                q = 2
                break
            wheel1.setVelocity(1)              
            wheel2.setVelocity(-1)

    if recognizedColor == 'ublack':
        speed1 = -1
        speed2 = -1
    
            
#действие робота при застревании
    lst1 = []
    lst.append([str(x), str(y), str(z)])
    if len(lst) > 50:
        del lst[0]
    for i in range(len(lst)):
        if lst[i] not in lst1:
            lst1.append(lst[i])
    if len(lst1) == 1 and len(lst) == 50:
        speed1 = random.randint(-6, 6)
        speed2 = random.randint(-6, 6)
    lstt1 = []
    lstt.append([str(x), str(y), str(z)])
    if len(lstt) > 100:
        del lstt[0]
    for i in range(len(lst)):
        if lstt[i] not in lstt1:
            lstt1.append(lstt[i])
    #if len(lstt1) == 1 and len(lstt) == 100:
    #    speed2 = 0
    #    speed1 = -6
    











    if q > 0:
        speed1 = 6
        speed2 = 6
        q -= 1
    wheel1.setVelocity(speed1)              
    wheel2.setVelocity(speed2)


    #imshow
    cv2.imshow("frame", frame)
    cv2.imshow("frameR", frameR)
    cv2.imshow("frameL", frameL)
    cv2.imshow("MAP", mapping_img)
    

    


