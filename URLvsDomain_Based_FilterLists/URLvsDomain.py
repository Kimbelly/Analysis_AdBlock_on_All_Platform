import os
import re
from urllib.parse import urlparse
from adblockparser import AdblockRules

### Desktop v.s Android on "Count_Domain_Combine_All_BlockResult"
'''Path = "/home/kimbelly/Analysis/Count_Domain_From_URLandDomain-based/"
f_android = open(Path + "AndroidVersion/Uniq(HAR)_1/Compress/Count_Domain_Combine_All_BlockResult_compres", 'r')
domains_android = f_android.read().splitlines()
f_android.close()
f_desk = open(Path + "DesktopVersion/Uniq(HAR)_1/Compress/Count_Domain_Combine_All_BlockResult_compres", 'r')
domains_desk = f_desk.read().splitlines()
f_desk.close()

# Only for Android
onlyFor_android = open(Path + "/OnlyFor_Android_onDomain_Combine_All_ads", 'w')
for android_line in domains_android:
    android_domain = [i for j in android_line.split() for i in (j, ' ')][2:-1]
    uniq = True
    for desk_line in domains_desk:
        desk_domain = [i for j in desk_line.split() for i in (j, ' ')][2:-1]
        if android_domain == desk_domain:
            uniq = False
            break
    if uniq:
        onlyFor_android.write(android_line + '\n')

# Only for Desktop
onlyFor_desk = open(Path + "/OnlyFor_Desktop_onDomain_Combine_All_ads", 'w')
for desk_line in domains_desk:
    desk_domain = [i for j in desk_line.split() for i in (j, ' ')][2:-1]
    uniq = True
    for android_line in domains_android:
        android_domain = [i for j in android_line.split() for i in (j, ' ')][2:-1]
        if desk_domain == android_domain:
            uniq = False
            break
    if uniq:
        onlyFor_desk.write(desk_line + '\n')'''


### Regex version
# Extract domains from URL-based filter results
# and then feed these domains into Domain-based filter lists
'''Path1 = "/home/kimbelly/DataSet/Filter_Lists/Domain_regex/Other_Combine/"
file_list1 = os.listdir(Path1)
domain_rules_dic = {}
for f1 in file_list1:
    if f1.startswith("Domain"):
        print("Domain-based file: " + f1)
        domainRules_file = open(Path1 + f1, 'r')
        domain_rules_dic[f1] = domainRules_file.read().splitlines()
        domainRules_file.close()

Path2 = "/home/kimbelly/Analysis/Block_Ads/AndroidVersion/Block_Ads_Uniq_1/"
file_list2 = os.listdir(Path2)
#readMe_file = open("/home/kimbelly/Analysis/URL_vs_Domain/AndroidVersion/Miss_URLtoDomain_Uniq_1/ReadMe_Miss_1", 'a+')
for f2 in file_list2:
    if f2.startswith("URL"):
        print("========================================================")
        #readMe_file.write("========================================================" + '\n')
        print("Process the URL-based file: " + f2)
        #readMe_file.write("Process the URL-based file: " + f2 + '\n')
        blockResult_file = open(Path2 + f2, 'r')
        urls = blockResult_file.read().splitlines()
        blockResult_file.close()

        print("    Total blocked-urls: #" + str(len(urls)))
        #readMe_file.write("    Total blocked-urls: #" + str(len(urls)) + '\n')
        #os.mkdir("/home/kimbelly/Analysis/URL_vs_Domain/AndroidVersion/Miss_URLtoDomain_Uniq_1/" + f2)

        for f1 in file_list1:
            if f1.startswith("Domain"):
                # Create files to store URLs which each Domain-based filter missed
                miss_file = open("/home/kimbelly/Analysis/URL_vs_Domain/AndroidVersion/Miss_URLtoDomain_Uniq_1/"
                                 + f2 + "/Miss_" + f1, 'a+')
                count_match_domain = 0
                domain_regex = '(?:% s)' % '|'.join(domain_rules_dic[f1])
                for url in urls:  # ad URL -> ad domain
                    domain = urlparse(url).netloc
                    if re.match(domain_regex, domain):
                        count_match_domain += 1
                    else:
                        miss_file.write(url + "\n")

                print("    " + f1 + ": Block #" + str(count_match_domain))
                #readMe_file.write("    " + f1 + ": Block #" + str(count_match_domain) + '\n')
                miss_file.close()'''
### Then run 'Count_NoMiss_About_URLtoDomain.sh'


# Extract domains from "Domain-based" filter results
# and then feed these domains into "URL-based" filter lists
# (must use Adblock parser version, not Regex)
'''Path1 = "/home/kimbelly/DataSet/Filter_Lists/test/"
file_list1 = os.listdir(Path1)
URL_rules_dic = {}
for f1 in file_list1:
    if f1.startswith("URL"):
        with open(Path1 + f1, 'rb') as URLRules_file:
            raw_rules = URLRules_file.read().decode('utf8').splitlines()
        URL_rules_dic[f1] = AdblockRules(raw_rules)
        URLRules_file.close()

Path2 = "/home/kimbelly/Analysis/Block_Ads/DesktopVersion/Block_Ads_Uniq_1/"
file_list2 = os.listdir(Path2)
readMe_file = open("/home/kimbelly/Analysis/URL_vs_Domain/DesktopVersion/Miss_DomaintoURL_Uniq_1/ReadMe_Miss_1", 'a+')
for f2 in file_list2:
    if f2.startswith("Domain"):
        print("========================================================")
        readMe_file.write("========================================================" + '\n')
        print("Process the Domain-based file: " + f2)
        readMe_file.write("Process the Domain-based file: " + f2 + '\n')
        blockResult_file = open(Path2 + f2, 'r')
        urls = blockResult_file.read().splitlines()
        blockResult_file.close()

        print("    Total blocked-urls: #" + str(len(urls)))
        readMe_file.write("    Total blocked-urls: #" + str(len(urls)) + '\n')
        os.mkdir("/home/kimbelly/Analysis/URL_vs_Domain/DesktopVersion/Miss_DomaintoURL_Uniq_1/" + f2)

        for f1 in file_list1:
            if f1.startswith("URL"):
                # Create files to store URLs which each URL-based filter missed
                miss_file = open("/home/kimbelly/Analysis/URL_vs_Domain/DesktopVersion/Miss_DomaintoURL_Uniq_1/"
                                 + f2 + "/Miss_" + f1, 'a+')
                count_match = 0
                for url in urls:
                    block_flag = False
                    try:
                        block_flag = URL_rules_dic[f1]. \
                            should_block(url, {'script': True, 'image': True,'third-party': True,
                                                'stylesheet': True, 'object': True,'media': True,
                                                'xmlhttprequest': True, 'object-subrequest': True,'other': True,
                                                'subdocument': True, 'background': True, 'xbl': True,
                                                'ping': True, 'dtd': True, 'collapse': True,
                                                'donottrack': True, 'websocket': True})
                    except:
                        print("Rule error......")
                        continue

                    if block_flag:
                        count_match += 1
                    else:
                        miss_file.write(url + "\n")

                print("    " + f1 + ": Block #" + str(count_match))
                readMe_file.write("    " + f1 + ": Block #" + str(count_match) + '\n')
                miss_file.close()'''

### Then run 'Count_NoMiss_About_DomaintoURL.sh'


# Count the types of domains from URL-based/Domain-based block result
#Path1 = "/home/kimbelly/Analysis/Block_Ads/DesktopVersion/Block_Ads_Uniq_1/"
Path1 = "/home/kimbelly/Analysis/URL_vs_Domain/AndroidVersion/Miss_DomaintoURL_Uniq_1/Domain_Combine_All_BlockResult/"
file_list1 = os.listdir(Path1)
for f1 in file_list1:
    if f1.startswith("ReadMe"):
        print("Skip: " + f1)
    elif f1.startswith("Miss_URL_Combine_All"):  # else:
        print("Process: " + f1)
        blockResult_file = open(Path1 + f1, 'r')
        urls = blockResult_file.read().splitlines()
        blockResult_file.close()
        #extractDomain_file = open("/home/kimbelly/Analysis/Count_Domain_From_URLandDomain-based/DesktopVersion/Uniq("
         #                         "HAR)_1/" + "Count_" + f1, 'a+')
        extractDomain_file = open(Path1 + "Count_" + f1, 'a+')
        for url in urls:  # ad URL -> ad domain
            domain = urlparse(url).netloc
            extractDomain_file.write(domain + "\n")
        extractDomain_file.close()

### Start counting: run script 'Count_Domain_From_URLandDomain-based.sh'

