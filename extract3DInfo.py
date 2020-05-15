#!/usr/local/bin/python3
import re
import sys

mtlData = ''
objData = ''
mtlPwd = sys.argv[1]
objPwd = sys.argv[2]

# mtlPwd = '/Users/zhengzhi/Desktop/B2.mtl'
# objPwd = '/Users/zhengzhi/Desktop/B2.obj'


with open(objPwd, 'r', encoding='ISO-8859-1') as f:
    objData = f.read()
    # print('obj content: ', objData)


with open(mtlPwd, 'r', encoding='ISO-8859-1') as f:
    mtlData = f.read()
    # print('mtl content: ', mtlData)


# 从mtl文件中提取所有点的坐标信息
def getNumCoord(data):
    initCoord = re.findall('v (.*)\n', data)
    outNumCroodtList = []
    for num in range(len(initCoord)):
        outNumCroodtList.append(f'{num+1} 'f'    {initCoord[num]}')
    # print('\ninit coord: \n', outNumCroodtList)
    # print('\n------All num length: ', len(outNumCroodtList))
    return outNumCroodtList


# 从obj文件中按序提取每个RBG模式
def getSeqRBGMode(data):
    seqRBGMode = re.findall('usemtl (.*)', data)
    print('\n------RBGModeList is: \n', seqRBGMode)
    return seqRBGMode


# 从mtl文件中提取每个RBG模式对应的Kd
def getRBG(data, inRBGModeList):
    RBGKdList = []
    outRBGKdList = []
    for eachRBG in inRBGModeList:
        eachRBGKd = re.findall(f'newmtl {eachRBG}\nKd(.*?)\n', data)
        # 前后加空格方便正则匹配
        RBGKdList.append(f'     {eachRBGKd[0]} ')
    print('\n------different mode RBG: \n', RBGKdList)
    for i in range(0, len(RBGKdList)):
        everyRBGModeKd = re.findall(r'(-?\d+\.?\d*e?-?\d*?)', RBGKdList[i])
        # print('\n------everyRBGModeKd: \n ', everyRBGModeKd)
        for j in range(0, 3):
            everyRBGModeKd[j] = str(round(float(everyRBGModeKd[j])*255))
        # print('\n---*255----: \n', everyRBGModeKd)
        outRBGKdList.append(f'      {everyRBGModeKd[0]} {everyRBGModeKd[1]} {everyRBGModeKd[2]} ')
    print(outRBGKdList)
    return outRBGKdList


# 从mtl文件中提取Default模式的点序号
def getDefaultModeNum(data, inRBGModeList):
    defaultModeNum1 = re.findall(f'g Default([\s\S]*)usemtl {inRBGModeList[1]}', data)
    defaultModeNum2 = re.findall(' ([0-9]{1,})\/', defaultModeNum1[0])
    # 将得到的Num去重
    outDefaultNumList = (list(set(defaultModeNum2)))
    print('\nDefaultMode num: \n', outDefaultNumList)
    print('\n------DefaultMode num length: ', len(outDefaultNumList))
    return outDefaultNumList


# 从mtl文件中提取最后一个模式的点序号
def getLastSeqModeNum(data, inRBGModeList):
    i = len(inRBGModeList)
    lastModeNum1 = re.findall(f'usemtl {inRBGModeList[i-1]}([\s\S]*)', data)
    lastModeNum2 = re.findall(' ([0-9]{1,})\/', lastModeNum1[0])
    # 将得到的Num去重
    outDefaultNumList = (list(set(lastModeNum2)))
    print('\nLastSeqMode num: \n', lastModeNum2)
    print('\n------LastSeqMode num length: ', len(lastModeNum2))
    return outDefaultNumList


# 从mtl文件中提取中间模式的点序号
def getOtherNum(data, inRBGModeList):
    RBGModeNum = len(inRBGModeList)
    outOtherNumList = []
    # print('\n------RBG mode num: \n', RBGModeNum)
    for i in range(1, RBGModeNum-1):
        modeNum1 = re.findall(f'usemtl {inRBGModeList[i]}([\s\S]*)usemtl {inRBGModeList[i+1]}', data)
        modeNum2 = re.findall(' ([0-9]{1,})\/', modeNum1[0])
        # 将得到的Num去重
        outOtherNumList.append(list(set(modeNum2)))
    print('\n-----outInitOtherNumList\n', outOtherNumList)
    # print('\n------outOtherNumList length: ', len(outOtherNumList[0])+len(outOtherNumList[1]))
    return outOtherNumList


# 将other里面的数值从前往后删除
def deleteRepeatNum(inOtherModeNumList):
    otherNumListLength = len(inOtherModeNumList)
    print('\n-----other num list length: ', otherNumListLength)
    for i in range(0, otherNumListLength-1):
        latestNumList = []
        for j in range(i+1, otherNumListLength):
            latestNumList += inOtherModeNumList[j]
            print(latestNumList)
        inOtherModeNumList[i] = list(set(inOtherModeNumList[i]) - set(latestNumList))
    print('\n------unrepeat othertList: \n', inOtherModeNumList)
    return inOtherModeNumList


def getOutList(inNumCoordList, inRBGModeKdList, inLastSeqModeNumList, inOtherModeNumList, inDefaultModeNumList):
    outList = []
    # 获得点的总个数
    pointNum = len(inNumCoordList)
    print('\n------total point num: \n', pointNum)
    # 获得RBG模式的个数
    RBGModeNum = len(inRBGModeKdList)

    for i in range(0, pointNum):
        # 把所有点的坐标初始化，把每个点的RBG按default初始化
        outList.append(inNumCoordList[i]+inRBGModeKdList[0])
        # 替换obj文件中靠后点的RBG，如果有则直接进入下次循环
        if str(i+1) in inLastSeqModeNumList:
            outList[i] = re.sub('      (.*) ', inRBGModeKdList[RBGModeNum-1], outList[i])
            continue
        # 替换中间点的RBG
        for j in range(0, RBGModeNum-2):
            if str(i+1) in inOtherModeNumList[j]:
                outList[i] = re.sub('      (.*) ', inRBGModeKdList[j+1], outList[i])                
    return outList


def outputTxt(inList):
    with open('./output.txt', 'w+') as f:
        f.write('NUM------------Crood------------RBG\n\n')
        for element in inList:
            f.write(f'{element}\n')
        f.close


# def usage():
#     print('--------------\n python extract3D.py [mtl_path] [obj_path]\n created by zhengzhi@zerozero.cn')


if __name__ == "__main__":
    RBGMode = getSeqRBGMode(objData)
    RBGModeKdList = getRBG(mtlData, RBGMode)
    numCroodList = getNumCoord(objData)
    defaultNumList = getDefaultModeNum(objData, RBGMode)
    lastSeqNumList = getLastSeqModeNum(objData, RBGMode)
    otherNumList = getOtherNum(objData, RBGMode)
    otherNoRepeatList = deleteRepeatNum(otherNumList)
    outputList = getOutList(numCroodList, RBGModeKdList, lastSeqNumList, otherNoRepeatList, defaultNumList)
    outputTxt(outputList)
