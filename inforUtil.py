from BeautifulSoup import BeautifulSoup
import os
import requests
import json

collectFiveThreeNineItems = lambda item: [item.text.encode('ascii', 'ignore')[3:12], [item.text.encode('ascii', 'ignore')[24:34][i:i + 2] for i in range(0, len(item.text.encode('ascii', 'ignore')[24:34]), 2)], item.text.encode('ascii', 'ignore')[12:22]]
collectDayDayHappyItems = lambda item: [item['Drawdate'], [item['Sb1'], item['Sb2'], item['Sb3'], item['Sb4'], item['Sb5']]]


def removeDuplicatDictInList(l):
    return [dict(t) for t in {tuple(d.items()) for d in l}]


class informationUtil(object):
    eachIssueInformation = []
    Lotto = 'Lotto'
    SixColor = 'SixColor'
    FiveThreeNine = 'FiveThreeNine'
    DayDayHappy = 'DayDayHappy'
    CurrentYear = 2019

    def __init__(self, type=SixColor, collectYear=2019):
        self.collectYear = collectYear
        self.init(type)

    def getTempDict(self, type='Lotto'):
        if type == self.Lotto or type == self.SixColor:
            tempDict = {
                "Date": "",
                "Type": type,
                1: "",
                2: "",
                3: "",
                4: "",
                5: "",
                6: "",
                7: ""
            }
        elif type == self.FiveThreeNine:
            tempDict = {
                "Issue": "",
                "Type": type,
                "Numbers": []
            }
        return tempDict

    def getLottoData(self):
        recordList = []
        for page in range(0, 18):
            payload = {
                "indexpage": page,
                "orderby": "old"
            }
            returnDict = requests.get("https://www.lotto-8.com/listltobig.asp", params=payload,
                                      headers={'content-type': 'application/json'}, stream=True)
            parsed_html = BeautifulSoup(returnDict.text)
            List = parsed_html.body.findAll('td')
            index = 0
            result = ''
            result.split(',')
            tempDict = self.getTempDict()
            for item in List:
                if len(item.attrs) > 1:
                    if (u'style', u'border-bottom-style: dotted; border-bottom-color: #CCCCCC; background-color: #CCCCCC;font-size:24px') in item.attrs:
                        continue
                    if (u'class', u'auto-style5') in item.attrs:
                        result = item.text.replace('&nbsp;', '')
                        if result != '':
                            if index == 0:
                                index += 1
                                tempDict['Date'] = result.encode('ascii', 'ignore').replace('/', '-')
                            elif index == 1:
                                index += 1
                                numberList = result.split(',')
                                count = 0
                                indexCount = 1
                                while count < len(numberList):
                                    tempDict[indexCount] = int(numberList[count])
                                    count += 1
                                    indexCount += 1
                            elif index == 2:
                                index = 0
                                tempDict[7] = int(result)
                                recordList.append(tempDict.copy())
        return recordList

    def getFiveThreeNineYearData(self, year):
        returnDict = requests.get('https://lotto.auzonet.com/daily539/list_%s_all.html' % year, headers={'content-type': 'application/json'}, stream=True)
        parsed_html = BeautifulSoup(returnDict.text)
        return parsed_html.body.findAll('td', attrs={"class": "history_view_Lottery"})

    def getDayDayHappyData(self):
        returnDict = requests.get('http://60.249.253.146:8011/api/ed')
        return json.loads(returnDict.text)

    def getSixAndColorYearData(self, year):
        payload = {
            "year": year,
            "sort": "seq"
        }
        returnDict = requests.get("https://www.cpzhan.com/liu-he-cai/all-results/", params=payload,
                                  headers={'content-type': 'application/json'}, stream=True)
        parsed_html = BeautifulSoup(returnDict.text)
        print 'Year: %s Extracted' % year
        return parsed_html.body.findAll('td')

    def init(self, type):
        if type == self.Lotto:
            self.eachIssueInformation = self.getLottoData()
            # print self.eachIssueInformation
        elif type == self.SixColor:
            collectYear = range(2008, self.CurrentYear + 1)
            startRecord = False
            recordCount = 1
            recordList = []
            for year in collectYear:
                yearDataList = self.getSixAndColorYearData(year=year)
                for item in yearDataList:
                    if len(item.attrs) > 0:
                        startRecord = True
                        tempDict = self.getTempDict(type='SixColor')
                        tempDict['Date'] = item.text.encode('ascii', 'ignore')
                        continue

                    if startRecord:
                        tempDict[recordCount] = int(item.text)
                        recordCount += 1

                    if recordCount == 8:
                        recordList.append(tempDict)
                        recordCount = 1
                        startRecord = False
            self.eachIssueInformation = recordList
        elif type == self.FiveThreeNine:
            collectYear = range(self.collectYear, self.CurrentYear + 1)
            dictList = []
            for year in reversed(collectYear):
                print 'Collecting Year %s Data' % year
                yearDataList = self.getFiveThreeNineYearData(year)
                recordList = map(collectFiveThreeNineItems, yearDataList)
                tempDictList = map(lambda item: {
                    "Issue": item[0],
                    "Type": type,
                    "Numbers": item[1],
                    "Date": item[2]
                }, recordList)
                for item in tempDictList:
                    while tempDictList.count(item) > 1:
                        tempDictList.remove(item)

                dictList += tempDictList

            with open(os.path.join('Log', 'issueInformation'), 'w+') as infile:
                for element in reversed(dictList):
                    infile.write('%s\n' % json.dumps(element, indent=4))

            self.eachIssueInformation = dictList
        elif type == self.DayDayHappy:
            recordJson = self.getDayDayHappyData()
            recordList = map(collectDayDayHappyItems, recordJson)
            dictList = []
            for data in recordList:
                if int(data[0][0:4]) >= self.collectYear:
                    tempDict = {
                        "Issue": 'XX',
                        "Type": type,
                        "Numbers": data[1],
                        "Date": data[0]
                    }
                    dictList.append(tempDict)
            self.eachIssueInformation = dictList