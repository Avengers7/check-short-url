# def identify_short_link_from_url(url):
#     """
#     判断该URL是否为短链，根据的逻辑为：
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


# def local_identify_short_url(self):
#     """
#     本地（离线）识别URL是否属于短链
#     :param content_raw: 需要检验的字符串文本内容
#     :return: 属于短链的原始URL:TLD的字典，示例数据：{'https://zeek.ir/huhsdfods': 'zeek.ir'}
#     """
#
#     # 从文本内容中提取的URL:TLD字典
#     url_to_tld_dict = extract_tld(content_raw=self.content_raw)
#
#     # 初始化属于短链的URL:TLD的字典
#     short_url_to_tld_dict = {}
#
#
#     # 经过短链服务检查后的URL:TLD字典
#     url_to_tld_dict_after_service = self.identify_short_url_by_service()
#     # 更新总共的短链的URL:TLD字典
#     short_url_to_tld_dict.update(url_to_tld_dict_after_service)
#
#     # 经过常见的短链后缀检查后的URL:TLD字典
#     url_to_tld_dict_after_suffix_check = self.identify_short_url_by_suffix()
#     # 更新总共的短链的URL:TLD字典
#     short_url_to_tld_dict.update(url_to_tld_dict_after_suffix_check)
#
#     # 经过URL长度是否符合短链长度特征后的URL:TLD字典
#     url_to_tld_after_length_check = self.identify_short_url_by_length()
#     # 更新总共的短链的URL:TLD字典
#     short_url_to_tld_dict.update(url_to_tld_after_length_check)
#
#     # 经过检查URL的TLD是否在域名白名单中
#     url_to_tld_after_domain_white_list_check = self.identify_short_url_by_white_domain_list()
#     # 更新总共的短链的URL:TLD字典
#     short_url_to_tld_dict.update(url_to_tld_after_domain_white_list_check)
#
#     # 将可信度较低的筛选结果求交集
#     part_one_short_url_list = list(url_to_tld_dict_after_suffix_check.keys() &
#                                    url_to_tld_after_domain_white_list_check.keys())
#     # 将可行度较高的筛选结果求交集
#     part_two_short_url_list = list(url_to_tld_dict_after_service.keys() & url_to_tld_after_length_check.keys())
#
#     # 将可信度较低结果的交集与高可信结果做并集，得到最终确定的短链URL列表
#     # final_short_url_list = part_one_short_url_list + part_two_short_url_list
#
#     final_short_url_list = list(url_to_tld_dict_after_suffix_check.keys() & url_to_tld_after_domain_white_list_check.keys()\
#                            & url_to_tld_dict_after_service.keys() & url_to_tld_after_length_check.keys())
#
#     # 将最终确定的短链URL转化为集合（set），去重
#     final_short_url_set = set(final_short_url_list)
#
#     return final_short_url_set

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
