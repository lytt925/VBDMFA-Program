import pandas as pd
import numpy as np
from itertools import combinations, product, chain, repeat
import copy

def genCombinations(countList):
    temp = []
    i = 4
    for count in countList:
        i += 1
        temp.append(np.repeat(i,count))

    ratings = []
    for i in range(len(temp)):
        stimRating = temp[i]
        ratings.append([str(j)+'_'+str(i+1) for i,j in enumerate(stimRating)])

    diffList = [[] for i in range(4)]
    for c in list(combinations(ratings,2)):
        diff = abs(int(c[1][0].split('_')[0])-int(c[0][0].split('_')[0]))
        diffList[diff-1].append(c)
        
    RatingCombinations = []
    diffCombinations =[[] for i in range(4)]
    i=0
    for diff in diffList:
        for rate in diff:
            this = list(product(rate[0], rate[1]))
            RatingCombinations += this
            diffCombinations[i]+= this
        i+=1
    # allcom = np.array(RatingCombinations).flatten()
    
    return diffCombinations, RatingCombinations, ratings


def getStim(diff, diffCombinations, diffComcopy, stimList, quotaDF):
    def checkQuota(stim):
        if (quotaDF[quotaDF['Name']==stim[0]]['NowCounts'].values[0]==0) or \
            (quotaDF[quotaDF['Name']==stim[1]]['NowCounts'].values[0]==0):
            return False
        return True
    global failed
    ind = diff-1
    # needCounts = [150, 120, 90, 60]
    needCounts = [160, 120, 80, 40]
    for i in range(len(diffCombinations[ind])):
        if len(stimList[ind]) == needCounts[ind]:
            break
        index = np.random.randint(len(diffCombinations[ind]))
        toAdd = diffCombinations[ind][index]
        diffCombinations[ind].pop(index)
        if checkQuota(toAdd):
            stimList[ind].append(toAdd)
            diffComcopy[ind].remove(toAdd)
            for img in toAdd:
                updateIndex = quotaDF[quotaDF['Name']==img].index[0]
                quotaDF.at[updateIndex, 'NowCounts'] -= 1
        else:
            failed+=1

failed = 0
def createFirstStim(NowCounts, allcounts):
    print(NowCounts)
    diffCombinations, RatingCombinations, ratings = genCombinations(allcounts) # [6,8,10,10,8,12]
    diffComcopy = copy.deepcopy(diffCombinations)
    stimList = [[] for i in range(4)]
    allratings = [item for rating in ratings for item in rating]
    quotaDF = pd.DataFrame({'Name':allratings, 'NowCounts': NowCounts})
    global failed
    failed = 0
    for i in [4,3,2,1]:
        getStim(i, diffCombinations, diffComcopy, stimList, quotaDF)
    stimOccur = []
    for ind in range(4):
        stimOccur += list(sum(stimList[ind], ()))
    print(len([item for rating in stimList for item in rating]))
    return stimList, stimOccur, diffComcopy

def createSecondStim(NowCounts, prevDiffCom, allcounts):
    print(NowCounts)
    diffComcopy = copy.deepcopy(prevDiffCom)
    stimList = [[] for i in range(4)]
    __, _, ratings = genCombinations(allcounts) # [6,8,10,10,8,12]
    allratings = [item for rating in ratings for item in rating]
    quotaDF = pd.DataFrame({'Name':allratings, 'NowCounts': NowCounts})
    global failed
    failed = 0
    for i in [4,3,2,1]:
        getStim(i, prevDiffCom, diffComcopy, stimList, quotaDF)
    stimOccur = []
    for ind in range(4):
        stimOccur += list(sum(stimList[ind], ()))
    print(len([item for rating in stimList for item in rating]))
    return stimList, stimOccur, diffComcopy

def makeStim(allcounts):
    NowCounts=5
    while True:
        stimList1, stimOccur1, newDiffComcopy = createFirstStim(NowCounts, allcounts)
        total = len([item for rating in stimList1 for item in rating])
        if total == 400:
            break
        else:
            NowCounts+=1
    NowCounts=5
    while True:
        diffComcopy = copy.deepcopy(newDiffComcopy)
        stimList2, stimOccur2, lastDiffComcopy = createSecondStim(NowCounts, diffComcopy, allcounts)
        total = len([item for rating in stimList2 for item in rating])
        if total == 400:
            break
        else:
            NowCounts+=1
    
    return stimList1, stimList2
    