import os
import time
import random
import logging
import requests
import configparser

proxy_list = [
    "120.196.112.6:3128",
    "124.205.155.153:9090",
]

headers_list = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

proxies = {
    'http': None,
    'https': None,
}

csv_file = 'summary.csv'
cnt_file = 'data'


def get_version():
    '''
    code revise version
    :return: str
    '''
    return '0.1.0'


def read_conf(config, args):
    '''
    change parameters according to conf with a json form
    :param config:config parser
    :param args:argument parser
    :return:None
    '''

    cfg = configparser.ConfigParser()

    cfg.read(config)

    args.seed = cfg.get('spider', 'seed')
    args.result = cfg.get('spider', 'result')
    args.max_depth = eval(cfg.get('spider', 'max_depth'))
    args.crawl_interval = eval(cfg.get('spider', 'crawl_interval'))
    args.crawl_timeout = eval(cfg.get('spider', 'crawl_timeout'))
    args.thread_count = eval(cfg.get('spider', 'thread_count'))


def get_headers():
    '''
    chooce random headers
    :return: dict, headers
    '''
    headers = random.choice(headers_list)
    headers = {"user-agent": "{}".format(headers)}

    return headers


def save_htm(url, headers, args):
    '''
    save each web page
    :param url: url of the web page
    :param headers: request headers
    :param args: parameter to point out the path to save
    :return: int, size of the saved file
    '''
    subresp = requests.get(url, headers=headers, timeout=args.crawl_timeout, allow_redirects=False)
    filename = url.strip('/').split('/')[-1]
    if '?' in filename:
        filename = filename.replace('?', ' ')
    svpath = os.path.join(args.result, 'data', filename)
    with open(svpath, mode='wb') as f:
        f.write(subresp.content)
    subresp.close()

    return os.path.getsize(svpath)


def save_errlog(e, args):
    '''
    save each failed crawling
    :param e: standard err info
    :return: None
    '''
    now = str(time.strftime("%Y-%m-%d %H-%M-%S"))
    today = now.split(' ')[0]
    logName = now + "_err.log"
    if not os.path.exists("{}/log/".format(args.result)):
        os.makedirs("{}/log/".format(args.result))
    if not os.path.exists("{}/log/{}/".format(args.result, today)):
        os.makedirs("{}/log/{}/".format(args.result, today))
    if not os.path.exists("{}/log/{}/{}".format(args.result, today, logName)):
        reportFile = open("{}/log/{}/{}".format(args.result, today, logName), 'w')
        reportFile.close()
    logger = logging.getLogger()
    handler = logging.FileHandler("{}/log/{}/{}".format(args.result, today, logName), encoding='utf8')
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(levelname)s %(message)s')

    handler.setFormatter(formatter)
    console.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(console)
    logger.setLevel(logging.INFO)
    logging.info(e)
