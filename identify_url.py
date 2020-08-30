import urllib.request
import tldextract
import argparse


def identify_short_link_from_url(url):
    """
    判断该URL是否为短链,根据的逻辑为:
    - 检查TLD顶级域名
        - TLD是否存在于真实访问的链接中
        - TLD长度是否较短
    - 检查URL请求响应码
        - 响应码是否为302
    :param url: 需要检验的URL
    :return: 判断为短链返回True, 不是短链返回False
    """
    # 打开url
    response = urllib.request.urlopen(url)

    # 获取真实访问的链接，返回请求的url
    final_url = response.geturL()
    # 提取传入检验URL的TLD
    # ExtractResult(subdomain, domain, suffix)
    url_tld = tldextract.extract(url)[0] + '.' + tldextract.extract(url)[1]
    # URL请求响应码
    response_code = response.getcode()

    # 初始化链接列表
    # short_link_list = []

    # 如果传入检验URL的TLD存在真实访问的链接中，则认为其不属于短链
    if url_tld not in final_url:
        # 认为URL的TLD长度大于9则可能不属于短链接，进行下一步判断
        if len(url_tld) <= 9:
            with open('short_link_list.txt', 'a') as list:
                list.write(url+'\n')
            # short_link_list.append(url)
            return True
        # 在URL的TLD长度大于9的情况下，且其TLD不在真实访问链接中，则根据响应码判断其是否属于短链
        elif response_code == 302:
            with open('short_link_list.txt', 'a') as list:
                list.write(url+'\n')
            # short_link_list.append(url)
            return True
    else:
        return False


def add_help():
    """
    # argparse用于解析命令行参数
    :return:
    """
    # 创建一个解析对象
    parser = argparse.ArgumentParser(description='check short url')
    # 向该对象中添加你要关注的命令行参数和选项，每一个add_argument方法对应一个你要关注的参数或选项
    parser.add_argument('--url', '-u', help='url you want to identify')
    # 调用parse_args()方法进行解析，解析成功之后即可使用
    args = parser.parse_args()


if __name__ == '__main__':
    # add_help()
    identify_short_link_from_url('http://suo.im/5TUxCn')
