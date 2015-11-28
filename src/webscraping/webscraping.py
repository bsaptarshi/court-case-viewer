from lxml import html
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import sys
import json


headerData = {}
bodyData = []


urlBase = "http://localhost:8000"
keyMap = {'0' : 'serial', '1' : 'case_no', '2' : 'party', '3' : 'petitionar_advocates', '4' : 'respondent_advocates'}
toJSONMap = {'serial' : 'serial', 'case_no' : 'case_no', 'party' : 'party', 'petitionar_advocates' : 'petitionar_advocates', 'respondent_advocates' : 'respondent_advocates'}

caseNumber = 'ABCD'
cNo = '-1'
slNo = '-1'
serialNumber = '-101'

caseData = []
tempDataSet = {'serial':'', 'case_no':'', 'party':'', 'petitionar_advocates':'', 'respondent_advocates':''}
finalData = {'date' : '', 'courts' : ''}
finalDataToJSON = ''
dateOfData = ''


def scrapehelper(argv):
    global dateOfData
    if len (argv) == 1:
        daemon = "y"
    else:
        daemon = "n"
    if daemon == "n":
        testOrScrape = raw_input ("Use sample file for testing (y/n):")
        if testOrScrape == "n":
            r0 = requests.get ('http://clists.nic.in/viewlist/index.php?court=VTNWd2NtVnRaU0JEYjNWeWRDQnZaaUJKYm1ScFlRPT0=&q=TkRZeU5UQXpaV1kwWldNeVpHWmlOVGxoWXpFNFlqRXdOVE5pWmpNd00yVT0=')
            sessionID = r0.headers['Set-Cookie'].split('=', 1)[1].split(';')[0]

            sessionIDString = "PHPSESSID="+sessionID
            r1 = requests.post ("http://clists.nic.in/viewlist/index.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php?court=VTNWd2NtVnRaU0JEYjNWeWRDQnZaaUJKYm1ScFlRPT0=","DNT":"1"}, data={"listtype":"DAILY LIST OF REGULAR HEARING MATTERS", "submit_list_value": "submit", "q":""})
            getAvailableDates (r1.text)
            print "-----"
            dates = raw_input ("Enter data in DD-MM-YYYY: ")
            dateOfData = dates
            r2 = requests.post ("http://clists.nic.in/viewlist/search_result.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php","DNT":"1"}, data={"case":"COURT", "date": dates, "q":""})
            courtNos = getAvailableCourts (r2.text)
            print "-----"
            court = raw_input ("Enter Court No: ")
            r3 = requests.post("http://clists.nic.in/viewlist/search_result_final.php",headers={"Cookie":sessionIDString,"Referer":"http://clists.nic.in/viewlist/search_result.php","DNT":"1"},data={"court_wise":"Court No. "+court,"court_wise_submit":"Submit","q":""})
            parseHTMLtoJSON(r3.text)
        else:
            sample = open ('sample.html', 'r')
            parseHTMLtoJSON(sample.read ())
    else:
        if argv[0] == "sample":
            #print "Reading from sample"
            sample = open ('mySample.html', 'r')
            parseHTMLtoJSON(sample.read ())
            #sending predefined json to web service for now.

            json_file = open ('json_sample', 'r')
            json_data = json.load(json_file)            
            r = requests.post (urlBase+"/cases/scrape/", data = json.dumps(json_data))
            print "======================================================================="
            print r.text

        else:
            today = date.today ()
            r0 = requests.get ('http://clists.nic.in/viewlist/index.php?court=VTNWd2NtVnRaU0JEYjNWeWRDQnZaaUJKYm1ScFlRPT0=&q=TkRZeU5UQXpaV1kwWldNeVpHWmlOVGxoWXpFNFlqRXdOVE5pWmpNd00yVT0=')
            sessionID = r0.headers['Set-Cookie'].split('=', 1)[1].split(';')[0]

            sessionIDString = "PHPSESSID="+sessionID
            r1 = requests.post ("http://clists.nic.in/viewlist/index.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php?court=VTNWd2NtVnRaU0JEYjNWeWRDQnZaaUJKYm1ScFlRPT0=","DNT":"1"}, data={"listtype":"DAILY LIST OF REGULAR HEARING MATTERS", "submit_list_value": "submit", "q":""})
            todayString = today.strftime ('%d-%m-%Y')
            dateOfData = todayString
            r2 = requests.post ("http://clists.nic.in/viewlist/search_result.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php","DNT":"1"}, data={"case":"COURT", "date": todayString, "q":""})
            courtNos = getAvailableCourts (r2.text)
            for court in courtNos:
                r3 = requests.post("http://clists.nic.in/viewlist/search_result_final.php",headers={"Cookie":sessionIDString,"Referer":"http://clists.nic.in/viewlist/search_result.php","DNT":"1"},data={"court_wise":court.text,"court_wise_submit":"Submit","q":""})
                parseHTMLtoJSON(r3.text)

            #sending predefined json to web service for now.
            # json_file = open ('json_sample', 'r')
            # json_data = json_file.read ()
            # print json_data
            # Access finalDataToJSON var to get the final data in JSON form
           
            #r = requests.post ("url", data={"body": finalDataToJSON, "date":"25-11-2015", "court":"13"})
            
            r = requests.post (urlBase+"/cases/scrape/", data = json.dumps(finalDataToJSON))
            print r.text

        

def getAvailableDates (htmlText):
    soup = BeautifulSoup (htmlText, 'html.parser')
    options = soup.findChildren ('option')
    for option in options:
        print option.text

def getAvailableCourts (htmlText):
    soup = BeautifulSoup (htmlText, 'html.parser')
    options = soup.findChildren ('option')
    return options

def parseHTMLtoJSON(htmlText):
    soup = BeautifulSoup(htmlText, 'html.parser')
    allTables = soup.findChildren('table')
    storeHeader(allTables[0])
    bodyTables = soup.findChildren('table', {'class':'style3'})
    storeBody(bodyTables)


def storeBody(bodyText):
    num = 0;
    for body in range(0,len(bodyText)):#len(bodyText)
        extractBodyText(bodyText[body])

    tempDataSet['serial'] = slNo
    formatCaseData(tempDataSet)
    renderFullJSON()

def extractBodyText(row):
    children = row.findChildren('tr')
    caseNo = ''
    serialNo = ''
    for child in children:
        parseChildren(child)


def parseChildren(data):
    elem = data.findChildren('td')
    if not elem:
        return

    count = 0;
    global caseNumber
    global cNo
    global slNo
    global serialNumber
    global tempDataSet

    for e in elem:
        currKey = keyMap[str(count%5)]
        elemText = str(e.find('pre-line')).replace ("<pre-line>","").replace ("</pre-line>","")

        if (currKey == 'case_no'):
            if (cNo == '-1'):
                cNo = elemText
            if (elemText != caseNumber and elemText != "None" and elemText != "\xc2\xa0"):
                caseNumber = elemText
        
        if (cNo != caseNumber and cNo != '-1'):
            cNo = caseNumber
            tempDataSet['serial'] = slNo

            if (tempDataSet['petitionar_advocates'] != ""):
                formatCaseData(tempDataSet)
                tempDataSet = {'serial':'', 'case_no':'', 'party':'', 'petitionar_advocates':'', 'respondent_advocates':''}

        if (currKey == 'serial'):
            if (serialNumber == '-101'):
                serialNumber = elemText
            if (elemText != slNo and elemText != "None" and elemText != "\xc2\xa0" and elemText != "WITH"):
                slNo = elemText

        if (serialNumber != slNo and serialNumber != '-101'):
            tempDataSet['serial'] = serialNumber
            serialNumber = slNo
            if (tempDataSet['petitionar_advocates'] != ""):
                formatCaseData(tempDataSet)
                tempDataSet = {'serial':'', 'case_no':'', 'party':'', 'petitionar_advocates':'', 'respondent_advocates':''}

        if ((elemText == 'None') or (elemText == '\xc2\xa0')):
            count = count + 1
            continue

        if (tempDataSet[currKey] != ''):
            tempDataSet[currKey] += " <br> " + elemText
        else:
            tempDataSet[currKey] += elemText

        if e.has_attr("colspan"):
            count = count + int(e['colspan'])
        else:
            count = count + 1

def formatCaseData(data):
    if type(data['petitionar_advocates']) is str:
        data['petitionar_advocates'] = data['petitionar_advocates'].split('<br>')
    if type(data['respondent_advocates']) is str:
        data['respondent_advocates'] = data['respondent_advocates'].split('<br>')
    caseData.append(data)



def storeHeader(headerText):
    children = headerText.find('td')
    contentText = re.sub('<[^<]+?>', '&&&', children.renderContents().strip()).split('&&&')
    courtNo = contentText[0].split(' ')[2].strip()
    justice1 = contentText[1].strip()
    justice2 = contentText[2].strip()

    headerData["CourtNo"] = courtNo
    headerData["Justice1"] = justice1
    headerData["Justice2"] = justice2
        
    print "Court No: ", courtNo
    print "Justice 1: ", justice1
    print "Justice 2: ", justice2
    print "-----"

def renderFullJSON():
    global finalDataToJSON
    global finalData
    tempFinalData = {"court_no" : '', "judge" : '', "case" : ''}
    tempFinalData['court_no'] = headerData["CourtNo"]
    tempFinalData['judge'] = headerData["Justice1"] + "<br>" +headerData["Justice2"]
    tempFinalData['case'] = caseData
    finalData['date'] = dateOfData
    finalData['courts'] = {'court' : ''}
    finalData['courts']['court'] = tempFinalData
    tempFinalData = {"court_no" : '', "judge" : '', "case" : ''}
    finalDataToJSON = json.dumps(finalData)

    # print "--------------------------FINAL JSONDATA---------------------------------"
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(finalDataToJSON)


if __name__ == '__main__':
    scrapehelper(sys.argv[1:])
