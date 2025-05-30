"""
yamlファイルに該当するtracerouteの結果であるか確認すればいい
vpcs_ip_listのほかにルーターに設定したIPのリストを作成する必要がある
"""

### 出力例
# linkfailure-link-Cf4-Cf5-before-communication-Cl1-Cl7
#
# trace 10.0.15.1
# trace to 10.0.15.1, 8 hops max, press Ctrl+C to stop
#  1   10.0.19.2   15.205 ms  15.326 ms  15.299 ms
#  2   10.0.1.1   45.537 ms  45.467 ms  45.548 ms
#  3   10.0.9.2   75.785 ms  76.002 ms  75.510 ms
#  4   10.0.8.2   105.928 ms  105.359 ms  105.499 ms
#  5   10.0.7.2   135.731 ms  136.284 ms  136.150 ms
#  6     *  *  *
#  7   *10.0.15.1   150.817 ms (ICMP type:3, code:3, Destination port unreachable)
# 
# 
# VPCS> 

import yaml
import shutil
import time_count

def root_simulation_l3():
    return 0

def test_result_l3(kiki_num, when, yaml_dict, vpcs_name_ip_list):
    # IPとルーターを対応させる
    dynamps_ip_list = []
    dir = 'VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/cmd_kiki'
    # cmd_node/cmd_kikiのファイルを開いてIPを取得する
    # [[Cf1, [192.168., 192.168.]], [Cf2, [192., 192.]], ...]
    for i in range(kiki_num):
        append_dynamps_ip_list = ["Cf" + str(i + 1)]
        append_ip_list = []
        with open(dir + '/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f_type:
            for line in f_type:
                if "ip address" in line:
                    # print("IPの抽出")
                    # print(line.split()[2])
                    append_ip_list.append(line.split()[2])
        append_dynamps_ip_list.append(append_ip_list)
        dynamps_ip_list.append(append_dynamps_ip_list)
    print(dynamps_ip_list)

    # 対象のtracerouteファイルを開く
    # ipの順序にcf1などを並び替える
    # 1行に含まれるIPアドレスを取得すればいいかな

    linkfailure_point = list(yaml_dict.keys())[0]
    print(list(yaml_dict[linkfailure_point][0].keys())[0])
    print(len(yaml_dict[linkfailure_point]))

    for i in range(len(yaml_dict[linkfailure_point])):
        communication_node = list(yaml_dict[linkfailure_point][i].keys())[0]
        # with open("VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/linkfailure-link-" + linkfailure_point + "-" + when + "-communication-" + str(communication_node) + ".txt") as f:
        with open("VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/linkfailure-link-Cf2-Cf3-" + when + "-communication-" + str(communication_node) + ".txt") as f:
            for line in f:
                # このlineにIPアドレスが含まれている場合、それがどのノードのIPなのか確認する
                # lineからIPアドレスを取り出して、dynamips_ip_listと比較した方がいいかな
                if line.count(".") >= 4:
                    pass_node_ip = line.split(" ")[4]
                    # 最後に到達したノードのログは *10.0.18.2 みたいになる
                    if "*" in pass_node_ip:
                        pass_node_ip = pass_node_ip[1:]
                    print(pass_node_ip)
                    
                    for j in range(len(dynamps_ip_list)):
                        if pass_node_ip in dynamps_ip_list[j][1]:
                            pass_node_name = dynamps_ip_list[j][0]
                    # 該当のリストの番号から-1すればいい
                    for k in range(len(vpcs_name_ip_list)):
                        if pass_node_ip == vpcs_name_ip_list[k][1]:
                            pass_node_name = vpcs_name_ip_list[k][0]
                    print('pass_node_name = ' + pass_node_name)

        print('-------------------------')

    # これがyamlと等しいか判定
    # とりあえずyamlと同じ表示にして、試験結果の表示はyamlと同じ処理で修正できるようにする
    """ これでシミュレーション結果のamlファイルを作成する
    import yaml

    obj = { 'x': 'XXX', 'y': 100, 'z': [200, 300, 400] }
    with open('output.yaml', 'w') as file:
        yaml.dump(obj, file)
    """
    return 0

# 追記してく感じがいいかな
def create_yaml(linkfailure_point, communication_node, link_name_pass_list, yaml_file_name_test):
    # 書き込むyamlファイルにlinkfailure_pointがなければ書く、あればそこに追記する
    # obj = [{linkfailure_point: []}]
    # obj = [{"none": [{"Cl1-Cl2": ["Cl1", "Cf1", "Cf2", "Cl2"]}, {"Cl1-Cl2": ["Cl1", "Cf1", "Cf2", "Cl2"]}]}, "Cf1-Cf2", "Cf2-Cf3", "Cf3-Cf1"]
    yaml_file_root = 'VERIFICATIONforNCMonGNS3/verification-tool/communication_root/'
    print('create yaml')

    with open(yaml_file_root + yaml_file_name_test, 'r+') as f:
        data = yaml.safe_load(f)
        # print(len(data))
        # print(data[1][linkfailure_point][1][communication_node])
        # print("linkfailure_point = " + linkfailure_point)
        # print("communication_node = " + communication_node)
        # data[0][linkfailure_point].append([{communication_node: link_name_pass_list}])
        # data[0][linkfailure_point] = {communication_node: link_name_pass_list}

        # yamlの-を行頭につけないと動かない
        # for 文回してkeyerrorで飛ばす？
        for i in range(len(data)):
            for j in range(6):
                try:
                    print(data[i][linkfailure_point][j][communication_node])
                    data[i][linkfailure_point][j][communication_node] = link_name_pass_list
                except KeyError as e:
                    continue
        # data[0][linkfailure_point][str(communication_node)] = link_name_pass_list
        
        print('ok')
        f.seek(0)
        yaml.dump(data, f)
    # time_count.count_stop("VERIFICATIONforNCMonGNS3/verification-tool/time_count.txt")
