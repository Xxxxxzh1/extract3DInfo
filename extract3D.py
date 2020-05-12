#!/usr/local/bin/python3
import re
import sys

mtlData = ''
objData = ''
mtlPwd = sys.argv[1]
objPwd = sys.argv[2]


with open(objPwd, 'r', encoding='ISO-8859-1') as f:
    objData = f.read()
    # print('obj content: ', objData)


with open(mtlPwd, 'r', encoding='ISO-8859-1') as f:
    mtlData = f.read()
    # print('mtl content: ', mtlData)


def getNumCoord(data):
    initCoord = re.findall('v (.*)\n', data)
    outNumCroodtList = []
    for num in range(len(initCoord)):
        outNumCroodtList.append(f'{num+1} 'f'{initCoord[num]}')
    # print('\ninit coord: \n', outNumCroodtList)
    # print('\n------All num length: ', len(outNumCroodtList))
    return outNumCroodtList


def getDefaultNum(data):
    defaultNum1 = re.findall('g Default([\s\S]*)usemtl mid', data)
    defaultNum2 = re.findall(' ([0-9]{1,})\/', defaultNum1[0])
    outDefaultNumList = list(set(defaultNum2))
    # print('\nDefault num: \n', outDefaultNumList)
    # print('\n------Default num length: ', len(outDefaultNumList))
    return outDefaultNumList


def getMidNum(data):
    midNum1 = re.findall('usemtl mid([\s\S]*)usemtl top', data)
    midNum2 = re.findall(' ([0-9]{1,})\/', midNum1[0])
    outMidNumList = list(set(midNum2))
    # print('\nMid num: \n', outMidNumList)
    # print('\n------Mid num length: ', len(outMidNumList))
    return outMidNumList


def getTopNum(data):
    topNum1 = re.findall('usemtl top([\s\S]*)', data)
    topNum2 = re.findall(' ([0-9]{1,})\/', topNum1[0])
    outTopNumList = list(set(topNum2))
    # print('\nTop num: \n', outTopNumList)
    # print('\n------Top num length: ', len(outTopNumList))
    return outTopNumList


def getRBG(data):
    defaultRBG = re.findall('newmtl Default\nKd(.*?)\n', data)
    midRBG = re.findall('newmtl mid\nKd(.*?)\n', data)
    topRBG = re.findall('newmtl top\nKd(.*?)\n', data)
    outRBGList = defaultRBG+midRBG+topRBG
    # print('\n------different mode RBG: \n', outRBGList)
    return outRBGList


def getOutList(initList, inDefaultList, inMidList, inTopList, inRBGList):
    outList = []
    for i in range(0, len(initList)):
        i += 1
        if str(i) in inTopList:
            outList.append(initList[i-1]+inRBGList[2])
        elif str(i) in inMidList:
            outList.append(initList[i-1]+inRBGList[1])
        else:
            outList.append(initList[i-1]+inRBGList[0])  
    # print('\n-----final list: \n', outList)
    return outList


def outputTxt(inlist):
    with open('./output.txt', 'w+') as f:
        f.write('-----NUM------Crood------RBG------\n\n')
        for element in inlist:
            f.write(f'{element}\n')
        f.close


# def usage():
#     print('--------------\n python extract3D.py [mtl_path] [obj_path]\n created by zhengzhi@zerozero.cn')


if __name__ == "__main__":
    numCroodList = getNumCoord(objData)
    defaultNumList = getDefaultNum(objData)
    midNumList = getMidNum(objData)
    topNumList = getTopNum(objData)
    RBGList = getRBG(mtlData)
    outputList = getOutList(numCroodList, defaultNumList, midNumList, topNumList, RBGList)
    outputTxt(outputList)
