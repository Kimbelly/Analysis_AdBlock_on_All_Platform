from browsermobproxy import Server
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
import time

server = Server(path="/home/kimbelly/Tools/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
# server default port 8080
proxy = server.create_proxy(params={"trustAllServers": "true", "useEcc": "true"})
# proxy default port 8081

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0'
desired_caps['deviceName'] = 'HTCmobile'
desired_caps['automationName'] = 'UIAutomator2'
desired_caps['appPackage'] = 'com.android.chrome'
desired_caps['appActivity'] = 'com.google.android.apps.chrome.Main'
desired_caps['noReset'] = True
desired_caps['acceptSslCerts'] = True

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

getHAR_file = open('/home/kimbelly/DataSet/Get_HAR_Files/HAR_test.txt', 'a+')
crawlURL_file = open('/home/kimbelly/DataSet/Crawl_URLs/test_url.txt', 'r')
urls = crawlURL_file.read().splitlines()
crawlURL_file.close()
browseURL_count = 1

for url in urls:  # each test website (maybe contain ads)
    print(str(browseURL_count) + ". In: " + url)
    domain = urlparse(url).netloc
    proxy.new_har(domain)
    try:
        driver.get(url)
        time.sleep(8)
    except TimeoutException as e:
        print(url + ": Page load timeout or Invalid URL... moving to next URL !!!")
    except:
        print("It is a bug...?!")
    result = proxy.har
    url_arr = []
    url_set = []
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        url_arr.append(_url)

    url_set = list(set(url_arr))  # Delete duplicate urls
    for elem in url_set:
        getHAR_file.write(elem + "\n")
    browseURL_count += 1

server.stop()
# can't stop the server, you have to run linux command: (important!!)
# sudo netstat -lpn | grep 8080
# sudo kill [the process id]
driver.quit()
getHAR_file.close()

