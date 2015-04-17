# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "DCM048_DFCMAS_gov"
url = "https://www.gov.uk/government/publications/transactions-over-25k-2013-2014"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
blocks = soup.findAll('div', {'class':'attachment-details'})

for block in blocks:

	link = block.a['href']
	title = block.h2.contents[0]
	
	# Some of our tags aren't consistent and bury the 'a' tag within the H2 tag
	if hasattr(title,"href"):
		title = title.text.strip()

	# add the right prefix onto the url
	csvUrl = link.replace("/preview","")
	csvUrl = csvUrl.replace("/government","http://www.gov.uk/government")
	#print csvUrl

	# create the right strings for the new filename
	csvYr = title.split(' ')[-1]
	csvMth = title.split(' ')[-2][:3]
	csvMth = csvMth.upper()
	csvMth = convert_mth_strings(csvMth);
	
	filename = entity_id + "_" + csvYr + "_" + csvMth + ".csv"
	
	todays_date = str(datetime.now())
	
	scraperwiki.sqlite.save(unique_keys=['l'], data={"l": csvUrl, "f": filename, "d": todays_date })
	
	print filename
