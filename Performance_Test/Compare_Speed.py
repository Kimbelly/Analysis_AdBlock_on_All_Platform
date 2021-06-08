import json
from datetime import datetime
import time

# har_dir = '/home/mitmproxyuser/dump_har/VPN/'
# # AdBlock, No_VPN, AdandDoT_Block
# getTime_file = open('/home/kimbelly/Analysis/Time_Delay/VPN.txt', 'a+')
#
# fmt = '%Y-%m-%dT%H:%M:%S.%f+00:00'
#
# for i in range(1, 1001):  # 1, 1001
#     har_file = har_dir + 'dump_' + str(i) + '.har'
#     ans = 0
#     end_count = 0
#     list_t = []
#     with open(har_file) as json_file:
#         data = json.load(json_file)
#         for entry in data['log']['entries']:
#             list_t.append(entry['startedDateTime'])
#             end_count += 1
#
#     if end_count == 0:
#         getTime_file.write("0:00:00.0\n")
#     else:
#         list_t.sort()
#         start = datetime.strptime(list_t[0], fmt)
#         end = datetime.strptime(list_t[end_count-1], fmt)
#         ans = end - start
#         getTime_file.write(str(ans) + "\n")
#
# getTime_file.close()

# Calculate average, ignore strange data: too small or too large
f = open('/home/kimbelly/Analysis/Time_Delay/AdandDoH_Block.txt', 'r')
waits = f.read().splitlines()
f.close()

fmt = '0:00:%S.%f'

ans = 0
count = 1000
for wait in waits:
    t = datetime.strptime(wait, fmt)
    if t.second == 0:  # t.second == 0 or t.second > 17
        count -= 1  # too small or too large
    else:
        ss = (t.second * 1000000 + t.microsecond) / 1000000
        ans += ss
    # ss = (t.second * 1000000 + t.microsecond) / 1000000
    # ans += ss

print("count: " + str(count))
ans /= count
print("Average : " + str(ans))
# f2 = open('/home/kimbelly/Analysis/Time_Delay/average.txt', 'a+')

# f2.write("Average of VPN: " + str(ans) + "\n")
# f2.write("Average of No_VPN: " + str(ans) + "\n")
# f2.write("Average of AdandDoH_Block: " + str(ans) + "\n")
# f2.write("Average of AdBlock: " + str(ans) + "\n")

# f2.write("Average of (AdBlock - No_VPN): " + str(ans) + "\n")
# f2.write("Average of (AdandDoH_Block - No_VPN): " + str(ans) + "\n")
# f2.write("Average of (AdandDoH_Block - AdBlock): " + str(ans) + "\n")


##############################################################
### AdBlock - No_VPN
# AdBlock_time_f = open('/home/kimbelly/Analysis/Time_Delay/AdBlock.txt', 'r')
# adblock_t = AdBlock_time_f.read().splitlines()
# AdBlock_time_f.close()
#
# No_VPN_time_f = open('/home/kimbelly/Analysis/Time_Delay/No_VPN.txt', 'r')
# noVPN_t = No_VPN_time_f.read().splitlines()
# No_VPN_time_f.close()
#
# cmp_file = open('/home/kimbelly/Analysis/Time_Delay/AdBlock_vs_No_VPN.txt', 'a+')
#
# for i in range(0, 1000):
#     ans = int(adblock_t[i]) - int(noVPN_t[i])
#     cmp_file.write(str(ans) + "\n")
#
# cmp_file.close()

### AdandDoH_Block - No_VPN

### AdandDoH_Block - AdBlock

