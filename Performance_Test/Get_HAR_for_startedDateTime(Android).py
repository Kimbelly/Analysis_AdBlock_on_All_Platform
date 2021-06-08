#from selenium import webdriver
from appium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import os
import pprint
#from sudo import run_as_sudo
import subprocess

desired_caps = {}

### Use Android Emulator ###
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['automationName'] = 'UIAutomator2'
# desired_caps['browserName'] = 'Chrome'
desired_caps['appPackage'] = 'com.android.chrome'
desired_caps['appActivity'] = 'com.google.android.apps.chrome.Main'
desired_caps['noReset'] = True
desired_caps['acceptSslCerts'] = True
# desired_caps['fullReset'] = False

### Use Real Device ###
# desired_caps['platformName'] = 'Android'
# desired_caps['platformVersion'] = '6.0'
# desired_caps['deviceName'] = 'HTCmobile'
# desired_caps['automationName'] = 'UIAutomator2'
# desired_caps['appPackage'] = 'com.android.chrome'
# desired_caps['appActivity'] = 'com.google.android.apps.chrome.Main'
# desired_caps['noReset'] = True
# desired_caps['acceptSslCerts'] = True

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

crawlURL_file = open('/home/kimbelly/DataSet/Crawl_URLs/Test_URLs.txt', 'r')
urls = crawlURL_file.read().splitlines()
crawlURL_file.close()
browseURL_count = 1
time.sleep(2)

for url in urls:  # each test website (maybe contain ads)
    print(str(browseURL_count) + ". In: " + url)

    time.sleep(1)
    proc = subprocess.Popen(['sudo /home/kimbelly/Run_mitmproxy/run_mitmproxy_' + str(browseURL_count) + '.sh'], shell=True)

    driver.implicitly_wait(20)
    try:
        driver.get(url)
        time.sleep(8)
    except TimeoutException as e:
        print(url + ": Page load timeout or Invalid URL... moving to next URL !!!")
    except:
        pass
        #print("It is a bug...?!")

    proc.terminate()
    proc2 = subprocess.Popen(['sudo /home/kimbelly/Run_mitmproxy/stop_mitmproxy.sh'], shell=True)
    time.sleep(1)
    proc2.terminate()
    browseURL_count += 1
    driver.quit()
    time.sleep(2)
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

#driver.quit()

