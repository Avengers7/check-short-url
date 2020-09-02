import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 引入根目录，让程序在执行的单个文件时能找到根目录
sys.path.append(rootPath)

from common import argument_parse

if __name__ == '__main__':
    # 初始化变量处理类
    argument_obj = argument_parse.ArgumentParse()
    # 初始化短链识别类的对象内容
    argument_obj.init_content()
    # 经过多种检验后，提取出的短链URL:TLD字典
    short_url_to_tld_dict = argument_obj.result_dict
    print(short_url_to_tld_dict)