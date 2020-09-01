"""
本模块用于本地（离线）识别URL是否属于短链
（初版）主要有以下四个判断因素：
- 检查URL是否来自短链服务，通过对比TLD
- 检查URL的后缀是否为常见的短链后缀
- 检查URL信息的长度进行判别
- 检查URL的TLD是否在域名白名单中

"""
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 引入根目录，让程序在执行的单个文件时能找到根目录
sys.path.append(rootPath)

import tldextract.tldextract

from extract_url.extract_short_url import extract_tld
from utils import loads_file
from utils.loads_file import loads_file_from_txt_to_list


def identify_short_url_by_service(url_to_tld_dict):
    """
    检查URL是否来自短链服务，通过对比TLD
    :param url_to_tld_dict: 从文本内容中提取的URL:TLD字典
    :return: 经过短链服务检查后的URL:TLD字典
    """

    # 属于短链的URL:它的TLD的字典
    short_url_to_tld_dict = {}
    short_url_service_domain_list = loads_file_from_txt_to_list(fpath="../data/short_url_services_list.txt")
    for url in url_to_tld_dict.keys():
        for service_domain in short_url_service_domain_list:
            # 传入URL的TLD
            tld = url_to_tld_dict[url]
            if tld == service_domain:
                short_url_to_tld_dict[url] = tld
    return short_url_to_tld_dict


def identify_short_url_by_suffix(url_to_tld_dict):
    """
    检查URL的后缀是否为常见的短链后缀
    :param url_to_tld_dict: 从文本内容中提取的URL:TLD字典
    :return: 经过后缀检查后的URL:TLD字典
    """
    # 可能属于短链的URL:TLD的字典
    short_url_to_tld_dict = {}
    short_url_service_domain_list = loads_file_from_txt_to_list(fpath="../data/short_url_services_list.txt")
    # 常见短链服务提供商的域名后缀集合
    suffix_set = set()
    for url in short_url_service_domain_list:
        suffix = tldextract.extract(url)[2]
        suffix_set.add(suffix)
    # 通用域名，不列为可疑的短链域名后缀
    common_suffix_list = ['com', 'net', 'info', 'org', '']
    for common_suffix in common_suffix_list:
        suffix_set.remove(common_suffix)

    # print("短链服务提供商的常见域名后缀的集合：{0}".format(suffix_set))

    for url in url_to_tld_dict.keys():
        input_url_suffix = tldextract.extract(url_to_tld_dict[url])[2]
        # 传入URL的TLD
        tld = url_to_tld_dict[url]
        for suffix in suffix_set:
            if input_url_suffix == suffix:
                short_url_to_tld_dict[url] = tld
    return short_url_to_tld_dict


def identify_short_url_by_length(url_to_tld_dict):
    """
    检查URL信长度是否符合短链的长度特征
    :param url_to_tld_dict: 从文本内容中提取的URL:TLD字典
    :return: 经过URL长度检查后的URL:TLD字典
    """
    # 可能属于短链的URL:TLD的字典
    short_url_to_tld_dict = {}

    # 关于 URL:URL长度 的字典
    url_length_dict = {}
    # 关于 URL:TLD长度 的字典
    tld_length_dict = {}
    for url in url_to_tld_dict.keys():
        tld = url_to_tld_dict[url]
        if len(tld) > 10:
            tld_length_dict[url] = False
        else:
            tld_length_dict[url] = True

    for url in url_to_tld_dict.keys():
        if len(url) >= 35:
            url_length_dict[url] = False
        else:
            url_length_dict[url] = True

    for url in url_to_tld_dict.keys():
        if url_length_dict[url] and tld_length_dict[url]:
            short_url_to_tld_dict[url] = url_to_tld_dict[url]

    return short_url_to_tld_dict


def identify_short_url_by_white_domain_list(url_to_tld_dict):
    """
    检查URL的TLD是否在域名白名单中
    :param url_list: 从文本内容中提取的URL:TLD字典
    :return: 经过TLD白名单检查后的URL:TLD字典
    """
    # 可能属于短链的URL:TLD的字典
    short_url_to_tld_dict = {}

    top_domain_list = loads_file.loads_file_from_txt_to_list(fpath="../data/top_domain_cn.txt")
    for url in url_to_tld_dict.keys():
        tld = url_to_tld_dict[url]
        for top_domain in top_domain_list:
            if not(tld == top_domain):
                short_url_to_tld_dict[url] = tld

    return short_url_to_tld_dict


def local_identify_short_url(content_raw):
    """
    本地（离线）识别URL是否属于短链
    :param content_raw: 需要检验的字符串文本内容
    :return: 属于短链的原始URL:TLD的字典，示例数据：{'https://zeek.ir/huhsdfods': 'zeek.ir'}
    """

    # 从文本内容中提取的URL:TLD字典
    url_to_tld_dict = extract_tld(content_raw=content_raw)

    # 初始化属于短链的URL:TLD的字典
    short_url_to_tld_dict = {}


    # 经过短链服务检查后的URL:TLD字典
    url_to_tld_dict_after_service = identify_short_url_by_service(url_to_tld_dict=url_to_tld_dict)
    # 更新总共的短链的URL:TLD字典
    short_url_to_tld_dict.update(url_to_tld_dict_after_service)

    # 经过常见的短链后缀检查后的URL:TLD字典
    url_to_tld_dict_after_suffix_check = identify_short_url_by_suffix(url_to_tld_dict=url_to_tld_dict)
    # 更新总共的短链的URL:TLD字典
    short_url_to_tld_dict.update(url_to_tld_dict_after_suffix_check)

    # 经过URL长度是否符合短链长度特征后的URL:TLD字典
    url_to_tld_after_length_check = identify_short_url_by_length(url_to_tld_dict=url_to_tld_dict)
    # 更新总共的短链的URL:TLD字典
    short_url_to_tld_dict.update(url_to_tld_after_length_check)

    # 经过检查URL的TLD是否在域名白名单中
    url_to_tld_after_domain_white_list_check = identify_short_url_by_white_domain_list(url_to_tld_dict)
    # 更新总共的短链的URL:TLD字典
    short_url_to_tld_dict.update(url_to_tld_after_domain_white_list_check)

    # 将可信度较低的筛选结果求交集
    part_one_short_url_list = list(url_to_tld_dict_after_suffix_check.keys() &
                                   url_to_tld_after_domain_white_list_check.keys())
    # 将可行度较高的筛选结果求交集
    part_two_short_url_list = list(url_to_tld_dict_after_service.keys() & url_to_tld_after_length_check.keys())

    # 将可信度较低结果的交集与高可信结果做并集，得到最终确定的短链URL列表
    # final_short_url_list = part_one_short_url_list + part_two_short_url_list

    final_short_url_list = list(url_to_tld_dict_after_suffix_check.keys() & url_to_tld_after_domain_white_list_check.keys()\
                           & url_to_tld_dict_after_service.keys() & url_to_tld_after_length_check.keys())

    # 将最终确定的短链URL转化为集合（set），去重
    final_short_url_set = set(final_short_url_list)

    return final_short_url_set