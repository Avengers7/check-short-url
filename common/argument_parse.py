import os
import sys

from identify_url import short_url_identify

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 引入根目录，让程序在执行的单个文件时能找到根目录
sys.path.append(rootPath)

import argparse
import copy


class ArgumentParse(object):
    """
    类：变量处理类
    """
    def __init__(self):
        # 创建一个解析对象
        parser = argparse.ArgumentParser(description='check short url')
        # 向该对象中添加你要关注的命令行参数和选项，每一个add_argument方法对应一个你要关注的参数或选项
        parser.add_argument('-f', '--file', help='the file you want to identify')
        # 调用parse_args()方法进行解析，解析成功之后即可使用
        self.args = parser.parse_args()
        self.relative_path = ""
        self.absolute_path = ""
        self.result_dict = {}

    def get_file_path(self):
        """
        在终端获取文件路径
        :return:none
        """
        file_path = self.args.file
        self.relative_path = file_path

    def change_path(self):
        """
        路径转化
        :return:none
        """
        # 设置需要检验的数据文件的绝对路径
        self.absolute_path = copy.deepcopy(os.path.abspath(self.relative_path))

    def init_content(self):
        """
        主方法：初始化短链识别类的对象内容
        :return:
        """
        self.get_file_path()
        self.change_path()

        # 初始化类的对象
        identifyShortUrl_obj = short_url_identify.IdentifyShortUrl()
        # 传入需要检验的数据文件路径
        identifyShortUrl_obj.init_content(file_path=self.absolute_path)
        # 经过多种检验后，提取出的短链URL:TLD字典
        short_url_to_tld_dict = identifyShortUrl_obj.local_identify_short_url()
        self.result_dict = copy.deepcopy(short_url_to_tld_dict)