import traceback
import json
from os import path


def loads_file_to_content_raw(fpath):
    """
    读取文件内容，不进行对象化
    :param fpath: 需要读取的文件
    :return: 字符串形式的文本内容
    """
    try:
        with open(fpath, "r", encoding="utf-8") as fp:
            content_raw = fp.read()
            return content_raw
    except:
        traceback.format_exc()
        return None


def loads_file_to_object(fpath):
    """
    读取文件内容，不进行对象化
    :param fpath: 需要读取的文件
    :return: 对象化后的文本内容
    """
    try:
        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()
            # 字符串文本JSON对象化
            object_content = json.loads(content)
            return object_content
    except:
        traceback.format_exc()
        return None


def loads_file_from_txt_to_list(fpath):
    """
    读取txt格式的文件，并将内容存储为list对象返回
    :param fpath: 文件路径
    :return:文件内容逐行读取后存入的list
    """
    content_list = []
    try:
        with open(fpath, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
            for line in lines:
                content_list.append(line.strip())
            return content_list
    except:
        traceback.format_exc()
        print("文件输入异常，请检查你的文件路径")
        return None


if __name__ == '__main__':
    file_path = "../data/short_url_service.txt"
    print(loads_file_to_content_raw(fpath=file_path))