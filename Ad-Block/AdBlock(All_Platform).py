# 模組化：把蒐集HAR和擋廣告以蒐集Ad URLs，這兩者功能拆開成兩個程式碼檔案
from adblockparser import AdblockRules
from urllib.parse import urlparse
import os

# Prepare rules
Path = "/home/kimbelly/DataSet/Filter_Lists/test/"
file_list = os.listdir(Path)
rules_dic = {}

for x in file_list:
    print("Prepare: " + x)
    with open(Path + x, 'rb') as blocklist_file:
        raw_rules = blocklist_file.read().decode('utf8').splitlines()
    rules_dic[x] = AdblockRules(raw_rules)
    blocklist_file.close()

# Read HAR file
HAR_file = open('/home/kimbelly/DataSet/Get_HAR_Files/AndroidVersion/HAR_Uniq_1.txt', 'r')
urls = HAR_file.read().splitlines()
HAR_file.close()

# For each filter list, start to block
print("=====================================================")
for x in file_list:
    print("Use " + x + " to block ads:")
    block_result_file = open("/home/kimbelly/Analysis/Block_Ads/AndroidVersion/Block_Ads_Uniq_1/" + x + "_BlockResult",
                             'a+')

    ad_count = 0
    for url in urls:
        block_flag = "False"
        try:
            block_flag = rules_dic[x].should_block(url, {'script': True, 'image': True, 'third-party': True,
                                                         'stylesheet': True, 'object': True, 'media': True,
                                                         'xmlhttprequest': True, 'object-subrequest': True,
                                                         'other': True,
                                                         'subdocument': True, 'background': True, 'xbl': True,
                                                         'ping': True, 'dtd': True, 'collapse': True,
                                                         'donottrack': True, 'websocket': True})
        except:
            print("Rule error......")
            continue

        if block_flag:
            block_result_file.write(url + "\n")
            ad_count += 1

    print("Block: #" + str(ad_count))
    readMe_file = open("/home/kimbelly/Analysis/Block_Ads/AndroidVersion/Block_Ads_Uniq_1/ReadMe_1", 'a+')
    readMe_file.write(x + " block #" + str(ad_count) + '\n')
    block_result_file.close()


# Just test ~
'''with open("/home/kimbelly/DataSet/Filter_Lists/test/tmptest", 'rb') as blocklist_file:
    raw_rules = blocklist_file.read().decode('utf8').splitlines()
rules_dic = AdblockRules(raw_rules)
blocklist_file.close()

url = 'https://qq.com/ex?href=abc.com'

try:
    block_flag = rules_dic.should_block(url, {'script': True, 'image': True,'third-party': True,
                                                'stylesheet': True, 'object': True,'media': True,
                                                'xmlhttprequest': True, 'object-subrequest': True, 'other': True,
                                                'subdocument': True, 'background': True, 'xbl': True,
                                                'ping': True, 'dtd': True, 'collapse': True,
                                                'donottrack': True, 'websocket': True})
    if block_flag:
        print("yes")
    else:
        print("no")
except:
    print("Rule error......")'''

