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