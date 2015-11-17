from lxml import html
import requests
from bs4 import BeautifulSoup

def scrapehelper():
	r0 = requests.get ('http://clists.nic.in/viewlist/index.php?court=VTNWd2NtVnRaU0JEYjNWeWRDQnZaaUJKYm1ScFlRPT0=&q=TkRZeU5UQXpaV1kwWldNeVpHWmlOVGxoWXpFNFlqRXdOVE5pWmpNd00yVT0=')
	sessionID = r0.headers['Set-Cookie'].split('=', 1)[1].split(';')[0]

	sessionIDString = "PHPSESSID="+sessionID
	r1 = requests.post ("http://clists.nic.in/viewlist/index.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php?court=VTNWd2NtVnRaU0JEYjNWeWRDQnZaaUJKYm1ScFlRPT0=","DNT":"1"}, data={"listtype":"DAILY LIST OF REGULAR HEARING MATTERS", "submit_list_value": "submit", "q":""})
	r2 = requests.post ("http://clists.nic.in/viewlist/search_result.php", headers= {"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/index.php","DNT":"1"}, data={"case":"COURT", "date": "06-11-2015", "q":""})
	r3 = requests.post ("http://clists.nic.in/viewlist/search_result_final.php", headers={"Cookie": sessionIDString, "Referer":"http://clists.nic.in/viewlist/search_result.php","DNT":"1"}, data={"court_wise":"Court No. 10","court_wise_submit":"Submit","q":""})
	parseHTMLtoJSON(r3.text)
	

def parseHTMLtoJSON(htmlText):
	# print htmlText
	soup = BeautifulSoup(htmlText, 'html.parser')
	# print soup.prettify()

	tables = soup.findChildren('table')
	print len(tables)
	# print tables[0]
	# print tables[1]
	# print tables[2]
	# print tables[3]
	print tables[4].prettify()
if __name__ == '__main__':
	scrapehelper()
