from spider.utils.common import get_version, get_headers, save_htm, save_errlog
from spider.__main__ import parser_args

if __name__ == '__main__':
    # 测试
    opt = parser_args()

    print(get_version())

    print(get_headers())

    save_htm(url='https://crawler-test.com/content/title_with_newline_quote_doublequote_and_comma_characters',
             headers=get_headers(), args=opt)

    try:
        save_htm(url='https://', headers=get_headers(), args=opt)
    except Exception as e:
        save_errlog(e, opt)
