import chardet
import requests
import threading
from lxml import etree

from spider.utils.common import get_headers


class Producer(threading.Thread):
    # 获取地址
    def __init__(self, page_queue, img_queue, args):
        super(Producer, self).__init__()
        self._page_queue = page_queue
        self._img_queue = img_queue
        self._args = args

    def run(self):
        while True:
            if self._page_queue.empty():
                break
            url = self._page_queue.get()
            self.parser_page(url)

    def parser_page(self, url):

        headers = get_headers()
        resp = requests.get(url=url, headers=headers, timeout=self._args.crawl_timeout, allow_redirects=False)
        resp.encoding = chardet.detect(resp.content)['encoding']
        cont = resp.text
        resp.close()
        html = etree.HTML(cont)
        table = html.xpath('/html/body/div[2]/div')

        for page in table:
            hrefs = page.xpath('div/div/div/a/@href')

        for href in hrefs:
            file_name = href
            if href[0] == '/':
                href = url + href
            self._img_queue.put((href, file_name))
