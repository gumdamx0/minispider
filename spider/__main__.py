import os
import json
import argparse
from queue import Queue

from spider.utils.common import csv_file, cnt_file, get_version, read_conf
from spider.utils.producer import Producer
from spider.utils.consumer import Consumer


def parser_args():
    parser = argparse.ArgumentParser(prog='minispider', description='from good coder project')

    parser.add_argument('--seed', type=str, default='./urls', help='Path to seed file')
    parser.add_argument('--result', type=str, default='./result', help='Path for saving results')
    parser.add_argument('--max_depth', type=int, default=1, help='Max crawling depth')
    parser.add_argument('--crawl_interval', type=int, default=1, help='Interval for each crawling')
    parser.add_argument('--crawl_timeout', type=int, default=1, help='Timeout parameter during crawling')
    parser.add_argument('--thread_count', type=int, default=1, help='max number of crawling threads')
    parser.add_argument('-v', '--version', action='version', version=get_version(), help='Display version')
    parser.add_argument('-c', '--conf_path', type=str, default='./spider.json', help='Load configuration file')
    opt = parser.parse_args()
    opt_dict = vars(opt)

    conf_type = opt.conf_path.split('.')[-1]
    if conf_type == 'json':
        with open(opt.conf_path, 'rt') as f:
            opt_dict.update(json.load(f))
    else:
        read_conf(opt.conf_path, opt)

    print(opt)

    if not os.path.exists(opt.result):
        os.mkdir(opt.result)

    if not os.path.exists(os.path.join(opt.result, cnt_file)):
        os.mkdir(os.path.join(opt.result, cnt_file))

    return opt


def main(args):
    page_queue = Queue(100)
    img_queue = Queue(1000)

    if os.path.exists(os.path.join(args.result, csv_file)):
        os.remove(os.path.join(args.result, csv_file))

    with open(args.seed, 'r') as source_file:
        urls = source_file.readlines()
    for url in urls:
        page_queue.put(url)

    for x in range(args.thread_count):
        t = Producer(page_queue=page_queue, img_queue=img_queue, args=args)
        t.start()

    img_queue.get()

    for x in range(args.thread_count):
        t = Consumer(page_queue=page_queue, img_queue=img_queue, args=args)
        t.start()


if __name__ == '__main__':
    main(parser_args())
