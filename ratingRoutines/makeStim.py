import pandas as pd
import numpy as np
from itertools import combinations, product, chain, repeat
import copy


def genCombinations(countList, chooseStim='2345678', difficultyRange=3):
    smallestStim = int(chooseStim[0])
    temp = []  # 得到所有分數*數量的list
    for i, count in enumerate(countList):
        i = i + smallestStim
        temp.append(np.repeat(i, count))

    ratings = []  # 將所有刺激給編號 (分數_編號)
    for i in range(len(temp)):
        stimRating = temp[i]
        ratings.append([str(j)+'_'+str(i+1) for i, j in enumerate(stimRating)])

    diffDict = {i+1: [] for i in range(difficultyRange)}  # 組合難度分類
    for c in list(combinations(ratings, 2)):
        diff = abs(int(c[1][0].split('_')[0])-int(c[0][0].split('_')[0]))
        if diff in diffDict.keys():
            diffDict[diff].append(c)

    AllCombinations = []  # 創建所有組合
    diffCombinationsDict = {i+1: []
                            for i in range(difficultyRange)}  # 創建所有組合並以難度分類
    for diff, comb in diffDict.items():
        for stims in comb:
            Trial = list(product(stims[0], stims[1]))
            AllCombinations += Trial
            diffCombinationsDict[diff] += Trial

    return diffCombinationsDict, AllCombinations, ratings


def getStim(diffCombinationsDict, quotaDF, needCounts=None):

    removeUsedStim = copy.deepcopy(diffCombinationsDict)
    if needCounts == None:
        needCounts = {1: 200, 2: 200, 3: 200, 4: 200}  # [150, 120, 90, 60]

    def checkQuota(stim):
        if (quotaDF[quotaDF['Name'] == stim[0]]['NowCounts'].values[0] == 0) or \
                (quotaDF[quotaDF['Name'] == stim[1]]['NowCounts'].values[0] == 0):
            return False
        return True
    global failed

    stimDict = {i+1: [] for i in range(3)}
    for diff, comb in list(diffCombinationsDict.items())[::-1]:
        for i in range(len(comb)):
            if len(stimDict[diff]) == needCounts[diff]:
                break
            index = np.random.randint(len(comb))
            toAdd = comb[index]
            diffCombinationsDict[diff].pop(index)  # 有抽出來過就丟掉
            if checkQuota(toAdd):
                stimDict[diff].append(toAdd)
                removeUsedStim[diff].remove(toAdd)
                for img in toAdd:
                    updateIndex = quotaDF[quotaDF['Name'] == img].index[0]
                    quotaDF.at[updateIndex, 'NowCounts'] -= 1
            else:
                failed += 1

    return stimDict, removeUsedStim, diffCombinationsDict


failed = 0


def createFirstStim(NowCounts, allcounts):
    print('all',allcounts)
    diffCombinationsDict, AllCombinations, ratings = genCombinations(
        allcounts)  # [6,8,10,10,8,12]
    allratings = [item for rating in ratings for item in rating]
    quotaDF = pd.DataFrame({'Name': allratings, 'NowCounts': NowCounts})
    global failed
    failed = 0
    stimDict, removeUsedStim, _ = getStim(diffCombinationsDict, quotaDF)
    print(len([item for rating in stimDict.values() for item in rating]))
    return stimDict, removeUsedStim, allratings


def createSecondStim(NowCounts, prevDiffComDict, allcounts, allratings):
    print(NowCounts)
    quotaDF = pd.DataFrame({'Name': allratings, 'NowCounts': NowCounts})
    global failed
    failed = 0
    stimDict, removeUsedStim, _ = getStim(prevDiffComDict, quotaDF)
    print(len([item for rating in stimDict.values() for item in rating]))
    return stimDict, removeUsedStim


def makeStim(allcounts):
    NowCounts = 4
    while True:
        stimDict1, newDiffCombination, allratings = createFirstStim(
            NowCounts, allcounts)
        total = len([item for rating in stimDict1.values() for item in rating])
        if total == 600:
            break
        else:
            NowCounts += 1
    NowCounts1 = NowCounts
    NowCounts = 4
    while True:
        diffComcopy = copy.deepcopy(newDiffCombination)
        stimDict2, removeUsedStim = createSecondStim(NowCounts, diffComcopy, allcounts, allratings)
        total = len([item for rating in stimDict2.values() for item in rating])
        if total == 600:
            break
        else:
            NowCounts+=1
    NowCounts2 = NowCounts

    return stimDict1, stimDict2, NowCounts1, NowCounts2
