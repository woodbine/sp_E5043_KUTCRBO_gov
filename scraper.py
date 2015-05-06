# -*- coding: utf-8 -*-
import os
import re
import datetime
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5043_KUTCRBO_gov"
url = "http://data.kingston.gov.uk/Kingston_Open_Data/"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string
	
def validateFilename(filename):
	filenameregex = '^[a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+_[0-9][0-9][0-9][0-9]_[0-9][0-9]$'
	dateregex = '[0-9][0-9][0-9][0-9]_[0-9][0-9]'
	validName = (re.search(filenameregex, filename) != None)
	found = re.search(dateregex, filename)
	if not found:
		return False
	date = found.group(0)
	year, month = int(date[:4]), int(date[5:7])
	now = datetime.datetime.now()
	validYear = (2000 <= year <= now.year)
	validMonth = (1 <= month <= 12)
	if all([validName, validYear, validMonth]):
		return True

def validateURL(url):
	try:
		r = requests.get(url, allow_redirects=True)
		return r.status_code == 200
	except:
		return False

def validateFiletype(url):
	try:
		r = requests.head(url, allow_redirects=True)
		sourceFilename = r.headers.get('Content-Disposition')
		if sourceFilename:
			ext = os.path.splitext(sourceFilename)[1].replace('"', '').replace(';', '')
		else:
			ext = os.path.splitext(url)[1]
		if ext in ['.csv', '.xls', '.xlsx']:
			return True
	except:
		return False
		
# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
links = soup.findAll('a', href=True)

for link in links:
	url = link['href']
	if 'https://drive.google.com/file/d/' in url:
		title = link.contents[0]
		# create the right strings for the new filename
		csvYr = title.split(' ')[-1]
		csvMth = title.split(' ')[-2][:3]
		csvMth = csvMth.upper()
		csvMth = convert_mth_strings(csvMth);
		filename = entity_id + "_" + csvYr + "_" + csvMth + ".csv"
		todays_date = str(datetime.now())
		if not validateFilename(filename):
			print "Invalid filename"
			continue
		if not validateURL(url):
			print "Invalid URL"
			continue
		if not validateFiletype(url):
			print "Invalid filetype"
			continue
		scraperwiki.sqlite.save(unique_keys=['l'], data={"l": url, "f": filename, "d": todays_date })
		print filename
