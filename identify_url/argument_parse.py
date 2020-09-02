import argparse
from utils import loads_file

# 创建一个解析对象
parser = argparse.ArgumentParser(description='check short url')
# 向该对象中添加你要关注的命令行参数和选项，每一个add_argument方法对应一个你要关注的参数或选项
parser.add_argument('-f','--file', help='the file you want to identify')
# 调用parse_args()方法进行解析，解析成功之后即可使用
args = parser.parse_args()


def get_file(file):
    file_path = file
    content_raw = loads_file.loads_file_to_content_raw(fpath = file_path)


if __name__ == '__main__':
    print(get_file(args.file))
