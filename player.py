import itertools
import json

class Player(object):
    maxNumber = 30
    allCombination = list(itertools.combinations([0, 1, 2, 3, 4], 2))
    continueLose = 0
    oneBetMoney = 22736
    oneWinMoney = 45000
    totalEarn = 0
    totalBet = 0
    accBetMoney = 0
    maxAccBetMoney = 0
    lock = False

    def __init__(self):
        self.allCombinationStatus = {}
        for item in self.allCombination:
            self.allCombinationStatus.update({
                item: dict.fromkeys(range(0, self.maxNumber), 0)
            })
            self.allCombinationStatus[item]['continueLose'] = 0

    def addInfomation(self, winCombination):
        for key in self.allCombinationStatus:
            if key in winCombination:
                continueLose = self.allCombinationStatus[key]['continueLose']
                if self.allCombinationStatus[key] is None:
                    self.allCombinationStatus[key][continueLose] = 1
                else:
                    self.allCombinationStatus[key][continueLose] += 1

                self.allCombinationStatus[key]['continueLose'] = 0
            else:
                self.allCombinationStatus[key]['continueLose'] += 1

        if self.betNumber is not None:
            if self.betNumber in winCombination:
                self.totalBet += self.oneBetMoney
                self.totalEarn += self.oneWinMoney
                if self.accBetMoney > self.maxAccBetMoney:
                    self.maxAccBetMoney = self.accBetMoney
                self.accBetMoney = 0
                self.continueLose = 0
                print 'Win: %s' % (self.totalEarn - self.totalBet)
            else:
                self.totalBet += self.oneBetMoney
                self.accBetMoney += self.oneBetMoney
                self.continueLose += 1
                print 'Loss: %s' % (self.totalEarn - self.totalBet)
        else:
            if self.betNumber in winCombination:
                self.continueLose = 0
            print 'Locking: %s' % (self.totalEarn - self.totalBet)

        print 'AccBetMoney: %s' % self.accBetMoney
        print 'MaxAccBetMoney: %s' % self.maxAccBetMoney

    def decideNumber(self):
        # decidedNumber = ()
        # maxWinRate = 0
        # for key in self.allCombinationStatus:
        #     continueLose = self.allCombinationStatus[key]['continueLose']
        #     molecule = self.allCombinationStatus[key][continueLose+1]
        #     denominator = 0
        #     for index in range(continueLose+1, self.maxNumber):
        #         denominator += self.allCombinationStatus[key][index]
        #     if denominator == 0:
        #         pass
        #     else:
        #         winRate = float(molecule)/float(denominator)
        #         print '%s: winRate %s' % (''.join(str(key)), winRate)
        #         if winRate > maxWinRate:
        #             maxWinRate = winRate
        #             decidedNumber = key
        self.betNumber = (1, 3)