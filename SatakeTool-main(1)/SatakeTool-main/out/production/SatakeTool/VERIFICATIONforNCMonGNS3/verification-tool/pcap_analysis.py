import pyshark
import subprocess
import time
import traceroute
import yaml
import status_check_stp
import link_failure_extend
import communication_root_check
import time_count

import functools
print = functools.partial(print, flush=True)

"""

root = "VERIFICATIONforNCMonGNS3/verification-tool/log_pcap/"

cap = pyshark.FileCapture(root + 'test4.pcap', display_filter= "ospf")
# print(dir(cap))


# cap = pyshark.FileCapture(root + 'blk-cf2-1.pcap', display_filter= "icmp")

# capの中身がないときの対応として、例外処理で対応する
try:
    for i in range(10):
        print('packet_num = ' + str(i + 1))
        # cap[i].show()
        # print(cap[i].highest_layer)
        print("src = " + cap[i].ip.src)
        print("dst = " + cap[i].ip.dst)
        print('--------------------------------------------------------------')
except KeyError as e:
    print(e)

print("ok")

# print(cap[0].layers)

"""


def l2_pcap(project_ID, all_link_list, vpcs_name_ip_list, yaml_dict , vpcs_name_ID_list, kiki_name_ID_list, yaml_file_name_test):
    print('l2_pcap-----------------------')

    linkfailure_point = list(yaml_dict.keys())[0]
    # 障害発生前後のどちらか確認する
    when = "before"
    if linkfailure_point != "none":
        # 障害を発生させる
        when = "after"
    
    # リンクの個数(all_link_list)だけ回す
    for i in range(len(all_link_list)):
        # 各リンクのキャプチャを開始する
        # 断線してる箇所のキャプチャは例外処理？
        # capture_file_name = none-cf1-cf2.pcap
        # shell = Trueにすると動かない　なぜかはしらん
        capture_file_name = "linkfailure-link-" + linkfailure_point + "-" + when + "-capture-" + str(all_link_list[i][0][0]) + "-" + str(all_link_list[i][1][0]) + ".pcap"
        link_ID = str(all_link_list[i][2])
        print('capture_file_name = ' + capture_file_name)
        capture_start_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + project_ID + '/links/' + link_ID + '/start_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
        print(capture_start_command)
        cp = subprocess.run(capture_start_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        print('----------------------')

    # ここで障害を発生させる
    if linkfailure_point != "none":
        # 障害を発生させる
        link_create_num = link_failure_extend.link_delete(project_ID, all_link_list, linkfailure_point)
        # 設定反映待ち
        time.sleep(40)
        # 復旧する時の手立てを返す？
    
    print("when = " + when)

    # 各クライアントを疎通する
    # 通信経路の入力から、疎通開始する機器を決定する
    # 例)Cl1 -> Cf1 -> Cf2 -> Cl2, Cl1のクライアントに接続しping Cl2 
    for i in range(len(yaml_dict[linkfailure_point])):
        communication_node = str(list(yaml_dict[linkfailure_point][i].keys())[0])
        print("communication_node = " + communication_node)
        # traceroute.traceroute(vpcs_name_ID_list[i][0], linkfailure_point, when, communication_node)
        # communication_nodeからtracerouteに必要なものを取得する
        node1_name = communication_node[:3]
        print("node1_name = " + node1_name)
        node2_name = communication_node[4:]
        print("node2_name = " + node2_name)

        # 通信元のコンソールポートを特定
        for j in range(len(vpcs_name_ID_list)):
            if node1_name == vpcs_name_ID_list[j][1]:
                node1_port = vpcs_name_ID_list[j][0]
                break

        print("node1_port = " + node1_port)

        # 通信先のIPを特定
        for j in range(len(vpcs_name_ip_list)):
            if node2_name == vpcs_name_ip_list[j][0]:
                node2_ip = vpcs_name_ip_list[j][1]
                break
        
        print("node2_ip = " + node2_ip)
        
        # 各機器の通信確認
        traceroute.traceroute(node1_port, linkfailure_point, when, communication_node, node2_ip)
        print("traceroute end")

    # ここ1回で障害発生前後のSTPのログを取得できる
    for i in range(len(kiki_name_ID_list)):
        status_check_stp.status_check_stp(kiki_name_ID_list[i][0], when, linkfailure_point, kiki_name_ID_list[i][1])
        print("status_check = " + str(i))

    # 障害対象のリンクをもとに戻す
    if linkfailure_point != "none":
        print("all_link_list_before = ")
        print(all_link_list)
        all_link_list_change_ID = link_failure_extend.link_recreate(link_create_num, all_link_list, project_ID, kiki_name_ID_list)
        all_link_list[link_create_num][2] = all_link_list_change_ID
        print("all_link_list_after = ")
        print(all_link_list)
        # 設定反映待ち
        time.sleep(40)


    # 各ネットワーク機器のポートのキャプチャを終了する
    for i in range(len(all_link_list)):
        capture_file_name = "linkfailure-link-" + linkfailure_point + "-" + when + "-capture-" + str(all_link_list[i][0][0]) + "-" + str(all_link_list[i][1][0]) + ".pcap"
        link_ID = str(all_link_list[i][2])
        capture_stop_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + project_ID + '/links/' + link_ID + '/stop_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
        print("capture_stop_command = " + capture_stop_command)
        subprocess.run(capture_stop_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    
    # pysharkにてICMPが通っている経路を確認する
    # 生成されるpcapの場所は変更できなそう
    # capture_file_pathを指定しても、想定していない、とのログが出る
    # ここでfor文で回す when とかもできる
    """
    """
    link_num = len(all_link_list)
    for i in range(len(yaml_dict[linkfailure_point])):
        dummy = l2_route_check("icmp", linkfailure_point, list(yaml_dict[linkfailure_point][i].keys())[0], list(list(yaml_dict.values())[0][i].values())[0], when, vpcs_name_ip_list, all_link_list, yaml_file_name_test)
    print('end')
    
    print("linkfailure_point = " + linkfailure_point)
    return 0


# 経路の判別には、src dstの情報が必要
# IPに関しては機器設定手順から取得する？
# vpcsに関してはvpcs_lstから取得できる
# 1経路が入力される
def l2_route_check(protocol, linkfailure_point, communication_node, communication_root, when, vpcs_name_ip_list, all_link_list, yaml_file_name_test):
    # 経路のyamlファイルからhostnameに対応するipを割り出す
    
    src_node_name = communication_node[:3]
    dst_node_name = communication_node[4:]
    for i in range(len(vpcs_name_ip_list)):
        if src_node_name == vpcs_name_ip_list[i][0]:
            src_node_ip = vpcs_name_ip_list[i][1]
        if dst_node_name == vpcs_name_ip_list[i][0]:
            dst_node_ip = vpcs_name_ip_list[i][1]
    # capture_file_pathを指定しても、想定していない、とのログが出る
    # そのためpcapファイルが作成されるファイルは手動で設定すること
    root = "C:/Users/s109s/GNS3/projects/campus_stp_root/project-files/captures/"
    # for文でpcapファイルの個数だけ回し，ICMPが通ったリンクを抽出する
    link_pass_list = []
    for i in range(len(all_link_list)):
        
        # 
        cap = pyshark.FileCapture(root + 'linkfailure-link-' + linkfailure_point + '-' + when + '-capture-' + str(all_link_list[i][0][0]) + "-" + str(all_link_list[i][1][0]) + '.pcap', display_filter= str(protocol))
        time.sleep(2)
        # capの中身がないときの対応として、例外処理で対応する
        try:
            val = 0
            for j in range(50):
                # time.sleep(1)
                # print('packet_num = ' + str(j + 1))
                # ひっくり返すことでリプライがあるかどうかを確認している
                if cap[j].ip.src == src_node_ip and cap[j].ip.dst == dst_node_ip:
                    # 取得できたパケットがno responseとかの確認した方がいいかも
                    val += 1
                    if val == 5:
                        # print('append 1')
                        link_pass_list.append(1)
                        cap.close()
                        break
                # time.sleep(1)
                
            
        except KeyError as e:
            cap.close()
            # print('append 0')
            link_pass_list.append(0)
            # time.sleep(2)
            
    print('link_pass_list =')
    print(link_pass_list)

    # link_pass_listとcommunication_rootを比較できないか
    # link_pass_listからノードを並べ替えて、communication_rootと同じリストになれば通信経路は設計通りとなる
    # all_link_listとlink_pass_listの順番が対応している

    select_list = []
    for i in range(len(link_pass_list)):
        # select_listにパケットが通過したリンクのノード関連をまとめる
        if link_pass_list[i] == 1:
            select_list.append([all_link_list[i][0][0], all_link_list[i][1][0]])

    print('select_list = ')
    print(select_list)

    # 再帰的にノードを並べなおす？
    new_list = []
    link_pass_name_list = select_root_setup(select_list, src_node_name, new_list)
    print('link_pass_name_list = ')
    print(link_pass_name_list)

    # yamlファイルにまとめる
    communication_root_check.create_yaml(linkfailure_point, communication_node, link_pass_name_list, yaml_file_name_test)


# select_list = [['Cf2', 'Cl2'], ['Cf3', 'Cl3'], ['Cf2', 'Cf3']] を修正する
def select_root_setup(select_root, start_node, new_list):
    try:
        for i in range(len(select_root)):
            if start_node in select_root[i]:
                select_root[i].remove(start_node)
                new_list.append(start_node)
                start_node = select_root[i][0]
                if len(select_root) == 1:
                    new_list.append(start_node)
                    print("break")
                    print(new_list)
                    break
                else:
                    del select_root[i]
                    print(new_list)
                    print('再帰')
                    select_root_setup(select_root, start_node, new_list)
    except IndexError as e:
        print('error')
        pass
    return new_list
        

    