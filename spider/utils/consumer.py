import os
import time
import threading

from spider.utils.common import csv_file, get_headers, save_htm, save_errlog


class Consumer(threading.Thread):
    """
    Attributes:
    page_queue (:class:`Queue`) : the queue of pages to be process
    img_queue (:class:`Queue`): the queue of pages to be save
    args (:class:`argparse.Namespace`) : parameters in configuration file
    """

    def __init__(self, page_queue, img_queue, args):
        super(Consumer, self).__init__()
        self._page_queue = page_queue
        self._img_queue = img_queue
        self._args = args

    def run(self):
        headers = get_headers()

        while True:
            if self._img_queue.empty() and self._page_queue.empty():
                break

            try:
                img_url, file_name = self._img_queue.get()
                print(img_url, '\tis proceeding')
                with open(os.path.join(self._args.result, csv_file), mode='a', encoding='utf-8') as f:
                    f.write(img_url + ',')
                    f.write(str(save_htm(img_url, headers, self._args)) + ',')
                    f.write(str(time.strftime("%Y-%m-%d %H:%M:%S")))
                    f.write('\n')
                print(img_url, '\tfile saved successfully!')
                time.sleep(self._args.crawl_interval)

            except Exception as e:
                save_errlog(e, self._args)
