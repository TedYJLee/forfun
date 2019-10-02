# coding=UTF-8

from inforUtil import informationUtil
import itertools
import json
from player import Player
from operator import itemgetter

if __name__ == '__main__':
    winner = Player()
    simulateTimes = 1
    lottoInfo = informationUtil(informationUtil.Lotto)
    sixInfo = informationUtil(informationUtil.SixColor)
    record = {}
    continueLose = 0
    # mergeList = lottoInfo.eachIssueInformation + sixInfo.eachIssueInformation
    mergeList = sixInfo.eachIssueInformation
    sortedList = sorted(mergeList, key=itemgetter('Date'))
    setList = []
    for item in sortedList:
        popItem = sortedList.pop()
        if popItem not in setList:
            setList.insert(0, popItem)

    maxLost = 0
    allCutStatus = {}
    for item in setList:
        temp = {}
        validHead = []
        winCombination = []
        print '連續沒開: %s' % continueLose
        winner.decideNumber()
        betCombination = winner.betNumber
        # betCombination = (3, 4)

        print item
        for i in range(1, 7):
            head = int(item[i]) / 10
            if not temp.has_key(head):
                temp.update({
                    head: 1
                })
            else:
                temp[head] += 1

        for key in temp.keys():
            if temp[key] == 1 or temp[key] == 2:
                validHead.append(key)

        allWinCombination = list(itertools.combinations(validHead, 2))
        if betCombination is not None:
            if betCombination in allWinCombination:
                if allCutStatus.has_key(continueLose):
                    allCutStatus[continueLose] += 1
                else:
                    allCutStatus.update({
                        continueLose: 1
                    })
                continueLose = 0
            else:
                continueLose += 1

            if continueLose > maxLost:
                maxLost = continueLose

        winner.addInfomation(allWinCombination)
        print '這次六碰組合: %s' % ''.join(str(allWinCombination))
        print '下注: %s' % ''.join(str(betCombination))
        print '==============='

    print '最多連續沒開: %s' % maxLost
    print '連續沒開次數統計: %s' % json.dumps(allCutStatus, sort_keys=True, indent=4)