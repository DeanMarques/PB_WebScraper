#!/usr/bin/python3.4
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import urllib
from subprocess import call
import transmissionrpc 

class BcColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PirateParser:

	def testFn(self):
		return "pageParser!"

	def searchPage(self, strSearch, pageNumber):

		f = {"q":strSearch, "page":pageNumber, "orderby":"99" }
		str = urllib.parse.urlencode(f)

		webpage = "https://tpbunblocked.org"
		url = webpage + "/s/?" + str;	

		page = requests.get(url)

		links = []

		if (page.status_code == 200):
			soup = BeautifulSoup(page.content, 'html.parser')


			for table in soup.find_all("table", id="searchResult"):
				for tr in table.find_all("tr"):
					tmpLink = []
					counter = 0
					for td in tr.find_all("td"):
						
						# first find link and text
						div = td.find(class_="detName")

						if div:
							link = div.find("a")
							linkAddress = link.get("href")
							tmpLink.append(link.get_text())
							tmpLink.append(webpage + linkAddress)

						if (td.get("align") == "right"):
							tmpLink.append(td.get_text())
							counter += 1
							if (counter == 2):
								links.append(tmpLink)


		else:
			print("Bad status code: " + page.status_code);#
		
		return links

	def getLink(self, url):
		page = requests.get(url)

		if (page.status_code == 200):
			soup = BeautifulSoup(page.content, 'html.parser')

			found = soup.find('div', class_='download')
			magnetLink = found.find('a')

			return magnetLink.get('href')


result = []

def checkInput(str):
	if (str == "exit"):
		return 0
	elif (str == "next"):
		return 1
	elif (str == "search"):
		return 2; 

def getSearchInput():
	return input("Enter search string: ")

print("Starting scraper...")

keepGoing = True

strSearch = getSearchInput()
pp = PirateParser()

pageNumber = 0

firstIndex = 0
while (keepGoing): 
	
	res = pp.searchPage(strSearch,pageNumber)
	
	result.extend(res)

	for i in range(firstIndex, len(result)):
		print(BcColors.OKGREEN + '[' + str(i) + '] ' + BcColors.ENDC, end='')
		print (result[i][0] + " " +  result[i][2] + " " + result[i][3])

	
	firstIndex = len(result);	
	downloadId = input("Pick ID to download: ")

	inputId = checkInput(downloadId)

	if inputId == 0:
		exit()
	elif inputId == 1:
		pageNumber += 1
		continue
	elif inputId == 2:
		result = []
		pageNumber = 0
		firstIndex = 0
		strSearch = getSearchInput()
		continue
	else:
		downloadId = int(downloadId)
		magnetLink = pp.getLink(result[downloadId][1])
		print(magnetLink)
		tc = transmissionrpc.Client('localhost', port=9091, user='pi', password='Studio54')
		tc.add_torrent(magnetLink)
		#call(["deluge-console", "add", magnetLink])


print("Finished!")
