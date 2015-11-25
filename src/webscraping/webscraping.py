from lxml import html
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import pprint
from datetime import date
import sys


headerData = {}
bodyData = []
keyMap = {'0' : 'SLNO', '1' : 'CASENO', '2' : 'PARTY', '3' : 'PETADV', '4' : 'RESADV'}

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
	tables = soup.findChildren('table')
#	print len(tables)
	storeHeader(tables[0])
	storeBody(tables)


def storeBody(bodyText):
    for body in range(1,2):#len(bodyText)
        extractBodyText(bodyText[body])

def extractBodyText(row):
	datas = row.findChildren('tr')

	# pp1 = pprint.PrettyPrinter(indent=4)
	# pp1.pprint(datas)
	num = 0;
	for data in datas:
		rowData = storeRowData(data)
		# print rowData
		bodyData.insert(num, rowData)
		num = num + 1

	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(bodyData)
            
def storeRowData(data):
	# print "PRINTING RAW DATA"
	# print data.prettify()
	elem = data.findChildren('td')
	count = 0;
	dataSet = {'SLNO':'', 'CASENO':'', 'PARTY':'', 'PETADV':'', 'RESADV':''}
	for e in elem:
		# print "COUNT = ", count%5
		currKey = keyMap[str(count%5)]
		dataSet[currKey] += str(e.find('pre-line')).replace ("<pre-line","").replace ("/pre-line>","")
		if e.has_attr("colspan"):
			count = count + int(e['colspan'])
		else:
			count = count + 1
		
		# print "COUNT = ", count%5

	# print "PRINTING DATASET"	
	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(dataSet)
	return dataSet



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
    scrapehelper(sys.argv[1:])
