mapWidth = 5
mapHeight = 5
mapList = ['0']*mapHeight
for i in range(mapHeight):
    mapList[i] = ['0']*mapWidth
mapList[int(mapHeight/2)][int(mapWidth/2)] = 'S'
print(mapList)
def expandRight():
    for i in range(len(mapList)):
        mapList[i].append('0')
def expandLeft():
    for i in range(len(mapList)):
        mapList[i].insert(0,'0')
def expandDown():
    addList = ['0']*len(mapList[1])
    mapList.append(addList)
def expandUp():
    addList = ['0']*len(mapList[1])
    mapList.insert(0,addList)
    
expandLeft()
print('###########')
print(mapList)
