# import os
# import sys
#
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# # 引入根目录，让程序在执行的单个文件时能找到根目录
# sys.path.append(rootPath)
#
# from extract_url.extract_short_url import extract_tld
# from identify_url.short_url_identify import local_identify_short_url, identify_short_url_by_service, \
#     identify_short_url_by_suffix, identify_short_url_by_length, identify_short_url_by_white_domain_list
# from utils import loads_file
#
#
# if __name__ == '__main__':
#     # 测试用数据的路径
#     # file_path = "../data/content_for_test.json"
#     file_path = "../data/random_data_one.json"
#     # 对象化测试用的文件数据
#     content_obj = loads_file.loads_file_to_object(fpath=file_path)
#     # 字符串形式的文件数据
#     content_raw = loads_file.loads_file_to_content_raw(fpath=file_path)
#     # 从文本内容中提取的URL:TLD字典
#     url_to_tld_dict = extract_tld(content_raw=content_raw)
#
#     """
#     测试：本地（离线）识别URL是否属于短链
#     """
#     short_url_to_tld_dict = local_identify_short_url(content_raw=content_raw)
#     print("【最终结果】属于短链的原始URL:TLD的字典：{0}".format(short_url_to_tld_dict))
#
#     print("{0}以下为单条判断的测试{1}".format('='*20,'='*20))
#
#     """
#     测试：检查URL是否来自短链服务，通过对比TLD
#     """
#     if_from_short_url_service = identify_short_url_by_service(url_to_tld_dict=url_to_tld_dict)
#     print("本地检测URL是否有来自短链服务提供商的：{0}".format(if_from_short_url_service))
#
#     """
#     测试：检查URL的后缀是否为常见的短链后缀
#     """
#     if_short_url_suffix = identify_short_url_by_suffix(url_to_tld_dict=url_to_tld_dict)
#     print("检查URL的后缀是否为常见的短链后缀：{0}".format(if_short_url_suffix))
#
#     """
#     测试：检查URL信息的长度进行判别
#     """
#     if_short_url_length = identify_short_url_by_length(url_to_tld_dict=url_to_tld_dict)
#     print("检查URL信长度是否符合短链的长度特征：{0}".format(if_short_url_length))
#
#     """
#     测试：检查URL的TLD是否在域名白名单中
#     """
#     if_tld_in_domain_white_list = identify_short_url_by_white_domain_list(url_to_tld_dict=url_to_tld_dict)
#     print("检查URL的TLD是否在域名白名单中：{0}".format(if_tld_in_domain_white_list))
#
#     """
#     {是否属于短链服务提供商, URL总体长度是否过长, URL的TLD是否够短, TLD白名单检查, 常见域名后缀检查}
#     """