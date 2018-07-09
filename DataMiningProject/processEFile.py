#!/usr/bin/python

#Loads the database with the records from the jobs.swf file into jobs
#after making sure that there are no -1 records found. (preprocess)

import sys
import re
from datetime import datetime, timedelta

recDict = dict()
commentDict = dict()
delayDict = dict()
dbarrayDict = dict()
minPts = 200

def main(argv):
    inputFile = argv[0]
    count = 1

    with open(inputFile) as fp:
        for newLine in fp:
            if len(newLine) > 323:
                comments = newLine[323:].strip()
                index = 322
                if not newLine[index].isspace():
                    while not newLine[index].isspace() and not newLine[index+1].isspace():
                        index -= 1
                    comments = newLine[index:].strip()

            data = newLine.strip().split()
            if len(data) > 0 and data[0].startswith('2'):
                cleanedComments = cleanFields(comments)
                newData = [data[items] for items in range(len(data)) if items < 12 and len(data[items]) > 1][3:7]
                gid = getGID(cleanedComments, newData[1], newData[2])
                newData.append(gid)
                recDict[count] = newData
                count += 1
                if count > 10000:
                    break

#---------------------------------------------------------------------
def cleanFields(comments):
    comments = comments.replace(',', '')
    fields = ['d+' if items.isdigit() else items for items in comments.split()]
    newFields = ['V*' if '=' in items else items for items in fields ]
    newFields2 = ' '.join(['V*' if items != 'd+' and not items.isalpha() else items for items in newFields ])
    return newFields2

#---------------------------------------------------------------------
def getGID(cleanedComments, subcomp, severity):
    if cleanedComments in commentDict.keys():
        return commentDict[cleanedComments]
    else:
        gidVal = len(commentDict) + 1
        commentDict[cleanedComments] = gidVal
        print cleanedComments, gidVal
        return gidVal

#---------------------------------------------------------------------
def generateDelays():
    for i in reversed(range(len(recDict))):
        recA = recDict[i+1]
        if recA[2] == 'FATAL' or recA[2] == 'ERROR':
            curr_time = datetime.strptime(recA[3],'%Y-%m-%d-%H.%M.%S.%f')
            j = i
            while True:
                if j == 0:
                    break
                else:
                    recB = recDict[j]
                    prev_time = datetime.strptime(recB[3],'%Y-%m-%d-%H.%M.%S.%f')
                    if (curr_time - prev_time) < timedelta(days=2):
                        if (recA[4],recB[4]) in delayDict:
                            l = delayDict[(recA[4], recB[4])]
                            l.append(curr_time -prev_time)
                            delayDict[(recA[4], recB[4])] = l
                        else:
                            delayDict[(recA[4], recB[4])] = []
                            delayDict[(recA[4], recB[4])].append(curr_time - prev_time)
                        j -= 1
                    else:
                        break
    #
    for keys in delayDict:
        dbarrayDict[keys] = len(delayDict[keys])

# It is a random algorithm, so there is no real trouble if we use one way or the other.
#---------------------------------------------------------------------
def runDBScan():
    CG = []
    for keys in dbarrayDict:
        if dbarrayDict[keys] > minPts:
            CG.append((keys,delayDict[keys][0]))
    for items in range(len(CG)):
        print CG[items]

#---------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1:])
        generateDelays()
        runDBScan()
    else:
        print '"insufficient number of arguments", len(sys.argv)'
#---------------------------------------------------------------------
