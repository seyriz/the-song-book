# -*- coding: utf-8 -*-
from json import dumps
from time import sleep
from urllib2 import urlopen

from google.appengine.ext import db
from bs4 import BeautifulSoup

from models import Musics

class TJCrawler(object):
    page = 1
    search_url = "http://www.tjmedia.co.kr/tjsong/song_search_list.asp?strType=1&strText=%EF%BF%BD&searchOrderType=up&searchOrderItem=pro&strCond=0&strSize01=100&intPage="
    has_next = True

    def __init__(self):
        while self.has_next:
            url = self.search_url + str(self.page)
            print(url)
            self.get_page(url)

    def get_page(self, url):
        print("PAGE {}".format(self.page))
        resp = urlopen(url)
        html = resp.read()
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.findAll("table", {'class': 'board_type1'})
        trs = table[0].find_all("tr")
        crawled_list = list()
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) != 0:
                song = {
                    "song_num": tds[0].get_text(),
                    "title": tds[1].get_text(),
                    "singer": tds[2].get_text(),
                    "lyrics": tds[3].get_text(),
                    "composer": tds[4].get_text(),
                }
                crawled_list.append(song)
        pages = soup.findAll("a", {'class': 'page1'})

        self.page += 1

        page_str = ""
        for page in pages:
            page_str += page.get_text() + "|"
        self.has_next = page_str.count(str(self.page+1)) > 0
        if not self.has_next:
            self.has_next = len(soup.findAll("img", {"src": "/images/common/page_next.gif"})) > 0
        print("DONE, HAS_NEXT: {}".format(self.has_next))
        ## POST TO DB
        with open("tj.json", mode="a") as f:
            for j in crawled_list:
                f.write(dumps(j) + "\n")
        sleep(5)


class KYCrawler(object):
    page = 1
    cat = xrange(1, 41)
    search_url = "http://www.ikaraoke.kr/isong/search_index.asp?&SelType=2&s_value=%A4%A1&keyIdx={}&page={}"
    has_next = True

    def __init__(self):
        # for i in range(1, 42):
        #     while self.has_next:
        i = 1
        url = self.search_url.format(i, self.page)
        print(url)
        self.get_page(url)

    def get_page(self, url):
        print("PAGE {}".format(self.page))
        resp = urlopen(url)
        html = unicode(resp.read(), 'euc-kr').encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.findAll("div", {'class': 'tbl_board'})[0].find_all('table')
        trs = table[0].find_all("tr")
        crawled_list = list()
        if len(trs) == 1:
            self.has_next = False
            print("DONE, HAS_NEXT: {}".format(self.has_next))
            return
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) != 0:
                compose_lyric = tds[4].get_text().split('작곡')
                lyrics = compose_lyric[1].replace('작사', '').strip() if len(compose_lyric) > 2 \
                    else compose_lyric[0].strip()
                song = {
                    "song_num": tds[1].get_text().strip(),
                    "title": tds[2].get_text().strip(),
                    "singer": tds[3].get_text().strip(),
                    "lyrics": lyrics,
                    "composer": compose_lyric[0].strip(),
                }
                print(song)
                crawled_list.append(song)
        pages = soup.findAll("div", {'class': 'paging'})

        self.page += 1

        print("DONE, HAS_NEXT: {}".format(self.has_next))
        ## POST TO DB
        with open("ky.json", mode="a") as f:
            for j in crawled_list:
                f.write(dumps(j) + "\n")
        sleep(5)
