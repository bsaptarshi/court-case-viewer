from lxml import html
import requests
from bs4 import BeautifulSoup
import re

headerData = {}
def scrapehelper():
	r0 = requests.get ('http://clists.nic.in/viewlist/index.php?court=VTNWd2NtVnRaU0JEYjNWeWRDQnZaaUJKYm1ScFlRPT0=&q=TkRZeU5UQXpaV1kwWldNeVpHWmlOVGxoWXpFNFlqRXdOVE5pWmpNd00yVT0=')
	sessionID = r0.headers['Set-Cookie'].split('=', 1)[1].split(';')[0]

	sessionIDString = "PHPSESSID="+sessionID
	r1 = requests.post ("http://clists.nic.in/viewlist/index.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php?court=VTNWd2NtVnRaU0JEYjNWeWRDQnZaaUJKYm1ScFlRPT0=","DNT":"1"}, data={"listtype":"DAILY LIST OF REGULAR HEARING MATTERS", "submit_list_value": "submit", "q":""})
        getAvailableDates (r1.text)
        date = raw_input ("Enter data in DD-MM-YYYY: ")
        r2 = requests.post ("http://clists.nic.in/viewlist/search_result.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php","DNT":"1"}, data={"case":"COURT", "date": date, "q":""})
        getAvailableCourts (r2.text)
        courtNo = input ("Enter CourtNo:")
	r3 = requests.post("http://clists.nic.in/viewlist/search_result_final.php",headers={"Cookie":sessionIDString,"Referer":"http://clists.nic.in/viewlist/search_result.php","DNT":"1"},data={"court_wise":"Court No. " + `courtNo`,"court_wise_submit":"Submit","q":""})
	parseHTMLtoJSON(r3.text)

def getAvailableDates (htmlText):
    soup = BeautifulSoup (htmlText, 'html.parser')
    options = soup.findChildren ('option')
    print "Available Dates"
    for option in options:
        print option.text

def getAvailableCourts (htmlText):
    soup = BeautifulSoup (htmlText, 'html.parser')
    options = soup.findChildren ('option')
    print "Available Courts:"
    for option in options:
        print option.text

def parseHTMLtoJSON(htmlText):
	soup = BeautifulSoup(htmlText, 'html.parser')

	tables = soup.findChildren('table')
	storeHeader(tables[0])
            
	

def storeHeader(headerText):
	children = headerText.find('td')
	contentText = re.sub('<[^<]+?>', '&&&', children.renderContents().strip()).split('&&&')
	courtNo = contentText[0].split(' ')[2].strip()
	justice1 = contentText[1].strip()
	justice2 = contentText[2].strip()

	headerData["CourtNo"] = courtNo
	headerData["Justice1"] = justice1
	headerData["Justice2"] = justice2

        print courtNo
        print justice1
        print justice2

if __name__ == '__main__':
	scrapehelper()
