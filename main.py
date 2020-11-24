from bs4 import BeautifulSoup as bs
import requests
import re

global _urls
_urls = None

states = ["Alabama", "Alaska", "Arizona", "Arkansas",
"California", "Colorado", "Connecticut",
"Delaware",
"Florida",
"Georgia",
"Hawaii",
"Idaho", "Illinois", "Indiana", "Iowa",
"Kansas", "Kentucky",
"Louisiana",
"Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
"Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
"Ohio", "Oklahoma", "Oregon", 
"Pennsylvania",
"Rhode Island",
"South Carolina",
"South Dakota",
"Tennessee", "Texas",
"Utah",
"Vermont", "Virginia",
"Washington", "West Virgina", "Wisconsin", "Wyoming",
]

working_states = ["Alabama", "Alaska", "Arizona", "Arkansas",
"California", "Colorado", "Connecticut",
"Florida",
"Georgia",
"Idaho", "Illinois", "Indiana", "Iowa",
"Kansas", "Kentucky",
"Louisiana",
"Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
"Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
"Ohio", "Oklahoma",
"Pennsylvania",
"Rhode Island",
"South Carolina",
"South Dakota",
"Tennessee", "Texas",
"Utah",
"Vermont",
"Washington", "West Virgina", "Wisconsin", "Wyoming",
]


def loadURLs():
	# loadURLs reads in the wikipedia page containing links to the articles we're going to scrape data from
	resp = requests.get('https://en.wikipedia.org/wiki/Lists_of_populated_places_in_the_United_States')
	
	if resp.status_code != 200:
		return None
	
	global _urls
	_urls = {}
		
	soup = bs(resp.text, 'html.parser')
	for link in soup.find_all('a'):
		if 'Cities' not in link.text and 'Municipalities' not in link.text:
			continue
		
		parts = re.search('in (.*)$', link.text)
		if parts is None:
			parts = re.search('of (.*)$', link.text)
		if parts is None:
			continue
		
		_urls[parts[1]] = link['href']
		

def getParsedHTML(state):
	# getParsedHTML fetches the HTML for the given states wikipedia page for cities and parses it with BeautifulSoup
	global _urls
	if _urls is None:
		loadURLs()
	
	if state not in _urls:
		return None

	url = 'https://en.wikipedia.org' + _urls[state]
	resp = requests.get(url)
	
	if resp.status_code != 200:
		return None
	
	return bs(resp.text, 'html.parser')

def getTable(parsedHTML):
	# getTable finds the table with the city - county info from the parsedHTML
	return parsedHTML.find('table', class_='sortable')
	
def getCountyIndex(table):
	# getCountyIndex finds the index of the column which contains the county data
	for idx, header in enumerate(table.find_all('th')):
		if 'ounty' in header.text or 'ount(ies)' in header.text: # Iowa uses 'Count(ies)' for some reason
			return idx
	
	# if the state doesn't have counties check for census area/borough/parish
	for idx, header in enumerate(table.find_all('th')):
		if 'ensus' in header.text or 'orough' in header.text or 'arish' in header.text:
			return idx

	return None
	
def getTableAsDict(table):
	# getTableAsDist transforms the table from a BeautifulSoup element into a python dictionary
	rows = table.find_all('tr')[1:] # the first to rows always seem to be header data
	countyIndex = getCountyIndex(table)
	
	# check if the first column is a th element, if so decrement countyIndex by 1
	if len(rows[3].find_all('th')) != 0 and countyIndex != 0:
		countyIndex -= 1
	
	data = {}
	for row in rows:
		# check if we hit the bottom of the table
		if row.has_attr('class') and row['class'][0] == "sortbottom":
			continue
		
		columns = row.find_all('td')
		if len(columns) < countyIndex:
			continue
		

		# extract city name from row
		link = row.find('a')
		if link is None:
			continue
		city = link.text.strip('†').strip()
		
		# extract county name from row
		link = columns[countyIndex].find('a')
		county = None
		if link is None:
			# probably okay to just grab the text here
			county = columns[countyIndex].text
		if county is None:
			# make sure that we didnt come across a reference link.
			# if so, then grab this elements text only and not any of its childrens text
			if '[' not in link.text:
				county = link.text
			else:
				county = columns[countyIndex].find(text=True,recursive=False)
				
		county = county.strip('†').strip()
		
		if county not in data:
			data[county] = []
		
		data[county].append(city)
	
	return data
	
def getDictForState(state):
	# getDictForState returns a dict of counties and cities for the state
	html = getParsedHTML(state)
	if html is None:
		return None
	table = getTable(html)

	return getTableAsDict(table)
	
def getDict():
	# getDict returns a dictionary with all of the states as dicionaries containing their counties and cites.
	data = {}
	for state in working_states:
		data[state] = getDictForState(state)
	return data
