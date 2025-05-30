# import pcap_analysis
import yaml
from telnetlib import Telnet
import time
import cmd_sort

# cmd_sort.sort_cmd_cisco3725(2)

"""
project_ID = '0b8c79d9-1d6e-4f46-a509-4ba26278c297'
all_link_list = [[['Cf1', '1', '1'], ['Cf3', '1', '0'], 'b2afbd14-7a33-44d1-88f5-199d4e863958'], [['Cf2', '1', '15'], ['Cl2', '0', '0'], '14ad7c2b-7a13-4115-8b6c-ef4804230225'], [['Cf1', '1', '0'], ['Cf2', '1', '1'], 'd34c3081-827d-44f2-8fd2-69c8a219e194'], [['Cl1', '0', '0'], ['Cf1', '1', '15'], 'f893f37a-4f5e-4186-ac08-250b33a311fb'], [['Cf3', '1', '15'], ['Cl3', '0', '0'], '3fdf8d76-188e-48bc-9f59-7b1367ccd1b2'], [['Cf2', '1', '0'], ['Cf3', '1', '1'], '1fd9301c-f483-424c-9334-e0381e52c628']]
vpcs_name_ip_list = [['Cl2', '192.168.1.2'], ['Cl3', '192.168.1.3'], ['Cl1', '192.168.1.1']]

pcap_analysis.l2_pcap(project_ID, all_link_list)
"""

"""
"""
with open('VERIFICATIONforNCMonGNS3/verification-tool/communication_root/test.yaml') as file:
    yml = yaml.safe_load(file)
    # print(yml[0])
    # print(yml["list"][-1])

linkfailure_point = list(yml[1].keys())[0]

#list(yml[0][linkfailure_point][j].keys())[0]

print(linkfailure_point)
print(list(list(yml[0].values())[0][1].values())[0])
print("---------------")
print(yml[0].values())
print(list(yml[0]["none"][0].keys())[0])
print(len(yml[0]["none"]))
print(list(yml[0][list(yml[0].keys())[0]][2].keys())[0])






"""

import traceroute

traceroute.traceroute(5003, "none", "before", "Cl1-Cl2", "192.168.1.2")
"""

"""
def traceroute(port):
    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))
    tn.read_until(b"~$ ", wait_time)
    tn.write(b"\n" + b"\r\n")
    tn.write(b"\n" + b"\r\n")
    tn.read_until(b">", wait_time)
    tn.write(b"ping 192.168.1.1" + b"\r\n")
    # 機器のコンフィグにコマンド実行結果が表示されるのを待つ
    time.sleep(10)
    log = tn.read_until(b">", wait_time).decode("ascii")
    tL = log.split("\n")[0:]
    for line in tL:
        print(line)
    tn.close()

traceroute(5007)


import communication_root_check

vpcs_name_ip_list = [['Cl6', '10.0.14.1'], ['Cl2', '10.0.18.2'], ['Cl8', '10.0.16.1'], ['Cl3', '10.0.11.1'], ['Cl5', '10.0.13.1'], ['Cl9', '10.0.17.1'], ['Cl7', '10.0.15.1'], ['Cl4', '10.0.12.1'], ['Cl1', '10.0.19.1']]

with open('VERIFICATIONforNCMonGNS3/verification-tool/communication_root/test_ospf.yaml') as file:
    yml = yaml.safe_load(file)

communication_root_check.test_result_l3(9, "before", yml[1], vpcs_name_ip_list)



import pyshark

root = "C:/Users/s109s/GNS3/projects/campus_stp_root/project-files/captures/"
cap = pyshark.FileCapture(root + 'linkfailure-link-Cf1-Cf2-after-capture-Cf1-Cf3.pcap', display_filter= str("icmp"))

j = 0
while True:
    if cap[j].ip.src == "192.168.1.3" and cap[j].ip.dst == "192.168.1.2":
        print(cap[j - 1])
        print(cap[j].icmp)
        break
    j += 1
"""


# with open('VERIFICATIONforNCMonGNS3/verification-tool/communication_root/test.yaml') as file:
#     yml = yaml.safe_load(file)
# 
# print(len(yml))

"""

import yaml

obj = { 'x': 'XXX', 'y': 100, 'z': [200, 300, 400] }
# x: XXX
# y: 100
# z:
# - 200
# - 300
# - 400
obj = [{"none": [{"Cl1-Cl2": ["Cl1", "Cf1", "Cf2", "Cl2"]}, {"Cl1-Cl2": ["Cl1", "Cf1", "Cf2", "Cl2"]}]}, "Cf1-Cf2", "Cf2-Cf3", "Cf3-Cf1"]
#obj2 = [
#    "none": ["Cl1-Cl2": ["Cl1", "Cf1", "Cf2", "Cl2"], "Cf1": ["Cl1", "Cf1", "Cf2", "Cl2"], "Cf2": ["Cl1", "Cf1", "Cf2", "Cl2"], "Cl2": ["Cl1", "Cf1", "Cf2", "Cl2"]]
#]
    

with open('output.yaml', 'w') as file:

    data = yaml.dump(obj, file)
    print(data)

with open('output.yaml', 'r+') as f:
    data = yaml.safe_load(f)
    print(data[0]["none"])
    # data[0]["none"] = [1, 2, 3]
    data[0]["none"].append([])
    f.seek(0)
    yaml.dump(data, f)
"""
    
# import pcap_analysis
# 
# select_list = [['Cl1', 'Cf1'], ['Cf2', 'Cf3'], ['Cf1', 'Cf3'], ['Cf2', 'Cl2']]
# new_lisr = []
# 
# print(pcap_analysis.select_root_setup(select_list, "Cl2", new_lisr))


import time_count

time_count.culcurate_time("VERIFICATIONforNCMonGNS3/verification-tool/time_count.txt")

# import shutil
# 
# yaml_file_root = 'VERIFICATIONforNCMonGNS3/verification-tool/communication_root/'
# yaml_file_name = "3Cf-3Cl-ring-ideal.yaml"
# yaml_file_name_test = yaml_file_name[:-10] + "test.yaml"
# 
# shutil.copyfile(yaml_file_root + yaml_file_name, yaml_file_root + yaml_file_name_test)


# root_ideal = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/3Cf-3Cl-ring-ideal.yaml"
# root_test = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/3Cf-3Cl-ring-test.yaml"
# 
# with open(root_ideal) as file:
#     yml_ideal = yaml.safe_load(file)
# 
# print(list(yml_ideal[0].values())[0])
# 
# print(list(yml_ideal[0].keys())[0])



import communication_root_check

communication_root_check.create_yaml("Cf1-Cf2", "Cl1-Cl3", ['Cl1', 'Cf1', 'Cf3', 'Cf2', 'Cl2'], '3Cf-3Cl-ring-test.yaml')