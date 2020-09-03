import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import re
import iocextract
from tldextract import tldextract
from utils import loads_file
from bs4 import BeautifulSoup


class ExtractUrl(object):
    """
    类：对文本数据进行短链提取
    """
    def __init__(self):
        pass

    # def extract_all_url_test(self, content_raw):
    #     """
    #     提取文本中全部的URL
    #     :param content_raw: 传入进行提取全部URL的文本
    #     :return: 文本中全部URL的列表
    #     """
    #
    #     # 经过iocextract提取后的URL列表
    #     url_list_after_ioc = iocextract.extract_urls(content_raw)
    #     """
    #     iocextract提取测试
    #     """
    #     url_number_after_ioc = len(list(url_list_after_ioc))
    #     url_list_after_ioc_test = []
    #     for url in url_list_after_ioc:
    #         url_list_after_ioc_test.append(url)
    #     # print("经过ioc提取后的URL列表：{0}".format(url_list_after_ioc_test))
    #     # print("经过ioc提取后的URL列表：{0}".format(list(url_list_after_ioc)))
    #     print("经过ioc提取后的URL链接数量为：{0}".format(url_number_after_ioc))
    #
    #     # 经过正则表达式提取后的URL列表
    #     url_list_after_regexp = self.extract_url_by_regexp()
    #     """
    #     正则表达式提取测试
    #     """
    #     url_number_after_regexp = len(url_list_after_regexp)
    #     url_list_after_regexp_show = []
    #     for url in url_list_after_regexp:
    #         url_list_after_regexp_show.append(url)
    #     print("经过正则表达式提取后的URL列表：{0}：".format(url_list_after_regexp_show))
    #     print("经过正则表达式提取后的URL链接数量为：{0}".format(url_number_after_regexp))
    #
    #     url_list_final = []
    #
    #     # TODO 需要进一步降低误报
    #
    #     return url_list_after_ioc

    def extract_url_by_regexp(self, content_raw):
        """
        根据正则表达式匹配文本中的URL
        :param content_raw: 传入进行提取全部URL的文本
        :return: 文本中全部URL的列表
        """
        url_list = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', content_raw)
        return url_list

    def extract_all_url(self, content_raw):
        """
        提取文本中全部的URL
        :param content_raw: 传入进行提取全部URL的文本
        :return: 文本中全部URL的列表
        """

        # 经过iocextract提取后的URL列表
        url_list_after_ioc = self.extract_all_url_simple(content_raw=content_raw)

        # 经过dots判断的URL列表
        url_list_after_dots = self.judge_by_dots(url_list_after_ioc=url_list_after_ioc)

        # 经过beautifulsoup去除标签的URL列表
        url_list_after_beautifulsoup = self.remove_html_tags(list_dots=url_list_after_dots)
        # print("url_list_after_beautifulsoup", url_list_after_beautifulsoup)
        return url_list_after_beautifulsoup

    def extract_all_url_simple(slef, content_raw):
        """
        提取文本中全部的URL（仅使用iocextract）
        :param content_raw: 传入进行提取全部URL的文本
        :return: 文本中全部URL的列表
        """

        # 经过iocextract提取后的URL列表
        url_list_after_ioc = iocextract.extract_urls(content_raw)
        return url_list_after_ioc

    def judge_by_dots(self, url_list_after_ioc):
        """
        通过点号数量判单是否为短链（短链<3）
        :param url_list_after_ioc: url list after iocextract
        :return: url_list_after_dots
        """

        iocextract_url = []
        list_dots = []
        list_more_dots = []
        for url in url_list_after_ioc:
            iocextract_url.append(url)

        # dots判断
        for url in iocextract_url:
            count = url.count('.')
            if count < 3:
                list_dots.append(url)
            else:
                list_more_dots.append(url)

        return list_dots

    def remove_html_tags(self, list_dots):
        """
        使用beautifulsoup去除标签
        :param list_dots: 经过dots判断的短链
        :return: 去除标签后的URL列表
        """

        list_dots_init = []
        list_soup = []
        for url in list_dots:
            list_dots_init.append(url)

        list_dots_init = "\n".join(list_dots_init)

        # beautifulsoup去除标签
        soup = BeautifulSoup(list_dots_init, features="html.parser")
        # 移除标签
        valid_tags = ['a']
        for tag in soup.find_all(True):
            if tag.name in valid_tags:
                tag.extract()

        soup = "\n".join(soup)

        # 再次iocextract提取
        soup = iocextract.extract_urls(soup)
        for url in soup:
            list_soup.append(url)
        return list_soup

    def extract_tld(self, content_raw):
        """
        提取文本中全部URL的TLD
        :param content_raw: 传入进行提取TLD的文本
        :return: 文本中所包含链接:TLD的字典，示例数据：{'https://zeek.ir/': 'zeek.ir'}
        """
        # url_list = extract_all_url(content_raw)
        # 测试使用
        url_list = self.extract_all_url_simple(content_raw)

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
    file_path = "../data/random_data_one.json"
    content_raw = loads_file.loads_file_to_content_raw(fpath=file_path)

    # """
    # 测试：提取文本中全部URL的TLD
    # """
    # tld_list = extract_tld(content_raw)
    # print(tld_list)

    """
    测试：提取文本中的全部URL
    """
    extract = ExtractUrl()
    list = extract.extract_all_url(content_raw=content_raw)
    print(list)

    # """
    # 测试：从文本中根据正则表达式
    # """
    # url_list = extract_url_by_regexp(content_raw=content_raw)
    # print(url_list)
