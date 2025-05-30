import tool
import status_check_allcover
import subprocess
import time
import traceroute
import communication_root_check
import yaml

import functools
print = functools.partial(print, flush=True)

print('GNS3-network-simulation start')

# 0と1でSNSがあるか示す
# hostnameとSNSがあるかだけメモ
# link_listのhostnameを比べる
'''
namelistにSNSがあるやつを01を追加する
断線させる前に，各機器の状態を取得しておく
'''
#冗長箇所の特定
#print('joutyoukasho-tokutei')

# SNSがある機器には1，ない機器には0
all_node_name_ospf_list = []
for i in range(tool.kiki_num):
    node_name_ospf_list = []
    # VERIFICATIONforNCMonGNS3/を付けないから動かない？
    with open('VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/cmd_kiki/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f: # 機器設定プログラムで判断
        node_name_ospf_list.append(tool.kiki_name_ID_list[i][1])
        for line in f:
            if "ospf" in line and len(node_name_ospf_list) == 1:
                node_name_ospf_list.append(1)
                break
        if len(node_name_ospf_list) == 1:
            node_name_ospf_list.append(0)
    all_node_name_ospf_list.append(node_name_ospf_list)

#print('all_node_name_stp_list =')
#print(all_node_name_stp_list)

# 断線させる回線の判別
# all_link_list = [['ESW1', '0', 'ESW2', '1'], ['ESW1', '1', 'ESW3', '0'], ['ESW2', '0', 'ESW3', '1']]
# all_node_name_stp_list = [['ESW1', 1], ['ESW2', 0], ['ESW3', 0]]

# 断線対象のリンクを示したリスト
ospf_target_list = []
for i in range(len(tool.all_link_list)):
    # 互いの機器にOSPFが設定されているか判断する
    ospf_num = 0
    for j in range(len(all_node_name_ospf_list)):
        if tool.all_link_list[i][0][0] == all_node_name_ospf_list[j][0]:
            ospf_num += all_node_name_ospf_list[j][1]
    for k in range(len(all_node_name_ospf_list)):
        if tool.all_link_list[i][1][0] == all_node_name_ospf_list[k][0]:
            ospf_num += all_node_name_ospf_list[k][1]
    if ospf_num == 2:
        ospf_target_list.append(1)
    else:
        ospf_target_list.append(0)

#print('ver_list =')
#print(ver_list)

# all_link_listの要素とver_listの01が対応
# 対象のlinkを削除して

kaisuu = len(ospf_target_list)
# kaisuu = 1

for i in range(kaisuu):
    if ospf_target_list[i] == 0:
        continue
    else:
        # 通信経路を取得
        for j in range(len(tool.vpcs_name_ip_list)):
            src_node_name = tool.vpcs_name_ip_list[j][0]
            for k in range(len(tool.vpcs_name_ID_list)):
                if tool.vpcs_name_ip_list[j][0] == tool.vpcs_name_ID_list[k][1]:
                    # 送信元のtelnet接続用ポートを取得
                    src_node_telport = tool.vpcs_name_ID_list[k][0]
                    print("src_node_telport = ")
                    print(src_node_telport)
                    break
            for l in range(len(tool.vpcs_name_ip_list)):
                if src_node_name != tool.vpcs_name_ip_list[l][0]:
                    dst_node_name = tool.vpcs_name_ip_list[l][0]
                    dst_node_ip = tool.vpcs_name_ip_list[l][1]
                    print("traceroute start")
                    traceroute.icmp_traceroute(src_node_telport, str(tool.all_link_list[i][0][0]) + '-' + str(tool.all_link_list[i][1][0]), "before", str(src_node_name + "-" + dst_node_name), dst_node_ip)
            

        print(' link failure link-' + str(tool.all_link_list[i][0][0]) + '-' + tool.all_link_list[i][1][0])
        # もともとの機器の状態を取得
        for j in range(tool.kiki_num):# node_nameからkiki_nameに変更
            print('     device-status-capture device-' + str(tool.kiki_name_ID_list[j][1]) + '   start..........', end='')
            status_check_allcover.status_check_ospf(str(tool.kiki_name_ID_list[j][0]), int(j), 'before', int(i))
            # status_check_allcover.status_check_route(str(tool.kiki_name_ID_list[j][0]), int(j), 'after', int(i))
            print('complete')

        # リンクの削除
        print('     link-delete           link-' + str(tool.all_link_list[i][0][0]) + '-' + tool.all_link_list[i][1][0] + ' start..........', end='')
        link_delete_command = 'curl -i -X DELETE http://localhost:3080/v2/projects/' + tool.project_ID + '/links/' + str(tool.all_link_list[i][2])
        cp = subprocess.run(link_delete_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        cp.stdout
        print('complete')

        # 設定反映待ち
        print('     device-fault-handling..........')
        time.sleep(40)

        # 通信経路を取得
        for j in range(len(tool.vpcs_name_ip_list)):
            src_node_name = tool.vpcs_name_ip_list[j][0]
            for k in range(len(tool.vpcs_name_ID_list)):
                if tool.vpcs_name_ip_list[j][0] == tool.vpcs_name_ID_list[k][1]:
                    # 送信元のtelnet接続用ポートを取得
                    src_node_telport = tool.vpcs_name_ID_list[k][0]
                    print("src_node_telport = ")
                    print(src_node_telport)
                    break
            for l in range(len(tool.vpcs_name_ip_list)):
                if src_node_name != tool.vpcs_name_ip_list[l][0]:
                    dst_node_name = tool.vpcs_name_ip_list[l][0]
                    dst_node_ip = tool.vpcs_name_ip_list[l][1]
                    print("traceroute start")
                    traceroute.icmp_traceroute(src_node_telport, str(tool.all_link_list[i][0][0]) + '-' + str(tool.all_link_list[i][1][0]), "after", str(src_node_name + "-" + dst_node_name), dst_node_ip)
            
        
        # リンク削除後の機器の状態取得
        for j in range(tool.kiki_num):
            print('     device-status-capture device-' + str(tool.kiki_name_ID_list[j][1]) + '   start..........', end='')
            status_check_allcover.status_check_ospf(str(tool.kiki_name_ID_list[j][0]), int(j), 'after', int(i))
            # status_check_allcover.status_check_route(str(tool.kiki_name_ID_list[j][0]), int(j), 'after', int(i))
            print('complete')

        # linkの復旧
        for j in range(tool.kiki_num):
            if tool.all_link_list[i][0][0] == tool.kiki_name_ID_list[j][1]:
                node_ID_1 = tool.kiki_name_ID_list[j][2]
            if tool.all_link_list[i][1][0] == tool.kiki_name_ID_list[j][1]:
                node_ID_2 = tool.kiki_name_ID_list[j][2]

        link_create_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + tool.project_ID +'/links -d "{""nodes"": [{""adapter_number"": ' + tool.all_link_list[i][0][1] + ', ""node_id"": ""' + str(node_ID_1) + '"", ""port_number"": ' + tool.all_link_list[i][0][2] + '}, {""adapter_number"": ' + tool.all_link_list[i][1][1] + ', ""node_id"": ""' + str(node_ID_2) + '"", ""port_number"": ' + tool.all_link_list[i][1][2] + '}]}"'
        with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
            cp = subprocess.run(link_create_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            f.write(cp.stdout)
        with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
            j = 0
            for line in f:
                if j == 14:
                    if 'link_id' in line:
                        link_ID = line[16:52]
                        #print(link_ID)
                        tool.all_link_list[i][2] = link_ID
                        #print(tool.all_link_list)
                        break
                    #else:
                    #    print('error')
                else:
                    j += 1

        # 設定反映待ち
        time.sleep(40)

print('GNS3-network-simulation complete')

# 試験結果の出力
"""
with open('VERIFICATIONforNCMonGNS3/verification-tool/communication_root/test_ospf.yaml') as file:
    yml = yaml.safe_load(file)

for i in range(1):
    communication_root_check.test_result_l3(9, "before", yml[1], tool.vpcs_name_ip_list)
"""
