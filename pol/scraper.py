#-*- coding: utf-8 -*-
"""
    Requirements:
    - requests (installation: pip install requests)
    - BeautifulSoup (installation: pip install beautifulsoup4)
    - slate (installation: pip install slate)
"""
import urllib,urllib2
from bs4 import BeautifulSoup
import os

def download_file(pdf_url, fileName):
	urllib.urlretrieve(pdf_url, fileName+'.pdf')

	docID = pdf_url[-13:-7]
	doc_url = "http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-%2f%2fEP%2f%2fNONSGML%2bWQ%2bE-2016-"+docID+"%2b0%2bDOC%2bWORD%2bV0%2f%2fEN"
	print(doc_url)
	urllib.urlretrieve(doc_url,fileName+'.doc')
	os.system("pdftotext "+'"'+fileName+'.pdf'+'"')

def getPages(html_data):
	soup = BeautifulSoup(html_data)
	raw_num = soup.find('div', class_="ep_elementtext").find('a').getText() 
	return int(raw_num[raw_num.index('(')+1:-1])/10

url = "http://www.europarl.europa.eu/RegistreWeb/search/typedoc.htm?codeTypeDocu=QECR&year=2016&lg=EN&currentPage=1"
html_data = urllib2.urlopen(url)
pages = getPages(html_data)

for i in range(1, pages+1):
	url = "http://www.europarl.europa.eu/RegistreWeb/search/typedoc.htm?codeTypeDocu=QECR&year=2016&lg=EN&currentPage="+str(i)
	html_data = urllib2.urlopen(url)
	soup = BeautifulSoup(html_data)
	questions = soup.find_all('div', class_="results")[0].find_all('a', target="_blank")
	names = soup.find_all('div', class_="results")[0].find_all('span', class_="reference")[::2]
	for q,n in zip(questions,names):
		name = n.getText().replace('\n','').replace('\t','').replace(' ','')
		download_file(q['href'], name.encode('utf-8'))