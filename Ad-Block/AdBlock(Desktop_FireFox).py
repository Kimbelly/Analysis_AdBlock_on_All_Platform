# 正式測試
# 缺點：MITM蒐集URLs和擋廣告功能的程式碼合在一起寫，尚未模組化
from adblockparser import AdblockRules
from browsermobproxy import Server
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
import time
import os
import pprint


class ProxyManger:
    __BMP = "/home/kimbelly/Tools/browsermob-proxy-2.1.4/bin/browsermob-proxy"

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

    profile = webdriver.FirefoxProfile()
    profile.set_proxy(client.selenium_proxy())
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    # Disable download popup
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.download.animateNotifications", False)
    profile.set_preference("browser.download.show_plugins_in_list", False)
    profile.set_preference("dom.popup_maximum", 0)
    # profile.set_preference("network.http.use-cache", False)
    driver = webdriver.Firefox(executable_path='/home/kimbelly/Tools/geckodriver', firefox_profile=profile)
    driver.set_page_load_timeout(20)

    Path = "/home/kimbelly/Experiment/Block_Ads/FilterList/test/"
    file_list = os.listdir(Path)
    rules_dic = {}
    block_result_file = []
    i = 1
    block_result_file.append(None)  # don't need block_result_file[0]

    for x in file_list:
        print(x + " = " + str(i))
        block_result_file.append(open("/home/kimbelly/Experiment/Block_Ads/Block_Result/Crawl_Result_5/Result" + str(i) + "_" + x + '.txt', 'w'))
        i += 1
        with open(Path + x, 'rb') as blocklist_file:
            raw_rules = blocklist_file.read().decode('utf8').splitlines()
        rules_dic[x] = AdblockRules(raw_rules)
        blocklist_file.close()

    testURL_file = open('/home/kimbelly/Experiment/Crawl_TestURLs/Crawl_Result/Crawl_Result_5.txt', 'r')
    urls = testURL_file.read().splitlines()
    browseURL_count = 1

    for url in urls:  # each test website (maybe contain ads)
        print(str(browseURL_count) + ". In the URL: " + url)
        domain = urlparse(url).netloc
        client.new_har(domain)
        try:
            driver.get(url)
            time.sleep(7)
        except TimeoutException as e:
            print(url + ": Page load timeout or Invalid URL... moving to next URL !!!")
        except:
            print("May be 'Reached error page' occurred")

        result = client.har
        url_arr = []
        url_set = []
        j = 1
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            url_arr.append(_url)

        url_set = list(set(url_arr))  # Delete duplicate urls
        block_flag = "False"
        ad_count = 0
        for x in file_list:
            for elem in url_set:
                try:
                    block_flag = rules_dic[x].should_block(elem, {'script': True, 'image': True,
                                                                  'stylesheet': True, 'object': True,
                                                                  'xmlhttprequest': True, 'object-subrequest': True,
                                                                  'other': True, 'media': True, 'third-party': True})
                except:
                    print("Rule error......")
                    continue

                if block_flag:
                    # print("Block: " + elem)
                    block_result_file[j].write(elem + "\n")
                    ad_count += 1

            print(x + ": Block #" + str(ad_count))
            ad_count = 0
            j += 1
        browseURL_count += 1

    for k in range(1, len(block_result_file)):
        block_result_file[k].close()

    server.stop()
    driver.quit()
