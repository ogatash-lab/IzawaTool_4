import os
import subprocess
import time
import functools
print = functools.partial(print, flush=True)

import cmd_sort

# vpcsの作成
def vpcs_create(i, project_id):
    print('     device-placement device-Cl' + str(i + 1)+ '   start..........', end='')
    vpcs_create_command = 'curl -X POST http://localhost:3080/v2/projects/' + project_id + '/nodes -d "{""name"": ""Cl' + str(i + 1) + '"", ""node_type"": ""vpcs"", ""compute_id"": ""local""}"'
    with open('VERIFICATIONforNCMonGNS3/verification-tool/node_create_info/vpcs_create_info/vpcs_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
        cp = subprocess.run(vpcs_create_command, shell = True, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        f.write(cp.stdout)
    time.sleep(1)
    print('complete')
    return 0

# dynamipsの作成
def dynamips_create(i, project_id):
    print('     device-placement device-Cf' + str(i + 1)+ '   start..........', end='')
    kiki_create_command = 'curl http://localhost:3080/v2/projects/'+ project_id + '/nodes -d "{""symbol"": "":/symbols/ethernet_switch.svg"", ""name"": ""Cf' + str(i + 1) + '"", ""properties"": {""platform"": ""c3725"", ""nvram"": 256, ""image"": ""c3725-adventerprisek9-mz.124-15.T14.image"", ""ram"": 128, ""slot0"": ""GT96100-FE"", ""slot1"": ""NM-16ESW""}, ""compute_id"": ""local"", ""node_type"": ""dynamips""}"'
    with open('VERIFICATIONforNCMonGNS3/verification-tool/node_create_info/kiki_create_info/kiki_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
        cp = subprocess.run(kiki_create_command, shell = True, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        f.write(cp.stdout)
    time.sleep(5)
    print('complete dynamips_create')
    return 0

# nodeのID，名前，コンソールポートの抽出
# vpcsも追加する
# [[node_accessport, node_name, node_id], [...]]
def name_id_list_create(i, kiki_type):
    name_id_list = []
    with open('VERIFICATIONforNCMonGNS3/verification-tool/node_create_info/' + kiki_type + '_create_info/' + kiki_type + '_create_info_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
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
                    # name_id_list.append(append_list)
                    break
                #else:
                #    print('error')
            else:
                j += 1
    # return name_id_list
    return append_list

# linkの作成
# vpcs の場合adapter=0, port=つなげたい箇所
# link_create_time は初めてリンクを作成する時はall_link_listに新しく追加するが、削除後に復元する時は該当のリンクを、該当のall_link_listの要素を書き換える
def link_create(i, project_id, node_name_id_list, all_link_list, link_create_time):
    node_name_1 = []
    node_name_2 = []
    node_ID_1 = []
    node_ID_2 = []
    for j in range(len(node_name_id_list)):
        print(all_link_list[i][0][0])
        print(node_name_id_list[j][1])
        if all_link_list[i][0][0] == node_name_id_list[j][1]:
            node_name_1 = node_name_id_list[j][1]
            node_ID_1 = node_name_id_list[j][2]
        if all_link_list[i][1][0] == node_name_id_list[j][1]:
            node_ID_2 = node_name_id_list[j][2]
            node_name_2 = node_name_id_list[j][1]
    print('     device-placement link-' + str(node_name_1) + '-' + str(node_name_2) + ' start..........', end='')
    port_1 = all_link_list[i][0][2]
    port_2 = all_link_list[i][1][2]
    slot_1 = all_link_list[i][0][1]
    slot_2 = all_link_list[i][1][1]
    link_create_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + project_id +'/links -d "{""nodes"": [{""adapter_number"": ' + slot_1 + ', ""node_id"": ""' + node_ID_1 + '"", ""port_number"": ' + port_1 + '}, {""adapter_number"": ' + slot_2 + ', ""node_id"": ""' + node_ID_2 + '"", ""port_number"": ' + port_2 + '}]}"'


    with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
        cp = subprocess.run(link_create_command, shell = True, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        f.write(cp.stdout)
    print('complete')

    with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
        j = 0
        for line in f:
            if j == 14:
                if 'link_id' in line:
                    link_ID = line[16:52]
                    #print(link_ID)
                    if link_create_time == "new":
                        all_link_list[i].append(link_ID)
                    if link_create_time == "renew":
                        all_link_list[i][2] = link_ID
                    #print(all_link_list)
                    break
                #else:
                #    print('error')
            else:
                j += 1
    return 0


# gns3の仮想ネットワークの構築
def gns3_network_build(project_id):
    print('GNS3-network-generetion start')

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    # NetworkConfigurationのファイル数を確認
    #dir = 'VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/cmd_kiki'
    dir = 'VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/' + selected_folder
    dynamips_num = sum(os.path.isfile(os.path.join(dir, name)) for name in os.listdir(dir))
    print("dynamips_num = " + str(dynamips_num))

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

    # nodeのlinkに関する情報を取得
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

    print("all_link_list = ")
    print(all_link_list)
    
    # vpcsの作成
    for i in range(vpcs_num):
        vpcs_create(i, project_id)
    
    # dynamipsの作成
    for i in range(dynamips_num):
        dynamips_create(i, project_id)
    
    # nodeのID，名前，コンソールポートの抽出
    # vpcsも追加する
    # [[node_accessport, node_name, node_id], [...]]
    dynamips_name_id_list = []
    for i in range(dynamips_num):
        dynamips_name_id_list.append(name_id_list_create(i, "kiki"))

    vpcs_name_id_list = []
    for i in range(vpcs_num):
        vpcs_name_id_list.append(name_id_list_create(i, "vpcs"))

    node_name_id_list = dynamips_name_id_list + vpcs_name_id_list
    print("node_name_id_list = ")
    print(node_name_id_list)

    # linkの作成
    # vpcs の場合adapter=0, port=つなげたい箇所
    link_num = len(all_link_list)
    link_create_time = "new"
    print("link_num = " + str(link_num))
    for i in range(link_num):
        link_create(i, project_id, node_name_id_list, all_link_list, link_create_time)
    
    print('all_link_list =')
    print(all_link_list)

    print('GNS3-network-generation complete')

    # 機器設定手順をソート
    cmd_sort.sort_cmd_cisco3725(dynamips_num)

    # ----------------------------------------
    # 機器設定コマンド
    print('GNS3-network-configuration start')

    node_num = dynamips_num + vpcs_num

    # nodeの起動
    for i in range(node_num):
        #node_start_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + project_ID + '/nodes/' + node_name_ID_list[i][2] + '/start'
        node_start_command = ['curl', '-i', '-X', 'POST', 'http://localhost:3080/v2/projects/' + project_id + '/nodes/' + node_name_id_list[i][2] + '/start']
        cp = subprocess.run(node_start_command, shell = False, encoding = 'utf-8', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        cp.stdout
    # 起動待ち
    time.sleep(10)

    # kikiへコマンド入力
    for i in range(dynamips_num):
        print('     device-configuration-program device-Cf' + str(i + 1) + ' start..........', end='')
        path = 'VERIFICATIONforNCMonGNS3/verification-tool/kikisettei/kikisettei_' + str(i + 1) + '.py'

        f = open(path, 'w')
        f.writelines('from telnetlib import Telnet\n')
        f.writelines('host = "127.0.0.1"\n')
        f.writelines('port = "' + str(dynamips_name_id_list[i][0]) + '"\n')
        f.writelines('wait_time = 3\n')
        f.writelines('tn = Telnet(host, port)\n')
        time.sleep(3)
        f.writelines('tn.write(b"no" + b"\\r\\n")\n')
        time.sleep(3)
        f.writelines('tn.write(b"\\n" + b"\\r\\n")\n')
        time.sleep(3)
        f.writelines('tn.read_until(b">", wait_time)\n')
        #with open('VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/cmd_kiki/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f2:
        with open('VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/' + selected_folder + '/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f2:
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

    #print("vpcs_name_ip_list = ")
    #print(vpcs_name_ip_list)

#-------------------停止箇所----------------------------------------------------------------------------
    #print("vpcs_name_id_list = ")
    #print(vpcs_name_id_list)

    for i in range(vpcs_num):
        val = 'Cl' + str(i + 1)
        for j in range(vpcs_num):
            if val == vpcs_name_id_list[j][1]:
                print('     device-configuration-program device-Cl' + str(i + 1) + ' start..........', end='')
                path = 'VERIFICATIONforNCMonGNS3/verification-tool/kikisettei/vpcs_' + str(i + 1) + '.py'

                f = open(path, 'w')
                f.writelines('from telnetlib import Telnet\n')
                f.writelines('host = "127.0.0.1"\n')
                f.writelines('port = "' + str(vpcs_name_id_list[j][0]) + '"\n')
                f.writelines('wait_time = 3\n')
                f.writelines('tn = Telnet(host, port)\n')
                time.sleep(3)
                f.writelines('tn.read_until(b">", wait_time)\n')
                for k in range(vpcs_num):
                    if vpcs_lst[k][0] == val:
                        f.writelines('tn.write(b"' + str(vpcs_lst[k][1]) + '" + b"\\r\\n")\n')
                f.close()

                # 機器設定プログラム実行
                # スクリプトの実行と出力のリアルタイム取得
                process = subprocess.Popen(['python', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # 出力のリアルタイム表示
                for line in process.stdout:
                    print(line, end='')

                # エラーのリアルタイム表示
                for line in process.stderr:
                    print(line, end='')

                # プロセスの終了を待機
                process.wait()

                # 終了ステータスの確認
                print("Exit status:", process.returncode)

    #機器設定完了
    #print(' device-configuration complete')

    #GNS3ネットワーク自動構築　完了
    print('GNS3-network-configuration complete')

    print("dynamips_num=",end="")
    print(dynamips_num)
    print("dynamips_name_id_list=",end="")
    print(dynamips_name_id_list)
    print("vpcs_name_id_list=",end="")
    print(vpcs_name_id_list)
    print("vpcs_name_ip_list=",end="")
    print(vpcs_name_ip_list)
    print("all_link_list=",end="")
    print(all_link_list)

    return dynamips_num, dynamips_name_id_list, vpcs_name_id_list, vpcs_name_ip_list, all_link_list
