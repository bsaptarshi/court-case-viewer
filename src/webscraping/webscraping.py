from lxml import html
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import pprint
from datetime import date
import json
import sys
import json


headerData = {}
bodyData = []


urlBase = "http://localhost:8000"
keyMap = {'0' : 'serial', '1' : 'case_no', '2' : 'party', '3' : 'petitionar_advocates', '4' : 'respondent_advocates'}
toJSONMap = {'serial' : 'serial', 'case_no' : 'case_no', 'party' : 'party', 'petitionar_advocates' : 'petitionar_advocates', 'respondent_advocates' : 'respondent_advocates'}

# serialNumber = 'NONE'
caseNumber = 'ABCD'
cNo = '-1'
slNo = '-1'

caseData = []


def scrapehelper(argv):
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
            r2 = requests.post ("http://clists.nic.in/viewlist/search_result.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php","DNT":"1"}, data={"case":"COURT", "date": todayString, "q":""})
            courtNos = getAvailableCourts (r2.text)
            for court in courtNos:
                r3 = requests.post("http://clists.nic.in/viewlist/search_result_final.php",headers={"Cookie":sessionIDString,"Referer":"http://clists.nic.in/viewlist/search_result.php","DNT":"1"},data={"court_wise":court.text,"court_wise_submit":"Submit","q":""})
                parseHTMLtoJSON(r3.text)

            #sending predefined json to web service for now.
            json_file = open ('json_sample', 'r')
            json_data = json_file.read ()
            print json_data
            r = requests.post ("url", data={"body": json_data, "date":"25-11-2015", "court":"13"})

        

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
    # print tables
    storeHeader(allTables[0])
    bodyTables = soup.findChildren('table', {'class':'style3'})
    storeBody(bodyTables)


def storeBody(bodyText):
    # print "Body Length = ", len(bodyText)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint (bodyText)
    num = 0;
    for body in range(0,len(bodyText)):#len(bodyText)
        rowData = extractBodyText(bodyText[body])
        bodyData.insert(num, rowData)
        num = num + 1

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(bodyData)
    # convertToJSON(bodyData)

    print "--------------------------FINAL CASEDATA---------------------------------"
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(caseData) 
    # print caseData

def extractBodyText(row):
    # print "----------------NEW ROW---------------------"
    rowData = storeRowData(row)
    children = row.findChildren('tr')
    caseNo = ''
    serialNo = ''
    for child in children:
        newData = parseChildren(child, caseNo, serialNo)
        # print "++++++++++++++++PARSED DATA++++++++++++++++"
        # print newData
    # print children
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(row)
    # print "++++++++++++++++PARSED DATA++++++++++++++++"
    # pp.pprint(rowData)
    return rowData


def parseChildren(data, caseNo, serialNo):
    elem = data.findChildren('td')
    if not elem:
        print "empty list"
        return

    # print "---------------------New Child--------------------------"
    # print data
    count = 0;
    global caseNumber
    global cNo
    global slNo
    dataSet = {'serial':'', 'case_no':'', 'party':'', 'petitionar_advocates':'', 'respondent_advocates':''}
    for e in elem:
        currKey = keyMap[str(count%5)]
        elemText = str(e.find('pre-line')).replace ("<pre-line>","").replace ("</pre-line>","")

        if (currKey == 'case_no'):
            # if (((elemText != 'None') or (elemText != '\xc2\xa0')) and (elemText != serialNumber)):
            #     serialNumber = elemText
            # print "------------------> ELEMTEXT = ", elemText
            if (elemText != caseNumber and elemText != "None" and elemText != "\xc2\xa0"):
                # print ("updating old case no "+caseNumber+" with "+elemText)
                caseNumber = elemText
                # print "--------------Dataset------------------"
                # print dataSet
            # print "------------------> CASE NUMBER = ", caseNumber
        
        if (currKey == 'serial'):
            if (elemText != slNo and elemText != "None" and elemText != "\xc2\xa0" and elemText != "WITH"):
                # print ("updating old serial no "+slNo+" with "+elemText)
                slNo = elemText
                # print "--------------Dataset------------------"
                # print dataSet
            # print "------------------> SERIAL Number = ", slNo

        if ((elemText == 'None') or (elemText == '\xc2\xa0')):
            # if (currKey == 'serial'):
            #     print elemText
            count = count + 1
            continue
        if (dataSet[currKey] != ''):
            dataSet[currKey] += " | " + elemText
        else:
            dataSet[currKey] += elemText
        if e.has_attr("colspan"):
            count = count + int(e['colspan'])
        else:
            count = count + 1

    if (cNo != caseNumber):
        cNo = caseNumber
        # print "Different Case Number Found--------------Dataset------------------"
        # print "Serial Number = ", slNo
        dataSet['serial'] = slNo
        # print dataSet
        convertAndStoreToJSON(dataSet)

    return dataSet


def storeRowData(data):
    elem = data.findChildren('td')
    count = 0;
    dataSet = {'serial':'', 'case_no':'', 'party':'', 'petitionar_advocates':'', 'respondent_advocates':''}
    for e in elem:
        currKey = keyMap[str(count%5)]
        elemText = str(e.find('pre-line')).replace ("<pre-line>","").replace ("</pre-line>","")

        # if (currKey == 'serial'):
        #     if (((elemText != 'None') or (elemText != '\xc2\xa0')) and (elemText != serialNumber)):
        #         serialNumber = elemText
        #         print "SERIAL  NUMBER = ", serialNumber
        if ((elemText == 'None') or (elemText == '\xc2\xa0')):
            # if (currKey == 'serial'):
            #     print elemText
            count = count + 1
            continue
        if (dataSet[currKey] != ''):
            dataSet[currKey] += " | " + elemText
        else:
            dataSet[currKey] += elemText
        if e.has_attr("colspan"):
            count = count + int(e['colspan'])
        else:
            count = count + 1
    return dataSet

def convertAndStoreToJSON(data):
    data['petitionar_advocates'] = data['petitionar_advocates'].split('<br>')
    data['respondent_advocates'] = data['respondent_advocates'].split('<br>')
    toJson = json.dumps(data)
    caseData.append(toJson)



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

if __name__ == '__main__':
    # print "serial = ", serialNumber
    scrapehelper(sys.argv[1:])
