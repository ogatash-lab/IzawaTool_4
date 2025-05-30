import tool
import status_check_allcover
import subprocess
import time
import traceroute
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
all_node_name_stp_list = []
for i in range(tool.kiki_num):
    node_name_stp_list = []
    # VERIFICATIONforNCMonGNS3/を付けないから動かない？
    with open('VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/cmd_kiki/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f: # 機器設定プログラムで判断
        node_name_stp_list.append(tool.kiki_name_ID_list[i][1]) # Cf1,2,3,?
        for line in f:
            if 'spanning-tree' in line and len(node_name_stp_list) == 1:
                node_name_stp_list.append(1)
                break
        if len(node_name_stp_list) == 1:
            node_name_stp_list.append(0)
    all_node_name_stp_list.append(node_name_stp_list)

#print('all_node_name_stp_list =')
#print(all_node_name_stp_list)

# 断線させる回線の判別
# all_link_list = [['ESW1', '0', 'ESW2', '1'], ['ESW1', '1', 'ESW3', '0'], ['ESW2', '0', 'ESW3', '1']]
# all_node_name_stp_list = [['ESW1', 1], ['ESW2', 0], ['ESW3', 0]]

# 断線対象のリンクを示したリスト
ver_list = []
for i in range(len(tool.all_link_list)):
    # 互いの機器にSNSが設定されているか判断する
    vernum = 0
    for j in range(len(all_node_name_stp_list)):
        if tool.all_link_list[i][0][0] == all_node_name_stp_list[j][0]:
            vernum += all_node_name_stp_list[j][1]
            break
    for k in range(len(all_node_name_stp_list)):
        if tool.all_link_list[i][1][0] == all_node_name_stp_list[k][0]:
            vernum += all_node_name_stp_list[k][1]
    if vernum == 2:
        ver_list.append(1)
    else:
        ver_list.append(0)

#print('ver_list =')
#print(ver_list)

# all_link_listの要素とver_listの01が対応
# 対象のlinkを削除して

kaisuu = len(ver_list)
# kaisuu = 1

for i in range(kaisuu):
    if ver_list[i] == 0:
        continue
    else:
        print(' link failure link-' + str(tool.all_link_list[i][0][0]) + '-' + tool.all_link_list[i][1][0])
        # もともとの機器の状態を取得
        for j in range(tool.kiki_num):# node_nameからkiki_nameに変更
            print('     device-status-capture device-' + str(tool.kiki_name_ID_list[j][1]) + '   start..........', end='')
            status_check_allcover.status_check_stp(str(tool.kiki_name_ID_list[j][0]), int(j), 'before', int(i))
            print('complete')

        # 各クライアントの通信，通信経路をキャプチャ開始して終了まで
        # 今回はキャプチャして放置すればエンジニアが確認してくれる想定かな
        # リンクの個数(all_link_list)だけ回す
        
        time.sleep(100)
        for j in range(len(tool.all_link_list)):
            # 各リンクのキャプチャを開始する
            # 断線してる箇所のキャプチャは例外処理？
            # capture_file_name = none-cf1-cf2.pcap
            # shell = Trueにすると動かない　なぜかはしらん
            capture_file_name = "linkfailure-link-" + str(tool.all_link_list[i][0][0]) + '-' + str(tool.all_link_list[i][1][0]) + "-" + "before" + "-capture-" + str(tool.all_link_list[j][0][0]) + "-" + str(tool.all_link_list[j][1][0]) + ".pcap"
            link_ID = str(tool.all_link_list[j][2])
            # print('capture_file_name = ' + capture_file_name)
            capture_start_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + tool.project_ID + '/links/' + link_ID + '/start_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
            # print(capture_start_command)
            cp = subprocess.run(capture_start_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            # print('----------------------')

        # 各クライアント同士の疎通確認
        # name_ip_listから最初のノードを取得
        # 最初のノードに接続して、ほかのIPへping
        # 2つ目以降のノードにも繰り返す

        # vpcs_name_ip_list = 
        # [['Cl2', '192.168.1.2'], ['Cl3', '192.168.1.3'], ['Cl1', '192.168.1.1']]
        # tool.vpcs_name_ip_list

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
                    traceroute.traceroute(src_node_telport, str(tool.all_link_list[i][0][0]) + '-' + str(tool.all_link_list[i][1][0]), "before", str(src_node_name + "-" + dst_node_name), dst_node_ip)
            

        # [[node_accessport, node_name, node_id], [...]]
        # tool.vpcs_name_ID_list

        # キャプチャの終了
        for j in range(len(tool.all_link_list)):
            # 各リンクのキャプチャを開始する
            # 断線してる箇所のキャプチャは例外処理？
            # capture_file_name = none-cf1-cf2.pcap
            # shell = Trueにすると動かない　なぜかはしらん
            capture_file_name = "linkfailure-link-" + str(tool.all_link_list[i][0][0]) + '-' + str(tool.all_link_list[i][1][0]) + "-" + "before" + "-capture-" + str(tool.all_link_list[j][0][0]) + "-" + str(tool.all_link_list[j][1][0]) + ".pcap"
            link_ID = str(tool.all_link_list[j][2])
            print('capture_file_name = ' + capture_file_name)
            capture_stop_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + tool.project_ID + '/links/' + link_ID + '/stop_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
            print(capture_stop_command)
            cp = subprocess.run(capture_stop_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            print('----------------------')
        time.sleep(100)


        # リンクの削除
        print('     link-delete           link-' + str(tool.all_link_list[i][0][0]) + '-' + tool.all_link_list[i][1][0] + ' start..........', end='')
        link_delete_command = 'curl -i -X DELETE http://localhost:3080/v2/projects/' + tool.project_ID + '/links/' + str(tool.all_link_list[i][2])
        cp = subprocess.run(link_delete_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        cp.stdout
        print('complete')

        # 設定反映待ち
        print('     device-fault-handling..........')
        time.sleep(40)
        
        # リンク削除後の機器の状態取得
        for j in range(tool.kiki_num):
            print('     device-status-capture device-' + str(tool.kiki_name_ID_list[j][1]) + '   start..........', end='')
            status_check_allcover.status_check_stp(str(tool.kiki_name_ID_list[j][0]), int(j), 'after', int(i))
            print('complete')


        # 各クライアントの通信，通信経路をキャプチャ開始して終了まで
        # 各クライアントの通信，通信経路をキャプチャ開始して終了まで
        # 今回はキャプチャして放置すればエンジニアが確認してくれる想定かな
        # リンクの個数(all_link_list)だけ回す
        time.sleep(100)
        for j in range(len(tool.all_link_list)):
            # 各リンクのキャプチャを開始する

            # 断線してる箇所のキャプチャは例外処理？
            
            # capture_file_name = none-cf1-cf2.pcap
            # shell = Trueにすると動かない　なぜかはしらん
            capture_file_name = "linkfailure-link-" + str(tool.all_link_list[i][0][0]) + '-' + str(tool.all_link_list[i][1][0]) + "-" + "after" + "-capture-" + str(tool.all_link_list[j][0][0]) + "-" + str(tool.all_link_list[j][1][0]) + ".pcap"
            link_ID = str(tool.all_link_list[j][2])
            # print('capture_file_name = ' + capture_file_name)
            capture_start_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + tool.project_ID + '/links/' + link_ID + '/start_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
            # print(capture_start_command)
            cp = subprocess.run(capture_start_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            # print('----------------------')

        # 各クライアント同士の疎通確認
        # name_ip_listから最初のノードを取得
        # 最初のノードに接続して、ほかのIPへping
        # 2つ目以降のノードにも繰り返す

        # vpcs_name_ip_list = 
        # [['Cl2', '192.168.1.2'], ['Cl3', '192.168.1.3'], ['Cl1', '192.168.1.1']]
        # tool.vpcs_name_ip_list

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
                    traceroute.traceroute(src_node_telport, str(tool.all_link_list[i][0][0]) + '-' + str(tool.all_link_list[i][1][0]), "after", str(src_node_name + "-" + dst_node_name), dst_node_ip)
            

        # [[node_accessport, node_name, node_id], [...]]
        # tool.vpcs_name_ID_list

        # キャプチャの終了
        for j in range(len(tool.all_link_list)):
            # 各リンクのキャプチャを開始する
            # 断線してる箇所のキャプチャは例外処理？
            # capture_file_name = none-cf1-cf2.pcap
            # shell = Trueにすると動かない　なぜかはしらん
            capture_file_name = "linkfailure-link-" + str(tool.all_link_list[i][0][0]) + '-' + str(tool.all_link_list[i][1][0]) + "-" + "after" + "-capture-" + str(tool.all_link_list[j][0][0]) + "-" + str(tool.all_link_list[j][1][0]) + ".pcap"
            link_ID = str(tool.all_link_list[j][2])
            print('capture_file_name = ' + capture_file_name)
            capture_stop_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + tool.project_ID + '/links/' + link_ID + '/stop_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
            print(capture_stop_command)
            cp = subprocess.run(capture_stop_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            print('----------------------')
        time.sleep(100)

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