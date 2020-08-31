import json

import iocextract
from tldextract import tldextract
from utils import loads_file


def extract_all_url(content_raw):
    """
    提取文本中全部的URL
    :param content_raw: 传入进行提取全部URL的文本
    :return: 文本中全部URL的列表
    """
    url_list_after_ioc = iocextract.extract_urls(content_raw)
    url_list_final = []

    # TODO 需要进一步降低误报

    return url_list_after_ioc


def extract_tld(content_raw):
    """
    提取文本中全部URL的TLD
    :param content_raw: 传入进行提取TLD的文本
    :return: 文本中所包含链接的全部TLD列表
    """
    url_list = extract_all_url(content_raw)
    tld_list = []
    for url in url_list:
        if url:
            tld_array = tldextract.extract(url)
            tld_element = tld_array[1] + "." + tld_array[2]
            tld_list.append(tld_element)
        else:
            continue

    return tld_list


if __name__ == '__main__':
    file_path = "../data/content_for_test.json"
    content_raw = loads_file.loads_file_to_content_raw(fpath=file_path)

    """
    测试：提取文本中全部URL的TLD
    """
    tld_list = extract_tld(content_raw)
    print(tld_list)
