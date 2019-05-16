# Author: Zhongyang Zhang
# E-mail: mirakuruyoo@gmail.com

import urllib
from urllib import request
from bs4 import BeautifulSoup
import os
import requests
import argparse
import re
import time
import math
import codecs
import threading
import urllib.parse as up

class imgThread (threading.Thread):
    def __init__(self, threadID, urls, outpath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "Thread-"+str(threadID)
        self.counter = threadID
        self.urls = urls
        self.outpath = outpath

    def run(self):
        log("Starting " + self.name)
        KonaPicCrawl(self.urls, self.outpath)
        log("Exiting " + self.name)

def log(*args, end=None):
    if end is None:
        print(time.strftime("==> [%Y-%m-%d %H:%M:%S]",
                            time.localtime()) + " " + "".join([str(s) for s in args]))
    else:
        print(time.strftime("==> [%Y-%m-%d %H:%M:%S]", time.localtime()) + " " + "".join([str(s) for s in args]),
              end=end)

def KonaPicCrawl(urls, outpath):
    for url in urls:
        img_name = up.unquote(url).split('/')[-1].replace(' ', '-')[15:]
        img_path = os.path.join(outpath, 'pic', img_name)
        try:
            img = requests.get(url)
            with open(img_path, 'wb') as f:
                f.write(img.content)
                f.flush()
            log("Successfully crawled img:{}".format(img_name[:60]))
        except:
            log("Failed crawling img:{}".format(url))

def KonaTagCrawlMain(url, outpath):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    if not os.path.exists(os.path.join(outpath, 'pic')):
        os.mkdir(os.path.join(outpath, 'pic'))
    html = str(request.urlopen(url).read(), 'utf-8')
    soup = BeautifulSoup(html, 'lxml')
    try:
        pagesum = int(soup.body.select(
            '#content #post-list .content #paginator .pagination a')[-2].get_text())
    except IndexError:
        pagesum = 1

    log('Start crawling image links...')
    links = []
    for pagenum in range(1, pagesum+1):
        _url = url + '&page=' + str(pagenum)
        html = str(request.urlopen(_url).read(), 'utf-8')
        soup = BeautifulSoup(html, 'lxml')
        links.extend([i.attrs['href'] for i in soup.body.select(
            '#content > #post-list > .content > div > #post-list-posts > li > a')])
    log('Finished crawling image links.')

    with codecs.open(os.path.join(outpath, 'url_list.txt'), 'w+') as f:
        for link in links:
            f.write(link+'\n')

    def chunks(arr, m):
        n = int(math.floor(len(arr) / float(m)))
        return [*[arr[i:i + n] for i in range(0, (m-1)*n, n)],arr[(m-1)*n:]]

    threads = []
    links_sep = chunks(links, opt.thread_num)

    for i in range(opt.thread_num):
        threads.append(imgThread(i, links_sep[i], outpath))

    for i in threads:
        i.start()

    for i in threads:
        i.join()
    log('Successfully crawled all of the images. Thanks for using.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', default='shingeki_no_kyojin', help='The name of tag you want to crawl.')
    parser.add_argument('--thread_num', type=int, default=5, help='The number of threads you want to use when crawling.')
    opt = parser.parse_args()
KonaTagCrawlMain('https://konachan.net/post?tags='+opt.key, opt.key)
