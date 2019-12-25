import os
import json

class fiveThreeNineFeatureUtil(object):
    logPath = os.path.join('Log', 'addInformation')

    lockCountsDict = {
        "0": {},
        "1": {},
        "2": {},
        "3": {},
        "4": {},
        "5": {},
        "6": {},
        "7": {},
        "8": {},
        "9": {}
    }

    currentLockDict = {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0
    }

    def __init__(self):
        if os.path.exists(self.logPath):
            os.remove(self.logPath)

    def addInformation(self, tailNumbers, issue):
        for key in self.currentLockDict:
            if key in tailNumbers:
                if self.currentLockDict[key] not in self.lockCountsDict[key]:
                    self.lockCountsDict[key].update({
                        self.currentLockDict[key]: 1
                    })
                else:
                    self.lockCountsDict[key][self.currentLockDict[key]] += 1
                self.currentLockDict[key] = 0
            else:
                self.currentLockDict[key] += 1

        with open(self.logPath, 'a+') as logFile:
            logFile.write('Issue: %s\n' % issue)
            logFile.write('lockCountsDict:\n%s\n' % json.dumps(self.lockCountsDict, indent=4))
            logFile.write('currentLockDict:\n%s\n' % json.dumps(self.currentLockDict, indent=4))
            logFile.write('======================\n')
