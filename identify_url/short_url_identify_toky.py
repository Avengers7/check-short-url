"""
本模块用于本地（离线）识别URL是否属于短链
（初版）主要有以下四个判断因素：
- 检查URL是否来自短链服务，通过对比TLD
- 检查URL的总体长度是否过长
- 检查URL的TLD是否够短
- 检查URL的TLD是否在域名白名单中
- 检查URL的后缀是否为常见的短链后缀
"""
import copy
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


class IdentifyShortUrl(object):
    """
    类：对文本数据中短链的提取、识别
    """
    def __init__(self):
        self.url_to_tld_dict = {}
        self.content_raw = ""
        self.obj = ""
        """
        判断字典
        字典结构：{URL:是否属于短链服务提供商, URL总体长度是否过长, URL的TLD是否够短, TLD白名单检查, 常见域名后缀检查}
        示例数据：'https://zeek.ir/huhsdfods': [True, False, True, True, False], 'https://virl.com/jdfiehoifn': [True, False, True, False, False]}
        """
        self.judge_dict = {}

    def init_content(self, file_path):
        """
        根据传入的文本数据初始化对象
        :param file_path: 传入的文本数据路径
        :return: none
        """
        # 对象化测试用的文件数据
        self.content_obj = copy.deepcopy(loads_file.loads_file_to_object(fpath=file_path))
        # 字符串形式的文件数据
        self.content_raw = copy.deepcopy(loads_file.loads_file_to_content_raw(fpath=file_path))
        # 从文本内容中提取的URL:TLD字典
        self.url_to_tld_dict = extract_tld(content_raw=self.content_raw)
        # 初始化判断字典
        for url in self.url_to_tld_dict.keys():
            self.judge_dict[url] = []

    def identify_short_url_by_service(self):
        """
        检查URL是否来自短链服务，通过对比TLD
        :param url_to_tld_dict: 从文本内容中提取的URL:TLD字典
        :return: 经过短链服务检查后的URL:TLD字典
        """

        # 属于短链的URL:它的TLD的字典
        short_url_to_tld_dict = {}
        short_url_service_domain_list = loads_file_from_txt_to_list(fpath="../data/short_url_services_list.txt")
        for url in self.url_to_tld_dict.keys():
            flag = False
            for service_domain in short_url_service_domain_list:
                # 传入URL的TLD
                tld = self.url_to_tld_dict[url]
                if tld == service_domain:
                    flag = True
                    short_url_to_tld_dict[url] = tld
            if flag:
                self.judge_dict[url].append(True)
            else:
                self.judge_dict[url].append(False)
        return short_url_to_tld_dict

    def identify_short_url_by_suffix(self):
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

        for url in self.url_to_tld_dict.keys():
            flag = False
            input_url_suffix = tldextract.extract(self.url_to_tld_dict[url])[2]
            # 传入URL的TLD
            tld = self.url_to_tld_dict[url]
            for suffix in suffix_set:
                if input_url_suffix == suffix:
                    flag = True
                    short_url_to_tld_dict[url] = tld
            if flag:
                self.judge_dict[url].append(True)
            else:
                self.judge_dict[url].append(False)

        return short_url_to_tld_dict

    def identify_short_url_by_length(self):
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
        for url in self.url_to_tld_dict.keys():
            tld = self.url_to_tld_dict[url]
            for url in self.url_to_tld_dict.keys():
                if len(url) >= 40:
                    url_length_dict[url] = True
                else:
                    url_length_dict[url] = False

                if len(tld) <= 10:
                    tld_length_dict[url] = True
                else:
                    tld_length_dict[url] = False

        for url in self.url_to_tld_dict.keys():
            if url_length_dict[url]:
                self.judge_dict[url].append(True)
            else:
                self.judge_dict[url].append(False)

        for url in self.url_to_tld_dict.keys():
            if tld_length_dict[url]:
                self.judge_dict[url].append(True)
            else:
                self.judge_dict[url].append(False)

        return short_url_to_tld_dict

    def identify_short_url_by_white_domain_list(self):
        """
        检查URL的TLD是否在域名白名单中
        :param url_list: 从文本内容中提取的URL:TLD字典
        :return: 经过TLD白名单检查后的URL:TLD字典
        """
        # 可能属于短链的URL:TLD的字典
        short_url_to_tld_dict = {}

        top_domain_list = loads_file.loads_file_from_txt_to_list(fpath="../data/top_domain_cn.txt")
        for url in self.url_to_tld_dict.keys():
            flag = False
            tld = self.url_to_tld_dict[url]
            for top_domain in top_domain_list:
                if tld == top_domain:
                    flag = True
                    short_url_to_tld_dict[url] = tld
            if flag:
                self.judge_dict[url].append(True)
            else:
                self.judge_dict[url].append(False)

        return short_url_to_tld_dict

    def local_identify_short_url(self):
        """
        主方法：本地（离线）识别URL是否属于短链
        :param content_raw: 需要检验的字符串文本内容
        :return: 属于短链的原始URL:TLD的字典，示例数据：{'https://zeek.ir/huhsdfods': 'zeek.ir'}
        """

        # 从文本内容中提取的URL:TLD字典
        url_to_tld_dict = extract_tld(content_raw=self.content_raw)

        # 初始化属于短链的URL:TLD的字典
        short_url_to_tld_dict = {}

        # 检查URL是否来自短链服务，通过对比TLD
        self.identify_short_url_by_service()

        # 检查URL信息的长度进行判别
        self.identify_short_url_by_length()

        # 检查URL的后缀是否为常见的短链后缀
        self.identify_short_url_by_suffix()

        # 检查URL的TLD是否在域名白名单中
        self.identify_short_url_by_white_domain_list()

        for url in self.url_to_tld_dict.keys():
            tld = self.url_to_tld_dict[url]
            # 首先，排除URL长度过长的
            if not(self.judge_dict[url][1]):
                # 属于短链服务提供商的，直接认为其属于短链
                if self.judge_dict[url][0]:
                    short_url_to_tld_dict[url] = tld
                # URL长度够短、URL的后缀属于常见短链域名后缀，且不属于TLD白名单的，认为其属于短链
                elif self.judge_dict[url][2] and self.judge_dict[url][4] and not(self.judge_dict[url][3]):
                    short_url_to_tld_dict[url] = tld
                # URL长度不够短但也不过长，URL的后缀属于常见短链域名后缀，且不属于TLD白名单的，认为其属于短链
                elif self.judge_dict[url][4] and not(self.judge_dict[url][3]):
                    short_url_to_tld_dict[url] = tld

        return short_url_to_tld_dict


if __name__ == '__main__':
    # 需要检验的数据文件路径
    file_path = "../data/random_data_one.json"
    # 初始化类的对象
    identifyShortUrl_obj = IdentifyShortUrl()
    # 传入需要检验的数据文件路径
    identifyShortUrl_obj.init_content(file_path=file_path)
    # 经过多种检验后，提取出的短链URL:TLD字典
    short_url_to_tld_dict = identifyShortUrl_obj.local_identify_short_url()
    print("【最终结果】属于短链的原始URL:TLD的字典：{0}".format(short_url_to_tld_dict))
