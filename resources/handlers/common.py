import re
import os
import time
import json
from urllib.request import urlopen, Request, urlretrieve
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup as soup
import logging


class Common:

    def __init__(self, link, name, direct):
        self.logger = logging.getLogger(__name__)
        self.link = link
        self.name = name
        self.direct = direct
        self.load_config()

        self.save()

    def load_config(self):
        with open('resources/config.json') as json_data_file:
            data = json.load(json_data_file)
        try:
            int(data["media_download"]["retries"])
            int(data["media_download"]["wait_time"])

            self.retries = data["media_download"]["retries"]
            self.wait_time = data["media_download"]["wait_time"]

        except:
            self.logger.error(
                "TypeError: Media download retries or wait time is not an integer.")
            self.retries = 5
            self.wait_time = 60

    def save(self):
        if 'gifv' in self.link:
            ext = '.mp4'
            self.link = self.link.replace('gifv', 'mp4')
        elif 'i.reddituploads.com' in self.link:
            ext = '.jpeg'
        else:
            ext = '.' + \
                re.search('jpg$|png$|gif$|jpeg$|mp4$', self.link).group()
        self.direct = os.path.join(
            self.direct, self.format_name(self.name) + ext)

        self.logger.debug("Saving {} with extension {}".format(self.link, ext))

        self.save_image()

    def save_image(self, current_retry=1):
        try:
            urlretrieve(self.link, self.direct)
        except URLError:
            if self.retries > current_retry:
                self.logger.warning("Retrying {}".format(self.link))
                time.sleep(5)
                current_retry += 1
                self.save_image(current_retry)
            else:
                self.logger.error("Failed {}".format(self.link))
                with open(os.path.join(os.getcwd(), 'error.txt'), 'a+') as logFile:
                    logFile.write('URLError: {}\n'.format(self.link))

    def get_html(self):
        req = Request(
            self.link,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        try:
            page_html = urlopen(req).read()
            page_html = soup(page_html, "lxml")
        except HTTPError:
            page_html = None
        return page_html

    def format_name(self, title):
        title = re.sub('[?/|\\\:<>*"]', '', title)
        if len(title) > 190:
            title = title[:120]
        return title
