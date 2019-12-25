from inforUtil import informationUtil
import json
from fivethreeninefeatureutil import fiveThreeNineFeatureUtil
from collections import OrderedDict
import os
import xlsxwriter

allLocksXlsxPath = os.path.join('report', 'reportAllLockCounts.xlsx')
eachIssueXlsxPath = os.path.join('report', 'reportEachIssue.xlsx')

if __name__ == '__main__':
    informationDay = informationUtil(informationUtil.DayDayHappy, collectYear=2019)
    informationFive = informationUtil(informationUtil.FiveThreeNine, collectYear=2019)
    fiveThreeNineInfoListBack = informationFive.eachIssueInformation
    dayDayHappyList = informationDay.eachIssueInformation

    fiveThreeNineInfoList = fiveThreeNineInfoListBack + dayDayHappyList
    fiveThreeNineInfoList = sorted(fiveThreeNineInfoListBack + dayDayHappyList, key=lambda k: k['Date'], reverse=True)

    for item in fiveThreeNineInfoList:
        print json.dumps(item, indent=4)
    fiveThreeNineFeatures = fiveThreeNineFeatureUtil()
    tailNumberRange = range(10)

    if os.path.exists(allLocksXlsxPath):
        os.remove(allLocksXlsxPath)

    if os.path.exists(eachIssueXlsxPath):
        os.remove(eachIssueXlsxPath)

    eachIssueReport = xlsxwriter.Workbook(eachIssueXlsxPath)
    cell_format = eachIssueReport.add_format()
    cell_format.set_font_size(18)
    cell_format.set_align("center")

    row = 0
    column = 0
    eachIssueWorkSheet = eachIssueReport.add_worksheet()
    eachIssueWorkSheet.set_column("A:Q", 24)

    eachIssueWorkSheet.write(row, column, 'Date\\Number', cell_format)
    column = column + 1
    for number in tailNumberRange:
        eachIssueWorkSheet.write(row, column, number, cell_format)
        column = column + 1

    row += 1
    column = 0
    for eachIssueInformation in fiveThreeNineInfoList:
        issue = eachIssueInformation['Issue']
        playType = eachIssueInformation['Type']
        numbers = eachIssueInformation['Numbers']
        date = eachIssueInformation['Date']
        tailNumbers = sorted(list(set(map(lambda number: str(int(number) % 10), numbers))))
        fiveThreeNineFeatures.addInformation(tailNumbers, date)
        eachIssueWorkSheet.write(row, column, '%s %s' % (date, playType), cell_format)

        for number in tailNumberRange:
            if str(number) in tailNumbers:
                eachIssueWorkSheet.write(row, number + 1, 'V', cell_format)

        row += 1

    eachIssueReport.close()
    maxNumber = 0
    lockCountsDict = OrderedDict(sorted(fiveThreeNineFeatureUtil.lockCountsDict.items(), key=lambda t: t[0]))
    for key, value in lockCountsDict.items():
        for key2 in value:
            if int(key2) > maxNumber:
                maxNumber = int(key2)

    numberRange = range(maxNumber + 1)
    xlsxFile = xlsxwriter.Workbook(allLocksXlsxPath)
    cell_format = xlsxFile.add_format()
    cell_format.set_font_size(18)
    cell_format.set_align("center")

    worksheet = xlsxFile.add_worksheet()
    worksheet.set_column("A:Q", 24)

    row = 0
    column = 0

    worksheet.write(row, column, 'Numbers\\Locks', cell_format)
    column = column + 1
    for lock in numberRange:
        worksheet.write(row, column, lock, cell_format)
        column = column + 1

    row += 1
    column = 0

    for key, value in lockCountsDict.items():
        worksheet.write(row, column, key, cell_format)
        column += 1
        sum = 0
        for lockNumber in value:
            sum += value[lockNumber]

        for lockNumber in value:
            worksheet.write_number(row, int(lockNumber) + 1, float(value[lockNumber]) / float(sum) * 100, cell_format)

        row = row + 1
        column = 0

    xlsxFile.close()
