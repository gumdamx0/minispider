import os
import time
import threading

from spider.utils.common import get_headers, save_htm, save_errlog


class Consumer(threading.Thread):
    # 下载网页内容
    def __init__(self, page_queue, img_queue, args):
        super(Consumer, self).__init__()
        self._page_queue = page_queue
        self._img_queue = img_queue
        self._args = args

    def run(self):
        headers = get_headers()
        csv_file = 'summary.csv'

        while True:
            if self._img_queue.empty() and self._page_queue.empty():
                break

            try:
                filea = open(os.path.join(self._args.result, csv_file), mode='a', encoding='utf-8')
                img_url, file_name = self._img_queue.get()
                print(img_url, '\tis proceeding')
                filea.write(img_url + ',')
                filea.write(str(save_htm(img_url, headers, self._args)) + ',')
                filea.write(str(time.strftime("%Y-%m-%d %H:%M:%S")))
                filea.write('\n')
                print(img_url, '\tfile saved successfully!')
                time.sleep(self._args.crawl_interval)

            except Exception as e:
                save_errlog(e, self._args)
