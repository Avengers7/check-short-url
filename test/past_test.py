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