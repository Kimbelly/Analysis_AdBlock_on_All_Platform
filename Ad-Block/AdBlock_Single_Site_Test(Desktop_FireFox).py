# 單一網站測試
# 缺點：MITM蒐集URLs和擋廣告功能的程式碼合在一起寫，尚未模組化
from adblockparser import AdblockRules
from browsermobproxy import Server
from selenium import webdriver
import pprint
import time

class ProxyManger:
    __BMP = "/home/kimbelly/browsermob-proxy-2.1.4/bin/browsermob-proxy"

    def __init__(self):
        self.__server = Server(ProxyManger.__BMP)
        self.__client = None

    def start_server(self):
        self.__server.start()
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(params={"trustAllServers": "true"})
        return self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server

if "__main__" == __name__:
    proxy = ProxyManger()
    server = proxy.start_server()
    client = proxy.start_client()
    client.new_har("charleslin74.pixnet.net")
    print(client.proxy)

    with open('easylist.txt', 'rb') as f:
        raw_rules = f.read().decode('utf8').splitlines()
    rules = AdblockRules(raw_rules)

    profile = webdriver.FirefoxProfile()
    profile.set_proxy(client.selenium_proxy())
    driver = webdriver.Firefox(executable_path='/home/kimbelly/geckodriver', firefox_profile=profile)
    driver.set_page_load_timeout(30)
    driver.get("https://www.w3schools.com/js/js_whereto.asp")
    time.sleep(5)

    result = client.har
    url_arr = []
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        url_arr.append(_url)

    url_set = list(set(url_arr))
    block_flag = "False"
    ad_count = 0
    for elem in url_set:
        #print(elem)
        block_flag = rules.should_block(elem, {'third-party': True})
        if block_flag:
            #print(elem)
            ad_count = ad_count + 1

    print(ad_count)

    server.stop()
    driver.quit()
