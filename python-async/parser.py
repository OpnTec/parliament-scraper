from itertools import count
from queue import Queue
import threading
import math
import os
import re

from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup as BS
from requests.exceptions import ConnectionError
from tqdm import tqdm
import requests

from datetime import datetime
startTime = datetime.now()

# page to start scraping with
SEARCH_LANDING = 'http://www.europarl.europa.eu/RegistreWeb/search/typedoc.htm?codeTypeDocu=QECR'

YEARS_TO_PARSE = [2015]

FOLDER_TO_DOWNLOAD = 'questions-data'


class DownloadThread(threading.Thread):
    def __init__(self, queue, destfolder):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True

    def run(self):
        while True:
            url, title = self.queue.get()
            try:
                self.download_url(url, title)
            except Exception as e:
                print("   Error: {}".format(e))
            self.queue.task_done()

    def download_url(self, url, title):
        download_dest = '{folder}/{file_name}'.format(
            folder=self.destfolder, file_name=title)
        with open(download_dest, 'wb') as question:
            q = requests.get(url, stream=True)
            for block in q.iter_content(512):
                if not block:
                    break
                question.write(block)
        print('\t{} ---> {}\n'.format(url, download_dest))


def download(urls, destfolder, numthreads=10):
    queue = Queue()
    for url, title in urls.items():
        queue.put((url, title))

    for i in range(numthreads):
        t = DownloadThread(queue, destfolder)
        t.start()

    queue.join()


def main():
    urls = {}
    requests = []
    session = FuturesSession(max_workers=10)
    for year in YEARS_TO_PARSE:
        landing_page = SEARCH_LANDING + '&year=' + str(year)
        landing_res = session.get(landing_page).result()
        landing_bs = BS(landing_res.content, 'html5lib')
        number_span = landing_bs.select('li.ep_tag_selected span')[0].text
        number_of_question = int(re.findall(r'\d+', number_span)[0])
        number_of_pages = math.ceil(
            number_of_question / 10)  # change to per page
        for page_num in range(1, number_of_pages + 1):
            res = session.get(landing_page + '&currentPage=' + str(page_num))
            requests.append(res)
        for request in tqdm(requests):
            try:
                request_result = request.result()
            except ConnectionError:
                print(
                    'Due to the ConnectionError page {} hasn\'t been parsed'.format(page_num))
                continue
            page = BS(request_result.content, "html5lib")
            if page:
                for notice in page.select('.results div.notice'):
                    for url in notice.select('ul.documents li a'):
                        title_text = notice.select(
                            'p.title a.result_details_link')[0].text
                        title_date = notice.select(
                            'div.date_reference span.date')[0].text
                        question_format = url.get('href').split('.')[-1]
                        title = '{} ({}).{}'.format(
                            title_text, title_date, question_format)
                        title = re.sub(r'[\n\r\t]', '', title)
                        title = title.replace('/', '-')
                        urls[url.get('href')] = title
            else:
                break
    if not os.path.exists(FOLDER_TO_DOWNLOAD):
        os.mkdir(FOLDER_TO_DOWNLOAD)
    download(urls, FOLDER_TO_DOWNLOAD)

if __name__ == '__main__':
    main()
    print(datetime.now() - startTime)
