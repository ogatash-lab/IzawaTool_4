# allcoverの時にtool.pyを実行する


import subprocess
import os
import time

import cmd_sort
import pcap_analysis
import yaml

import functools
print = functools.partial(print, flush=True)

#tool実行開始
#print('tool start')

#GNS3ネットワークの構築
print('GNS3-network-generetion start')

"""
# projectの名前を入力
project_name = str(input())

# projectを作成するコマンド
project_create_command = 'curl -X POST "http://localhost:3080/v2/projects" -d "{""name"": ""' + project_name +'""}"'

# projectを作成するコマンドを実行
# cp.stdout にプロジェクトの情報
with open('project_info.txt', 'w', encoding = 'shift-jis') as f:
    cp = subprocess.run(project_create_command, shell = True, encoding = 'shift-jis', stdout = subprocess.PIPE)
    f.write(cp.stdout)

# project_ID の抽出
with open('project_info.txt', 'r', encoding = 'shift-jis') as f:
    i = 0
    for line in f:
        if i == 9:
            if 'project_id' in line:
                project_ID = str(line[19:55])
            else:
                print('project_ID_error')
            break
        else:
            i += 1
"""
#############
# project_ID = '0b8c79d9-1d6e-4f46-a509-4ba26278c297'
# stp3yaml
# project_ID = "2fdd0237-28d1-4ccf-9a61-21cbdf5cb153"
# shinshu_univ_stp
# project_ID = "c002edb3-3a94-4bc8-aac3-ca6e62540f26"
# campus_asis_m2
# project_ID = "f1ed7d6c-a66a-48c0-90ef-7bdd8de19e66"
# m2stp
project_ID = "b8d1e9ee-bc20-470e-b01a-807e5f846a9d"
#############

#print('project_ID = ' + str(project_ID))

# NetworkConfigurationのファイル数を確認
dir = 'VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/cmd_kiki'
kiki_num = sum(os.path.isfile(os.path.join(dir, name)) for name in os.listdir(dir))

#print('cmd_kiki内のファイル数 = ' + str(kiki_num))

# vpcsの個数
vpcs_num = 0
with open('VERIFICATIONforNCMonGNS3/verification-tool/NetworkConfiguration/NetworkConfigurationInformation.txt', 'r', encoding = 'shift-jis') as f:
    val = 0
    for line in f:
        if 'Cl' in line:
            val += 1
        elif val == 1:
            if 'name' in line:
                val += 1
            else:
                val = 0
        elif val == 2:
            vpcs_num += 1
            val = 0

# メタモデルの情報を取得
# node_nameを取得
'''
node_name_list =[]
for i in range(node_num):
    with open('verification-tool/NetworkConfiguration/NetworkConfigurationInformation_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
        val = 0
        for line in f:
            if 'Hn' in line:
                val = 1
            elif val == 1:
                val += 1
            elif val == 2:
                node_name = line
                node_name_list.append(node_name.replace('\n', ''))
                val += 1
            if val == 3:
                break

print('node_name_list =')
print(node_name_list)
'''
# nodeのlinkに関する情報を取得
# SW1_slot1_port15>PC1_port0
all_link_list =[]
with open('VERIFICATIONforNCMonGNS3/verification-tool/NetworkConfiguration/NetworkConfigurationInformation.txt', 'r', encoding = 'shift-jis') as f:
    val = 0
    for line in f:
        if 'Li' in line:
            val = 1
        elif val == 1:
            # ここでlink以外を弾く
            if 'description' in line:
                val += 1
            else:
                val = 0
        elif val == 2:
            link_list = []
            pos = line.find('-')
            src1 = line[:pos].split('_')
            # print(src1)
            src2 = line[pos + 1 : -1].split('_') # -1は改行をなくすため
            
            ans = src1[1]
            src1[1] = ans[4:]
            ans = src1[2]
            src1[2] = ans[4:]

            ans = src2[1]
            src2[1] = ans[4:]
            ans = src2[2]
            src2[2] = ans[4:]
            
            link_list.append(src1)
            link_list.append(src2)
            # リンクを追加
            all_link_list.append(link_list)
            # その他のリンクを探す
            val = 0

#print('all_link_list =')
#print(all_link_list)

#
#print(' device-placement start')

# vpcsの作成
for i in range(vpcs_num):
    print('     device-placement device-Cl' + str(i + 1)+ '   start..........', end='')
    vpcs_create_command = 'curl -X POST http://localhost:3080/v2/projects/' + project_ID + '/nodes -d "{""name"": ""Cl' + str(i + 1) + '"", ""node_type"": ""vpcs"", ""compute_id"": ""local""}"'
    with open('VERIFICATIONforNCMonGNS3/verification-tool/node_create_info/vpcs_create_info/vpcs_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
        cp = subprocess.run(vpcs_create_command, shell = True, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        f.write(cp.stdout)
    time.sleep(1)
    print('complete')

# kikiの作成
# ethetnet_switch
for i in range(kiki_num):
    print('     device-placement device-Cf' + str(i + 1)+ '   start..........', end='')
    kiki_create_command = 'curl http://localhost:3080/v2/projects/'+ project_ID + '/nodes -d "{""symbol"": "":/symbols/ethernet_switch.svg"", ""name"": ""Cf' + str(i + 1) + '"", ""properties"": {""platform"": ""c3725"", ""nvram"": 256, ""image"": ""c3725-ipbase-mz.123-9a.bin"", ""ram"": 128, ""slot0"": ""GT96100-FE"", ""slot1"": ""NM-16ESW""}, ""compute_id"": ""local"", ""node_type"": ""dynamips""}"'
    with open('VERIFICATIONforNCMonGNS3/verification-tool/node_create_info/kiki_create_info/kiki_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
        cp = subprocess.run(kiki_create_command, shell = True, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        f.write(cp.stdout)
    time.sleep(1)
    print('complete')



# nodeのID，名前，コンソールポートの抽出
# vpcsも追加する
# [[node_accessport, node_name, node_id], [...]]

kiki_name_ID_list = []
for i in range(kiki_num):
    with open('VERIFICATIONforNCMonGNS3/verification-tool/node_create_info/kiki_create_info/kiki_create_info_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
        j = 0
        append_list = []
        for line in f:
            if j == 3:
                if 'console' in line:
                    node_accessport = line[15:19]
                    append_list.append(node_accessport)
                    j += 1
                #else:
                #    print('error')
            elif j == 18:
                if 'name' in line:
                    node_name = line[13:-3]
                    append_list.append(node_name)
                    j += 1
                #else:
                #    print('error')
            elif j == 20:
                if 'node_id' in line:
                    node_ID = line[16:52]
                    append_list.append(node_ID)
                    kiki_name_ID_list.append(append_list)
                    break
                #else:
                #    print('error')
            else:
                j += 1

vpcs_name_ID_list = []
for i in range(vpcs_num):
    with open('VERIFICATIONforNCMonGNS3/verification-tool/node_create_info/vpcs_create_info/vpcs_create_info_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
        j = 0
        append_list = []
        for line in f:
            if j == 3:
                if 'console' in line:
                    node_accessport = line[15:19]
                    append_list.append(node_accessport)
                    j += 1
                #else:
                #    print('error')
            elif j == 18:
                if 'name' in line:
                    node_name = line[13:-3]
                    append_list.append(node_name)
                    j += 1
                #else:
                #    print('error')
            elif j == 20:
                if 'node_id' in line:
                    node_ID = line[16:52]
                    append_list.append(node_ID)
                    vpcs_name_ID_list.append(append_list)
                    break
                #else:
                #    print('error')
            else:
                j += 1

node_name_ID_list = kiki_name_ID_list + vpcs_name_ID_list
#print('node_name_ID_list = ')
#print(node_name_ID_list)

# linkの作成
# vpcs の場合adapter=0, port=つなげたい箇所
link_num = len(all_link_list)
for i in range(link_num):
    for j in range(len(node_name_ID_list)):
        if all_link_list[i][0][0] == node_name_ID_list[j][1]:
            node_name_1 = node_name_ID_list[j][1]
            node_ID_1 = node_name_ID_list[j][2]
        if all_link_list[i][1][0] == node_name_ID_list[j][1]:
            node_ID_2 = node_name_ID_list[j][2]
            node_name_2 = node_name_ID_list[j][1]
    print('     device-placement link-' + str(node_name_1) + '-' + str(node_name_2) + ' start..........', end='')
    port_1 = all_link_list[i][0][2]
    port_2 = all_link_list[i][1][2]
    slot_1 = all_link_list[i][0][1]
    slot_2 = all_link_list[i][1][1]
    link_create_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + project_ID +'/links -d "{""nodes"": [{""adapter_number"": ' + slot_1 + ', ""node_id"": ""' + node_ID_1 + '"", ""port_number"": ' + port_1 + '}, {""adapter_number"": ' + slot_2 + ', ""node_id"": ""' + node_ID_2 + '"", ""port_number"": ' + port_2 + '}]}"'
    
    with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
        cp = subprocess.run(link_create_command, shell = True, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        f.write(cp.stdout)
    print('complete')

# link_IDをall_link_listに追加する
for i in range(link_num):
    with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
        j = 0
        for line in f:
            if j == 14:
                if 'link_id' in line:
                    link_ID = line[16:52]
                    #print(link_ID)
                    all_link_list[i].append(link_ID)
                    #print(all_link_list)
                    break
                #else:
                #    print('error')
            else:
                j += 1

print('all_link_list =')
print(all_link_list)
# all_link_list = [[['Cf1', '1', '1'], ['Cf3', '1', '0'], '92992b52-0558-455d-8de9-c571f6836cc8'],

#機器配置　完了
#print(' device-placement complete')
print('GNS3-network-generation complete')

# 機器設定手順をソート
cmd_sort.sort_cmd_cisco3725(kiki_num)

# ----------------------------------------
# 機器設定コマンド
#print('機器設定プログラムの作成実行')
print('GNS3-network-configuration start')

node_num = kiki_num + vpcs_num

# nodeの起動
for i in range(node_num):
    #node_start_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + project_ID + '/nodes/' + node_name_ID_list[i][2] + '/start'
    node_start_command = ['curl', '-i', '-X', 'POST', 'http://localhost:3080/v2/projects/' + project_ID + '/nodes/' + node_name_ID_list[i][2] + '/start']
    cp = subprocess.run(node_start_command, shell = False, encoding = 'utf-8', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    cp.stdout
# 起動待ち
time.sleep(10)

# kikiへコマンド入力
for i in range(kiki_num):
    print('     device-configuration-program device-Cf' + str(i + 1) + ' start..........', end='')
    path = 'VERIFICATIONforNCMonGNS3/verification-tool/kikisettei/kikisettei_' + str(i + 1) + '.py'
    f = open(path, 'w')
    f.writelines('from telnetlib import Telnet\n')
    f.writelines('host = "127.0.0.1"\n')
    f.writelines('port = "' + str(kiki_name_ID_list[i][0]) + '"\n')
    f.writelines('wait_time = 3\n')
    f.writelines('tn = Telnet(host, port)\n')
    time.sleep(3)
    f.writelines('tn.write(b"no" + b"\\r\\n")\n')
    time.sleep(3)
    f.writelines('tn.write(b"\\n" + b"\\r\\n")\n')
    time.sleep(3)
    f.writelines('tn.read_until(b">", wait_time)\n')
    with open('VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/cmd_kiki/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f2:
        for line in f2:
            f.writelines('tn.write(b"' + str(line).replace('\n', '') + '" + b"\\r\\n")\n')
            f.writelines('tn.read_until(b"#", wait_time)\n')
    f.writelines('tn.close()\n')
    f.close()
    # 機器設定プログラム実行
    subprocess.call('python %s' % path)
    print('complete')


# vpcsへコマンド入力
# ['Cl2\n', 'ip 192.168.1.2 255.255.255.0 192.168.1.253', 'Cl1\n', 'ip 192.168.1.1 255.255.255.0 192.168.1.254', 'Cl3\n', 'ip 192.168.1.3 255.255.255.0 192.168.1.252']
vpcs_lst = []
vpcs_name_ip_list = []
with open('VERIFICATIONforNCMonGNS3/verification-tool/NetworkConfiguration/NetworkConfigurationInformation.txt', 'r', encoding = 'shift-jis') as f:
    lst = []
    lst2 = []
    val = 0
    command = 'ip '
    for line in f:
        if 'Cl' in line:
            lst.append(line[:-1])
            lst2.append(line[:-1])
            val += 1
        elif val == 1:
            if 'name' in line:
                val += 1
            else:
                lst.pop()
                lst2.pop()
                val = 0
        elif val == 2 or val == 3 or val == 5 or val == 7:
            val += 1
        elif val == 4:
            command += line[:-1] + ' '
            lst2.append(line[:-1])
            vpcs_name_ip_list.append(lst2)
            lst2 = []
            val += 1
        elif val == 6:
            command += line[:-1] + ' '
            val += 1
        elif val == 8:
            command += line[:-1]
            lst.append(command)
            vpcs_lst.append(lst)
            command = 'ip '
            lst = []
            val = 0
        
print("vpcs_name_ip_list = ")
print(vpcs_name_ip_list)

for i in range(vpcs_num):
    val = 'Cl' + str(i + 1)
    for j in range(vpcs_num):
        if val == vpcs_name_ID_list[j][1]:
            print('     device-configuration-program device-Cl' + str(i + 1) + ' start..........', end='')
            path = 'VERIFICATIONforNCMonGNS3/verification-tool/kikisettei/vpcs_' + str(i + 1) + '.py'
            f = open(path, 'w')
            f.writelines('from telnetlib import Telnet\n')
            f.writelines('host = "127.0.0.1"\n')
            f.writelines('port = "' + str(vpcs_name_ID_list[j][0]) + '"\n')
            f.writelines('wait_time = 3\n')
            f.writelines('tn = Telnet(host, port)\n')
            time.sleep(3)
            f.writelines('tn.read_until(b">", wait_time)\n')
            for k in range(vpcs_num):
                if vpcs_lst[k][0] == val:
                    f.writelines('tn.write(b"' + str(vpcs_lst[k][1]) + '" + b"\\r\\n")\n')
            f.close()
            # 機器設定プログラム実行
            subprocess.call('python %s' % path)
            print('complete')
        #else:
        #    print('error = ' + str(i) + ' ' + str(j))

#機器設定完了
#print(' device-configuration complete')

#GNS3ネットワーク自動構築　完了
print('GNS3-network-configuration complete')
#print('--------------------------------')

"""
この下に関数を呼び出す形で続ける？
一旦リンク障害の疎通確認はおいておく
新しく疎通確認用のコードを作成する
疎通する関数と、キャプチャする関数で分ける？
キャプチャは1通信で区切る
3台STPの場合、1障害6通信

link_failure.pyを2つに分ける、障害発生し状態の取得までと、復旧、この間に通信確認する
"""

# キャプチャ開始
# 障害発生させる
# クライアント通信しつつ、機器の状態を取得
# 障害を復旧させる
# キャプチャ終了
# 
# キャプチャしたpcapからsrcとdstの関係を基に経路を算出
# 通信経路を機器の名前で入力してもらい、それを基にIPに変換してから処理をする？
# 
# 
# 
# 通信経路を記入したyamlファイルを読み込む？
# yamlファイルのnoneなど障害単位で回す
# for文で障害の回数だけ回す？

"""以下網羅性保証に関係なし
with open('VERIFICATIONforNCMonGNS3/verification-tool/communication_root/test.yaml') as file:
    yml = yaml.safe_load(file)

print('yml認識')

# len(yml) - 1
for i in range(3):
    # 障害発生前
    pcap_analysis.l2_pcap(project_ID, all_link_list, vpcs_name_ip_list, yml[0], vpcs_name_ID_list, kiki_name_ID_list)
    # 障害発生後
    pcap_analysis.l2_pcap(project_ID, all_link_list, vpcs_name_ip_list, yml[i + 1], vpcs_name_ID_list, kiki_name_ID_list)

"""


