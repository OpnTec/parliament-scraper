#!/usr/bin/env python
"""
    Requirements:
    - requests (installation: pip install requests)
    - lxml (installation: pip install lxml)
"""

import requests
import lxml.html
import os

def download_file(file_name, url):
    #file_name = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return file_name


for i in range(1, 1381):
    url = "http://www.europarl.europa.eu/RegistreWeb/search/typedoc.htm?codeTypeDocu=QECR&year=2015&currentPage={0}".format(i)
    html = lxml.html.parse(url)
    titles = [i.strip() for i in html.xpath("//div[contains(@class, 'notice')]/p[@class='title']/a/text()")]
    docs = [i.strip() for i in html.xpath("//div[contains(@class, 'notice')]/ul/li/a/@href")]
    q_refs = [i.strip() for i in html.xpath("//div[contains(@class, 'notice')]/div[@class='date_reference']/span[2]/text()")]
    for title, doc, q_ref in zip(titles, docs, q_refs):
        file_name = os.path.join(os.getcwd(),'data','-'.join(title.split('/'))+' '+q_ref+'.'+doc.split('.')[-1])
        downloaded_file = download_file(file_name, doc)
        print downloaded_file