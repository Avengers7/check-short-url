#
# def learn():
#     print("I love study!")
#
#
# if __name__ == '__main__':
#     while True: learn()
#
#
#
from utils.loads_file import loads_file_from_txt_to_list
import tldextract.tldextract

if __name__ == '__main__':
    short_url_service_domain_list = loads_file_from_txt_to_list(fpath="../data/short_url_services_list.txt")
    suffix_set = set()
    for url in short_url_service_domain_list:
        suffix = tldextract.extract(url)[2]
        suffix_set.add(suffix)

    print(suffix_set)