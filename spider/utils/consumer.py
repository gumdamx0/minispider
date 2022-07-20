import os
import time
import threading

from spider.utils.common import get_headers, save_htm, save_errlog


class Consumer(threading.Thread):

    # 下载网页内容

    def __init__(self, page_queue, img_queue, args):
        super(Consumer, self).__init__()
        self.page_queue = page_queue
        self.img_queue = img_queue
        self.args = args

    def run(self):
        headers = get_headers()
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break

            try:
                filea = open(os.path.join(self.args.result, 'summary.csv'), mode='a', encoding='utf-8')
                # cswriter = csv.writer(filea, delimiter=',')
                img_url, file_name = self.img_queue.get()
                print(img_url, '\tis proceeding')
                filea.write(img_url + ',')
                filea.write(str(save_htm(img_url, headers, self.args)) + ',')
                filea.write(str(time.strftime("%Y-%m-%d %H:%M:%S")))
                filea.write('\n')
                # cswriter.writerow([img_url, str(time.strftime("%Y-%m-%d %H:%M:%S")), str(save_htm(img_url, headers, opt))])
                print(img_url, '\tfile saved successfully!')
                time.sleep(self.args.crawl_interval)

            except Exception as e:
                save_errlog(e, self.args)