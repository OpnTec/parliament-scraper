#-*- coding: utf-8 -*-
"""
    Requirements:
    - requests (installation: pip install requests)
    - BeautifulSoup (installation: pip install beautifulsoup4)
"""
import requests
from bs4 import BeautifulSoup
import os

base_url = "http://www.europarl.europa.eu/RegistreWeb/search/typedoc.htm?codeTypeDocu=QECR"
cwd = os.getcwd()

def getSoup(url):
    html_data = requests.get(url).text
    soup = BeautifulSoup(html_data)
    return soup


def getFilesLinks(soup):
    return soup.find_all('div', class_="results")[0].find_all(
        'a', target="_blank")


def downloadFile(url):
    content = requests.get(url).content
    name = url.split("/")[-1].encode('utf-8')
    with open(name, "wb") as f:
        f.write(content)


def getYearsAvailable(soup):
    return soup.find_all('div', class_="ep_boxbody")[1].find_all(
        'ul', class_="facet")[0].find_all('a')


def getLangsAvailable(yearLink):
    soup = getSoup(yearLink)
    return soup.find_all('div', class_="ep_boxbody")[1].find_all(
        'ul', class_="facet")[-1].find_all('a')


def getPagesNum(url):
    soup = getSoup(url)
    raw_num = soup.find('div', class_="ep_elementtext").find('a').getText()
    return int(raw_num[raw_num.index('(') + 1:-1]) / 10


def scrapePages(url):
    pages = getPagesNum(url)
    for i in range(1, pages + 1):
        soup = getSoup(url + "&currentPage=" + str(i))
        questions = getFilesLinks(soup)
        for q in questions:
            downloadFile(q['href'])


def createDirs(years):
    for y in years:
        os.chdir(cwd)
        os.mkdir(y.getText())
        os.chdir(y.getText())
        langs = getLangsAvailable(y['href'])
        for l in langs:
            os.chdir(cwd)
            os.chdir(y.getText())
            os.mkdir(l.getText())

soup = getSoup(base_url)
years = getYearsAvailable(soup)
createDirs(years)

for y in years:
    os.chdir(y.getText())
    langs = getLangsAvailable(y['href'])
    for l in langs:
        os.chdir(cwd)
        os.chdir(y.getText())
        os.chdir(l.getText())
        scrapePages(l['href'])