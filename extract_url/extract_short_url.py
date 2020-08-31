import json
import re
import string

import iocextract
from tldextract import tldextract
from utils import loads_file


def extract_all_url_test(content_raw):
    """
    提取文本中全部的URL
    :param content_raw: 传入进行提取全部URL的文本
    :return: 文本中全部URL的列表
    """

    # 经过iocextract提取后的URL列表
    url_list_after_ioc = iocextract.extract_urls(content_raw)
    """
    iocextract提取测试
    """
    url_number_after_ioc = len(list(url_list_after_ioc))
    url_list_after_ioc_test = []
    for url in url_list_after_ioc:
        url_list_after_ioc_test.append(url)
    # print("经过ioc提取后的URL列表：{0}".format(url_list_after_ioc_test))
    # print("经过ioc提取后的URL列表：{0}".format(list(url_list_after_ioc)))
    print("经过ioc提取后的URL链接数量为：{0}".format(url_number_after_ioc))

    # 经过正则表达式提取后的URL列表
    url_list_after_regexp = extract_url_by_regexp(content_raw)
    """
    正则表达式提取测试
    """
    url_number_after_regexp = len(url_list_after_regexp)
    url_list_after_regexp_show = []
    for url in url_list_after_regexp:
        url_list_after_regexp_show.append(url)
    print("经过正则表达式提取后的URL列表：{0}：".format(url_list_after_regexp_show))
    print("经过正则表达式提取后的URL链接数量为：{0}".format(url_number_after_regexp))

    url_list_final = []

    # TODO 需要进一步降低误报

    return url_list_after_ioc


def extract_all_url(content_raw):
    """
    提取文本中全部的URL
    :param content_raw: 传入进行提取全部URL的文本
    :return: 文本中全部URL的列表
    """

    # 经过iocextract提取后的URL列表
    url_list_after_ioc = iocextract.extract_urls(content_raw)

    # 初始化list
    iocex_url = []
    list_dot = []
    list_more_dot = []
    list_sub_symbol = []
    list_last = []
    url_list_final = []

    for url in url_list_after_ioc:
        iocex_url.append(url)

    # 检测URL中点号是否>=3个
    for url in iocex_url:
        count = url.count('.')
        if count < 3:
            list_dot.append(url)
        else:
            list_more_dot.append(url)
    print('符合条件的url：', list_dot)
    print('不符合条件的url: ', list_more_dot)

    # 去除特殊字符
    for url in list_more_dot:
        url = re.sub('[’!"\'()*+,;-<=>?，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", url)
        url = re.sub(r'(\\n)', "", url)
        list_sub_symbol.append(url)
    print('去除特殊字符后: ', list_sub_symbol)

    # 类型转换
    list_sub_symbol = "\n".join(list_sub_symbol)

    # 再次提取
    list_final = iocextract.extract_urls(list_sub_symbol)
    for url in list_final:
        list_last.append(url)
    print('再次iocextract提取：', list_last)

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
    :return: 文本中所包含链接:TLD的字典，示例数据：{'https://zeek.ir/': 'zeek.ir'}
    """
    url_list = extract_all_url(content_raw)
    tld_list = []
    short_url_dict = {}
    for url in url_list:
        if url:
            tld_array = tldextract.extract(url)
            tld_element = tld_array[1] + "." + tld_array[2]
            tld_list.append(tld_element)
            short_url_dict[url] = tld_element
        else:
            continue

    return short_url_dict


if __name__ == '__main__':
    file_path = "../data/content_for_test.json"
    content_raw = loads_file.loads_file_to_content_raw(fpath=file_path)

    # """
    # 测试：提取文本中全部URL的TLD
    # """
    # tld_list = extract_tld(content_raw)
    # print(tld_list)


    """
    测试：提取文本中的全部URL
    """
    extract_all_url(content_raw)


    # """
    # 测试：从文本中根据正则表达式
    # """
    # url_list = extract_url_by_regexp(content_raw=content_raw)
    # print(url_list)
