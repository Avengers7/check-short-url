import json
import re

import iocextract
from tldextract import tldextract
from utils import loads_file


def extract_all_url(content_raw):
    """
    提取文本中全部的URL
    :param content_raw: 传入进行提取全部URL的文本
    :return: 文本中全部URL的列表
    """
    # 经过iocextract提取后的URL列表
    url_list_after_ioc = iocextract.extract_urls(content_raw)
    # 经过正则表达式提取后的URL列表
    url_list_after_regexp = extract_url_by_regexp(content_raw)

    url_list_final = []

    # TODO 需要进一步降低误报

    return url_list_final


def extract_url_by_regexp(content_raw):
    """
    根据正则表达式匹配文本中的URL
    :param content_raw: 传入进行提取全部URL的文本
    :return: 文本中全部URL的列表
    """
    url_list = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', content_raw)
    return url_list


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

    # """
    # 测试：提取文本中全部URL的TLD
    # """
    # tld_list = extract_tld(content_raw)
    # print(tld_list)
    #
    #
    # """
    # 测试：提取文本中的全部URL
    # """
    # print(extract_all_url(content_raw))


    """
    测试：从文本中根据正则表达式
    """
    url_list = extract_url_by_regexp(content_raw=content_raw)
    print(url_list)

