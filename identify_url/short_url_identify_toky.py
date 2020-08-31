"""
本模块用于提取URL中的相关信息
"""
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 引入根目录，让程序在执行的单个文件时能找到根目录
sys.path.append(rootPath)

from urllib.parse import urlparse
import iocextract
import tldextract.tldextract
import urllib.request

from extract_url.extract_short_url import extract_tld
from utils import loads_file
from utils.loads_file import loads_file_from_txt_to_list


def extract_port(url):
    """
    提取URL中端口
    :param url: 需要解析的URL
    :return: URL中包含的端口号（int型）
    """
    url_after_parse = urlparse(url)
    hostname = url_after_parse.hostname
    port = url_after_parse.port

    return port


def extract_short_link(content_raw):
    """
    从文本中提取全部的短链接
    :param content_raw: 需要传入进行检查的文本
    :return: 文本中所包含的短链接列表
    """
    url_list = iocextract.extract_urls(content_raw)
    short_link_list = []
    for url in url_list:
        if url:
            tld = tldextract.extract(url)
            domain_1 = tld[1] + "." + tld[2]

            if len(domain_1) <= 7:
                short_link_list.append(url)
        else:
            continue

    return short_link_list


# def identify_short_link_from_url(url):
#     """
#     判断该URL是否为短链，根据的逻辑为：
#     TODO 待完善
#     - 检查TLD
#         - TLD是否存在于真实访问的链接中
#         - TLD长度是否较短
#     - 检查URL请求响应码
#         - 响应码是否为302
#     :param url: 需要检验的URL
#     :return: 判断为短链返回True，不是短链返回False
#     """
#     # 增加请求头信息，减少出现403错误
#     request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
#     response = urllib.request.urlopen(request)
#     # 获取真实访问的链接
#     final_url = response.geturl()
#
#     # 提取传入检验URL的TLD
#     url_tld = tldextract.extract(url)[1] + '.' + tldextract.extract(url)[2]
#     # URL请求响应码
#     response_code = response.getcode()
#
#     # 初始化短链接列表
#     short_link_list = []
#
#     # 如果传入检验URL的TLD存在真实访问的链接中，则认为其不属于短链
#     if url_tld not in final_url:
#         # 认为URL的TLD长度大于9则可能不属于短链接，进行下一步判断
#         if len(url_tld) <= 9:
#             short_link_list.append(url)
#             return True
#         # 在URL的TLD长度大于9的情况下，且其TLD不在真实访问链接中，则根据响应码判断其是否属于短链
#         elif response_code == 302:
#             short_link_list.append(url)
#             return True
#     else:
#         if len(url_tld) <= 9:
#             short_link_list.append(url)
#             return True
#     return False


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

    return short_url_to_tld_dict


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
    :return:
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


if __name__ == '__main__':
    # example_url = "http://34.64.205.36:9421/"
    # port = extract_port(url=example_url)
    # print(type(port))

    # 测试用邮件数据的路径
    file_path = "../data/content_for_test.json"
    # 对象化邮件文本数据
    content_obj = loads_file.loads_file_to_object(fpath=file_path)
    # 字符串形式的邮件文本数据
    content_raw = loads_file.loads_file_to_content_raw(fpath=file_path)
    # 从文本内容中提取的URL:TLD字典
    url_to_tld_dict = extract_tld(content_raw=content_raw)

    # """
    # 测试：从文本中提取全部的短链接
    # """
    # short_link_list = extract_short_link(content_raw=content_raw)
    # print(short_link_list)
    #
    # """
    # 测试：判断短链接
    # """
    # example_short_url = "http://suo.im/5TwT29"
    # # example_short_url = "http://tinyurl.com/y2eo5an2"
    # # example_short_url = "http://dwz.win/NqE"
    # # example_short_url = "http://dwz.date/chCW"
    # if_short_url_list = identify_short_link_from_url(url=example_short_url)
    #
    # print("检测的链接是否为短链接：{0}".format(if_short_url_list))

    """
    测试：本地（离线）识别URL是否属于短链
    """
    short_url_to_tld_dict = local_identify_short_url(content_raw=content_raw)
    print("=======属于短链的原始URL:TLD的字典：{0}=======".format(short_url_to_tld_dict))

    """
    测试：检查URL是否来自短链服务，通过对比TLD
    """
    if_from_shoturl_service = identify_short_url_by_service(url_to_tld_dict=url_to_tld_dict)
    print("本地检测URL是否有来自短链服务提供商的：{0}".format(if_from_shoturl_service))

    """
    测试：检查URL的后缀是否为常见的短链后缀
    """
    if_short_url_suffix = identify_short_url_by_suffix(url_to_tld_dict=url_to_tld_dict)
    print("检查URL的后缀是否为常见的短链后缀：{0}".format(if_short_url_suffix))

    """
    测试：检查URL信息的长度进行判别
    """
    if_short_url_length = identify_short_url_by_length(url_to_tld_dict=url_to_tld_dict)
    print("检查URL信长度是否符合短链的长度特征：{0}".format(if_short_url_length))