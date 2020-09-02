import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 引入根目录，让程序在执行的单个文件时能找到根目录
sys.path.append(rootPath)

from identify_url import short_url_identify
from identify_url import argument_parse


if __name__ == '__main__':
    # 需要检验的数据文件的相对路径
    file_path_relative = argument_parse.get_file()
    # 需要检验的数据文件的绝对路径
    file_path_absolute = os.path.abspath(file_path_relative)
    # 初始化类的对象
    identifyShortUrl_obj = short_url_identify.IdentifyShortUrl()
    # 传入需要检验的数据文件路径
    identifyShortUrl_obj.init_content(file_path=file_path_absolute)
    # 经过多种检验后，提取出的短链URL:TLD字典
    short_url_to_tld_dict = identifyShortUrl_obj.local_identify_short_url()
    print(short_url_to_tld_dict)