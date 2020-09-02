import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 引入根目录，让程序在执行的单个文件时能找到根目录
sys.path.append(rootPath)

import argparse
from utils import loads_file


# 创建一个解析对象
parser = argparse.ArgumentParser(description='check short url')
# 向该对象中添加你要关注的命令行参数和选项，每一个add_argument方法对应一个你要关注的参数或选项
parser.add_argument('-f', '--file', help='the file you want to identify')
# 调用parse_args()方法进行解析，解析成功之后即可使用
args = parser.parse_args()


def get_file():
    file_path = args.file

    return file_path

# def


if __name__ == '__main__':
    print(get_file())
