"""
本模块用于提取URL中的相关信息
"""

from urllib.parse import urlparse
import iocextract
import tldextract.tldextract
import urllib.request

from utils import loads_file


def extract_port(url):
    """
    提取URL中端口
    :param url: 需要解析的URL
    :return: URL中包含的端口号（int型）
    """
    url_after_parse = urlparse(url)
    hostname = url_after_parse.hostname
    port = url_after_parse.port

    return port


def extract_short_link(content_raw):
    """
    从文本中提取全部的短链接
    :param content_raw: 需要传入进行检查的文本
    :return: 文本中所包含的短链接列表
    """
    url_list = iocextract.extract_urls(content_raw)
    short_link_list = []
    for url in url_list:
        if url:
            tld = tldextract.extract(url)
            domain_1 = tld[1] + "." + tld[2]

            if len(domain_1) <= 7:
                short_link_list.append(url)
        else:
            continue

    return short_link_list


def identify_short_link_from_url(url):
    """
    判断该URL是否为短链，根据的逻辑为：
    TODO 待完善
    - 检查TLD
        - TLD是否存在于真实访问的链接中
        - TLD长度是否较短
    - 检查URL请求响应码
        - 响应码是否为302
    :param url: 需要检验的URL
    :return: 判断为短链返回True，不是短链返回False
    """
    # 增加请求头信息，减少出现403错误
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(request)
    # 获取真实访问的链接
    final_url = response.geturl()

    # 提取传入检验URL的TLD
    url_tld = tldextract.extract(url)[1] + '.' + tldextract.extract(url)[2]
    # URL请求响应码
    response_code = response.getcode()

    # 初始化短链接列表
    short_link_list = []

    # 如果传入检验URL的TLD存在真实访问的链接中，则认为其不属于短链
    if url_tld not in final_url:
        # 认为URL的TLD长度大于9则可能不属于短链接，进行下一步判断
        if len(url_tld) <= 9:
            short_link_list.append(url)
            return True
        # 在URL的TLD长度大于9的情况下，且其TLD不在真实访问链接中，则根据响应码判断其是否属于短链
        elif response_code == 302:
            short_link_list.append(url)
            return True
    else:
        if len(url_tld) <= 9:
            short_link_list.append(url)
            return True
    return False


def identify_short_link_from_url_local(url):
    """
    判断该URL是否为短链，根据的逻辑为：
    TODO 待完善
    - 检查TLD
        - TLD长度是否较短
    :param url: 需要检验的URL
    :return: 判断为短链返回True，不是短链返回False
    """

    # 提取传入检验URL的TLD
    url_tld = tldextract.extract(url)[1] + '.' + tldextract.extract(url)[2]
    # 初始化短链接列表
    short_link_list = []
    # 认为URL的TLD长度大于9则可能不属于短链接，进行下一步判断
    if len(url_tld) <= 9:
        short_link_list.append(url)
        return True
    return False


if __name__ == '__main__':
    # example_url = "http://34.64.205.36:9421/"
    # port = extract_port(url=example_url)
    #
    # print(type(port))

    # 测试用邮件数据的路径
    file_path = "../data/content_for_test.json"
    # 对象化邮件文本数据
    content_obj = loads_file.loads_file_to_object(fpath=file_path)
    # 字符串形式的邮件文本数据
    content_raw = loads_file.loads_file_to_content_raw(fpath=file_path)

    """
    测试：从文本中提取全部的短链接
    """
    # short_link_list = extract_short_link(content_raw=content_raw)
    # print(short_link_list)

    """
    测试：判断短链接
    """
    example_short_url = "http://suo.im/5TwT29"
    # example_short_url = "http://tinyurl.com/y2eo5an2"
    # example_short_url = "http://dwz.win/NqE"
    # example_short_url = "http://dwz.date/chCW"
    if_short_url_list = identify_short_link_from_url(url=example_short_url)

    print("检测的链接是否为短链接：{0}".format(if_short_url_list))
