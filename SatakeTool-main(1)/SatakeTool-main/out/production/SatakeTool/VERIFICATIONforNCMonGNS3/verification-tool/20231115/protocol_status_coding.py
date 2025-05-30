# 取得した機器の挙動を、検証結果として出力するための整形をする
import os
import time
import yaml
import pyshark
import re

import functools
print = functools.partial(print, flush=True)

# pcapから
def communication_route_l2(folder_path, pcap_file_list, linkfailure_point, crd_section, crd_model, all_link_list, vpcs_name_ip_list, protocol, crd_linkfailure_point_list):
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

    # yamlファイルへの追記
    def create_yaml(protocol, crd_model, link_pass_name_list, crd_section):
        with open(crd_model, 'r+') as f:
            data = yaml.safe_load(f)
            # この時点ですでにSTPの何かしら記述されている場合は変更しない
            try:
                print(data[linkfailure_point]["communication-route"])
            except:
                data.update({linkfailure_point: {"communication-route": {}}})
            f.seek(0)
            f.truncate()
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            print("--------------------------")

        with open(crd_model, 'r+') as f:
            data = yaml.safe_load(f)
            #リンク障害を発生させる場所と検証するPC間に関する記述を空にする
            data[linkfailure_point]["communication-route"].update({crd_section: {}})
            #空にしたディクショナリ内にlink_pass_name_listを追加
            data[linkfailure_point]["communication-route"][crd_section].update({protocol: link_pass_name_list})
            f.seek(0)
            #ファイルの内容を全て削除する
            f.truncate()
            #変更を書き出す
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            print("OK")

        return 0

    #main
    #---------------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------------

    #crd_linkfailure_point_list = ['Cf2-Cf3', 'Cf2-Cf9', 'Cf3-Cf4', 'Cf4-Cf5', 'Cf5-Cf6', 'Cf6-Cf7', 'Cf7-Cf8', 'Cf8-Cf9', 'none']

    src_node_name = crd_section.split("-")[0] #通信を行う２つのPCのうち送信側
    dst_node_name = crd_section.split("-")[1] #通信を行う２つのPCのうち受信側

    print("src = " + str(src_node_name))
    print("dst = " + str(dst_node_name))

    for i in range(len(vpcs_name_ip_list)): #PCの名前とそのipアドレスが格納されている２次元配列
        if src_node_name == vpcs_name_ip_list[i][0]:
            src_node_ip = vpcs_name_ip_list[i][1] #検証する送信側のPCのipアドレス取得
        if dst_node_name == vpcs_name_ip_list[i][0]:
            dst_node_ip = vpcs_name_ip_list[i][1] #検証する受信側のPCのipアドレス取得
    
    print("src = " + str(src_node_ip))
    print("dst = " + str(dst_node_ip))
    
    when = "after"
    if linkfailure_point == "none":
        when = "before"
        # pcap_file_list の正規表現で何とかする

    link_pass_list = []
    for i in range(len(all_link_list)):
        print("1. link_pass_list = ")
        print(link_pass_list)
        # captureフォルダ内に"linkfailure-link-none-
        text = folder_path + 'linkfailure-link-' + linkfailure_point + '-' + when + '-capture-' + str(all_link_list[i][0][0]) + "-" + str(all_link_list[i][1][0]) + '.pcap'
        
        # この下でtextを書き換えよかな
        if linkfailure_point == "none":
            pre = crd_linkfailure_point_list.copy()
            print("pre = ")
            print(pre)
            pre.remove("none")
            text = text.replace("none", pre[0]) #フォルダ名を変更

        # linkfailure_pointと同じ個所のpcapファイルを開くときは必ずそのリンクを通っていないので0
        # textの末尾15文字の中にlinkfailure_pointが含まれているか
        if linkfailure_point in text[-15:]:
            link_pass_list.append(0)
            print("2. link_pass_list = ")
            print(link_pass_list)
            continue
        # 反転
        reverse = linkfailure_point.split("-")
        if (linkfailure_point != "none") and ((reverse[1] + "-" + reverse[0]) in text[-15:]):
            link_pass_list.append(0)
            print("append 0")
            continue
        
        try:
            #pyshark の FileCapture 関数を使用して、textで指定されたファイルからパケットをキャプチャします。
            #display_filter 引数を使って、特定の送信元IP(ip.src)と宛先IP(ip.dst)に基づいたフィルタリングを行います。
            cap = pyshark.FileCapture(text, display_filter= "ip.src == " + str(src_node_ip) + " and ip.capturedst == " + str(dst_node_ip))
            print("Pyshark_FileCapture")
            time.sleep(2)
        except FileNotFoundError as e:
            link_pass_list.append(0)
            print("FILE_NOT_FOUND_ERROR")
            continue
        
        # capの中身がないときの対応として、例外処理で対応する
        try:
            val = 0
            for j in range(1500000):
                # ひっくり返すことでリプライがあるかどうかを確認している
                #パケットの送信元IPアドレスが src_node_ip で、宛先IPアドレスが dst_node_ip と一致するかどうかをチェック
                if cap[j].ip.src == src_node_ip and cap[j].ip.dst == dst_node_ip:
                    # 取得できたパケットがno responseとかの確認した方がいいかも
                    val += 1
                    if val == 5:
                        # パケットの番号とか取得して，それで並び替えてもいいかも
                        link_pass_list.append(1) #成功したリンクパスを記録
                        print("link_pass_list = ")
                        print(link_pass_list)
                        cap.close()
                        break
        # range()の数だけのパケットがなければkeyerrorになって処理してる
        except KeyError as e:
            cap.close()
            link_pass_list.append(0)
            print("KEY_ERROR")
            print("link_pass_list = ")
            print(link_pass_list)
            
    print('link_pass_list =')
    print(link_pass_list)

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

    create_yaml(protocol, crd_model, link_pass_name_list, crd_section)
    time.sleep(10)

    return 0
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

def communication_route_l3(crd_name, vpcs_name_ip_list, crd_model, protocol):

    def create_yaml(communication_node_list, linkfailure_point, crd_section, crd_model, protocol):
        with open(crd_model, 'r+') as f:
            data = yaml.safe_load(f)
            # この時点ですでにSTPの何かしら記述されている場合は処理を飛ばす
            try:
                print(data[linkfailure_point]["communication-route"])
            except:
                data.update({linkfailure_point: {"communication-route": {}}})
            f.seek(0)
            f.truncate()
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            print("--------------------------")

        with open(crd_model, 'r+') as f:
            data = yaml.safe_load(f)
            data[linkfailure_point]["communication-route"].update({crd_section: {}})
            data[linkfailure_point]["communication-route"][crd_section].update({protocol: communication_node_list})
            f.seek(0)
            f.truncate()
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            #print("OK")

        return 0

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    # ipとdynamipsの対応をリスト化する
    dynamps_ip_list = [] #[[Cf1, [192.168., 192.168.]], [Cf2, [192., 192.]], ...]
    dir = 'VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/' + selected_folder
    #ディレクトリ内のファイル数取得
    kiki_num = sum(os.path.isfile(os.path.join(dir, name)) for name in os.listdir(dir))
    # cmd_node/cmd_kikiのファイルを開いてIPを取得する
    for i in range(kiki_num):
        append_dynamps_ip_list = ["Cf" + str(i + 1)]
        append_ip_list = []
        with open(dir + '/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f_type: #cmd_kiki_Cfファイルを開く
            for line in f_type:
                if "ip address" in line: #"ip address"が含まれている行を取り出す
                    # print("IPの抽出")
                    # print(line.split()[2])
                    append_ip_list.append(line.split()[2])
        append_dynamps_ip_list.append(append_ip_list)
        dynamps_ip_list.append(append_dynamps_ip_list)
    #print(dynamps_ip_list)

    # linkfailure_point, section
    # tracerouteファイルをすべて回すのではなく，指定したファイルを回す
    with open(crd_model, 'r+') as f:
        data = yaml.safe_load(f)
        crd_linkfailure_point_list = list(data.keys()) #yamlのトップレベルのキー（断線箇所）を取り出す
    #print("crd_linkfailure_point_list",end="")
    #print(crd_linkfailure_point_list)

    with open(crd_model, 'r+') as f:
        data = yaml.safe_load(f)
        for val in crd_linkfailure_point_list:
            crd_section_list = list(data[val]["communication-route"].keys())
    # print(crd_section_list)

    pre_lst = crd_linkfailure_point_list.copy()
    pre_lst.remove("none")

    for linkfailure_point in crd_linkfailure_point_list:
        for crd_section in crd_section_list:
            # 最初に通信区間の最初のノードを加えたい
            communication_node_list = [list(crd_section.split("-"))[0]]

            # print(linkfailure_point)
            # print(crd_section)
            when = "after"
            pos = linkfailure_point
            if linkfailure_point == "none":
                when = "before"
                # pos = pre_lst[1] #元
                pos = "none"
                # linkfailure_point を適当なやつに入れ替える
                #continue

            text = "VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/" + selected_folder + "/traceroute/linkfailure-link-" + pos +"-" + when + "-communication-" + crd_section + ".txt"
            try:
                with open(text) as f:
                    before_pass_node_name = ""
                    for line in f:
                        """
                        # このlineにIPアドレスが含まれている場合、それがどのノードのIPなのか確認する
                        # lineからIPアドレスを取り出して、dynamips_ip_listと比較した方がいいかな
                        if line.count(".") >= 4:
                            # lineの整形
                            line = line.replace("\n", "")
                            line_list = list(line.split(" "))
                            # filterでリスト内の空文字を取り除く
                            line_list_val = list(filter(None, line_list))
                            # check ここで「.」が３つあるものをipとして抽出するようにする
                            pass_node_ip = line_list_val[1]
                            # 最後に到達したノードのログは *10.0.18.2 みたいになる
                            # check 必ず上記の表示になるわけではないため，＊をすべて取り除くように処理する必要がある

                            while "*" in pass_node_ip:  #伊澤変更　*が２つのときも取り除く
                                pass_node_ip = pass_node_ip[1:]
                                #print("!!!!!!!!!!!!!!!!!!!!!!!!!    ",end="")
                                #print(pass_node_ip)
                            """
                        if line.count(".") >= 4:
                            # lineの整形
                            line = line.strip()
                            line_list = line.split(" ")
                            # 空文字を取り除く
                            line_list_val = list(filter(None, line_list))

                            # IPアドレスを含む要素を抽出
                            for item in line_list_val:
                                # "*"を取り除く
                                item_clean = item.replace("*", "")
                                # IPアドレスかどうかを確認
                                parts = item_clean.split(".")
                                if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                                    pass_node_ip = item_clean
                                    print(f"extracted IP address: {pass_node_ip}")
                                    break  # 最初に見つかったIPアドレスで処理を終了

                            for j in range(len(dynamps_ip_list)):
                                if pass_node_ip in dynamps_ip_list[j][1]:
                                    pass_node_name = dynamps_ip_list[j][0]
                                    #print(pass_node_ip + " : " + str(dynamps_ip_list[j][1]))
                            # 該当のリストの番号から-1すればいい
                            for k in range(len(vpcs_name_ip_list)):
                                if pass_node_ip == vpcs_name_ip_list[k][1]:
                                    pass_node_name = vpcs_name_ip_list[k][0]
                                    #print(pass_node_ip + " : " + str(vpcs_name_ip_list[k][1]))
                            # print('pass_node_name = ' + pass_node_name)

                            #print("pass_node_ip:" + pass_node_ip)
                            # pass_node_name を追加してく
                            # 最初に通信区間の最初のノードを加えたい
                            if(before_pass_node_name != pass_node_name): #追加
                                if(pass_node_name == "???"):
                                    pass_node_name = pass_node_ip
                                communication_node_list.append(pass_node_name)
                            before_pass_node_name = pass_node_name #追加

                            pass_node_name = "???"
            except FileNotFoundError:
                print("FILE_NOT_FOUND!!!!")
                communication_node_list = ["file error"]
            
            # print(communication_node_list)
            print("-----------------------------")

            create_yaml(communication_node_list, linkfailure_point, crd_section, crd_model, protocol)

    return 0

# vlan num, port status, root bridge を取得する
def stp(file_name, crd_model):

    # rootブリッジがどれであるか抽出する
    # 3個先のMACアドレスと8個先のMACアドレスを比較して、一致したらルートブリッジである
    # 次に最初のリストの値がaddressになるときにその値をsh得すればおけ
    def root_node_get(i, span_status_list):
        lst = []
        for j in range(i, i + 10):
            if span_status_list[j][0] == "Address":
                print(span_status_list[j])
                lst.append(span_status_list[j][1])
        if lst[0] == lst[1]:
            root_bridge = True
        else:
            root_bridge = False
        return root_bridge
    
    # 各ポートの状態を抽出する
    def port_status_get(i, span_status_list):
        lst = []
        for j in range(i + 1, len(span_status_list)):
            if "FastEthernet" in span_status_list[j][0]:
                print(span_status_list[j])
                lst.append([span_status_list[j][0], span_status_list[j][4]])
            # 次のVLANが表示されたらbreak
            elif "VLAN" in span_status_list[j][0]:
                break
        return lst

    file_path = "VERIFICATIONforNCMonGNS3/verification-tool//linkfailure-log/sh_spanning-tree_brief/"

    # file_nameを分解して、どの障害点のどの機器の設定か取得する？
    # 以下のように値を返せばいい　yamlを作成すればいい
    # example = {"vlan10": {"root_bridge": False, "port_status": [["FastEthernet1/0", "BLK"], ["FastEthernet1/0", "BLK"]]}}

    # file_name からどこで障害が起きたのか確認する
    # この時点でyamlに書き込んでおく linkfailure_point: {"stp": {}}
    if "after" in file_name:
        val = list(file_name.split("-"))
        linkfailure_point = val[2] + "-" + val[3]
    else:
        linkfailure_point = "none"
        kiki = file_name.split("-")[-1][:-4]
        print("kiki = " + kiki)

    with open(crd_model, 'r+') as f:
        data = yaml.safe_load(f)
        # この時点ですでにSTPの何かしら記述されている場合は処理を飛ばす
        try:
            print(data[linkfailure_point]["stp"])
            
            # 毎回noneの内容を書き換えちゃうことの防止
            # これだと
            if linkfailure_point == "none" and (kiki in list(data[linkfailure_point]["stp"].keys())):
                # print(data[linkfailure_point]["stp"][kiki])
                return 0
        except:
            data[linkfailure_point].update({"stp": {}})
        f.seek(0)
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    # file_name からどの機器の状態なのか取得する
    node_name = list(file_name.split("-"))[-1][:-4]

    with open(crd_model, 'r+') as f:
        data = yaml.safe_load(f)
        data[linkfailure_point]["stp"].update({node_name: {}})
        f.seek(0)
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    # stpの状態をリストにして取得している
    span_status_list = []
    with open(file_path + file_name, "r", encoding="shift-jis") as f:
        for line in f:
            line = line.replace("\n", "")
            line_list = list(line.split(" "))
            # filterでリスト内の空文字を取り除く
            line_list_val = list(filter(None, line_list))
            if len(line_list_val) != 0:
                span_status_list.append(line_list_val)


    for i in range(len(span_status_list)):
        if "VLAN" in span_status_list[i][0]:
            root_bridge = root_node_get(i, span_status_list)
            port_status = port_status_get(i, span_status_list)

            # yamlに追記する
            with open(crd_model, 'r+') as f:
                data = yaml.safe_load(f)
                
                data[linkfailure_point]["stp"][node_name].update({span_status_list[i][0]: {}})
                data[linkfailure_point]["stp"][node_name][span_status_list[i][0]].update({"root_bridge": root_bridge, "port_status": port_status})

                f.seek(0)
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    
    return 0

# 
### ospfに関して############################################################################
# # sh ip ospf neighbor でDR，BDRを取得しよかな
def ospf(file_name, crd_model):

    #機器の状態を保存したファイルの内容をリストに変換したものを引数にとり
    #リスト内に"vl"という記述があるものを抽出し戻り値とする関数　具体的には[Interface][Area][State]のみ抽出
    def status_get(ospf_status_list):
        append_lst = []
        for i in range(2, len(ospf_status_list) - 1):
            if "Vl" in ospf_status_list[i][0]:
                vlan = ospf_status_list[i][0].replace("Vl", "VLAN")
                lst = [vlan, ospf_status_list[i][2], ospf_status_list[i][5]]
                append_lst.append(lst)
            elif "VL" in ospf_status_list[i][0]: #追加
                vlan = ospf_status_list[i][0].replace("VL", "VLAN")
                lst = [vlan, ospf_status_list[i][2], ospf_status_list[i][5]]
                append_lst.append(lst)
        return append_lst

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    #機器の状態を保存したファイルがあるフォルダへのパス
    file_path = "VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/" + selected_folder + "/sh_ip_ospf_interface_brief/"
    # linkfailure_point, kiki の名前を取得
    if "after" in file_name: #リンク障害発生後の状態であったら
        val = list(file_name.split("-"))
        linkfailure_point = val[2] + "-" + val[3] #ファイル名からリンク障害発生箇所抽出
    else:
        linkfailure_point = "none"
        kiki = file_name.split("-")[-1][:-4] #どの機器の状態が保存されているのかを抽出
        #print("kiki = " + kiki)

    # "ospf"というキーが存在しているか？なければ作成するだけ
    with open(crd_model, 'r+') as f:
        data = yaml.safe_load(f)
        try:
            print("data[linkfailure_point][\"ospf\"]=",end="")
            print(data[linkfailure_point]["ospf"])
            # 毎回noneの内容を書き換えちゃうことの防止
            # これだと
            """
            if linkfailure_point == "none" and (kiki in list(data[linkfailure_point]["ospf"].keys())):
                # print(data[linkfailure_point]["stp"][kiki])
                return 0
            """
        except:
            data[linkfailure_point].update({"ospf": {}})
        f.seek(0)
        f.truncate()
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    # file_name からどの機器の状態なのか取得する
    node_name = list(file_name.split("-"))[-1][:-4]

    #ospfキーの要素に、状態を取得した機器の名前を追加
    with open(crd_model, 'r+') as f:
        data = yaml.safe_load(f)
        data[linkfailure_point]["ospf"].update({node_name: []})
        f.seek(0)
        f.truncate()
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    # ospfの状態をリストにして取得している
    ospf_status_list = []
    with open(file_path + file_name, "r", encoding="shift-jis") as f: #機器の状態を保存したファイルを開く
        for line in f:
            line = line.replace("\n", "")
            line_list = list(line.split(" "))
            # filterでリスト内の空文字を取り除く
            line_list_val = list(filter(None, line_list))
            if len(line_list_val) != 0:
                ospf_status_list.append(line_list_val)
    #print("ospf_status_list:"+file_name+"= ",end="")
    #print(ospf_status_list)

    #"ospf_status_list"から[Interface][Area][State]のみ抽出したもの
    append_lst = status_get(ospf_status_list) #"vl"という記述があれば"VLAN"に置き換え
    #print("append_lst= ",end="")
    #print(append_lst)

    with open(crd_model, "r+") as f:
        data = yaml.safe_load(f)
        for val in append_lst:
            data[linkfailure_point]["ospf"][node_name].append(val)
        f.seek(0)
        f.truncate()
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    return 0


### ルーティングテーブルに関して############################################################################
def route_table(file_name, crd_model):

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    #機器の状態を保存したファイルがあるフォルダへのパス
    file_path = "VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/" + selected_folder + "/sh_ip_route/"
    # linkfailure_point, kiki の名前を取得
    if "after" in file_name: #リンク障害発生後の状態であったら
        val = list(file_name.split("-"))
        linkfailure_point = val[2] + "-" + val[3] #ファイル名からリンク障害発生箇所抽出
    else:
        linkfailure_point = "none"
        kiki = file_name.split("-")[-1][:-4] #どの機器の状態が保存されているのかを抽出
        #print("kiki = " + kiki)

    # "routing_table"というキーが存在しているか？なければ作成するだけ
    with open(crd_model, 'r+') as f:
        data = yaml.safe_load(f)
        try:
            print("data[linkfailure_point][\"routing_table\"]=",end="")
            print(data[linkfailure_point]["routing_table"])
            # 毎回noneの内容を書き換えちゃうことの防止
            # これだと
            """
            if linkfailure_point == "none" and (kiki in list(data[linkfailure_point]["ospf"].keys())):
                # print(data[linkfailure_point]["stp"][kiki])
                return 0
            """
        except:
            data[linkfailure_point].update({"routing_table": {}})
        f.seek(0)
        f.truncate()
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    # file_name からどの機器の状態なのか取得する
    node_name = list(file_name.split("-"))[-1][:-4]

    #ospfキーの要素に、状態を取得した機器の名前を追加
    with open(crd_model, 'r+') as f:
        data = yaml.safe_load(f)
        data[linkfailure_point]["routing_table"].update({node_name: []})
        f.seek(0)
        f.truncate()
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    ospf_status_list = []

    # OSPF関連のコードパターン（O, OIA, O E1, O E2 など）
    ospf_codes = ['O', 'O IA', 'O E1', 'O E2', 'O N1', 'O N2', 'O IA', 'O E1', 'O E2']

    # 正規表現パターンの定義
    # 例: O E2    10.0.11.0 [110/20] via 10.0.4.1, 00:07:36, Vlan40
    route_pattern = re.compile(
        r'^(O(?:\s+(?:IA|E1|E2|N1|N2))?)\s+'  # OSPFコード
        r'(\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?)\s+'  # 宛先ネットワーク
        r'\[\d+/\d+\]\s+'  # メトリック（無視）
        r'via\s+(\d{1,3}(?:\.\d{1,3}){3}),\s+'  # 次ホップ
        r'\d{2}:\d{2}:\d{2},\s+'  # 時間（無視）
        r'(\S+)'  # 出力インターフェース
    )

    with open(file_path + file_name, 'r', encoding='shift-jis') as file:
        for line in file:
            line = line.strip()

            # OSPFルート行のみを対象とする
            if line.startswith('O'):
                match = route_pattern.match(line)
                if match:
                    ospf_code = match.group(1)
                    destination = match.group(2)
                    next_hop = match.group(3)
                    outgoing_interface = match.group(4)

                    # リストに追加
                    ospf_status_list.append([destination, next_hop, outgoing_interface])
                else:
                    # 複数のルートが記載されている場合（複数の次ホップがある場合）
                    # 例:
                    # O IA    10.0.2.0 [110/30] via 10.0.5.2, 00:06:51, Vlan50
                    #                  [110/30] via 10.0.4.1, 00:07:23, Vlan40
                    if '[' in line and 'via' in line:
                        # 継続行として扱う
                        match_cont = re.search(r'via\s+(\d{1,3}(?:\.\d{1,3}){3}),\s+\d{2}:\d{2}:\d{2},\s+(\S+)', line)
                        if match_cont:
                            next_hop = match_cont.group(1)
                            outgoing_interface = match_cont.group(2)
                            # 直前の宛先ネットワークを取得
                            if ospf_status_list:
                                destination = ospf_status_list[-1][0]
                                ospf_status_list.append([destination, next_hop, outgoing_interface])

    with open(crd_model, "r+") as f:
        data = yaml.safe_load(f)
        for val in ospf_status_list:
            data[linkfailure_point]["routing_table"][node_name].append(val)
        f.seek(0)
        f.truncate()
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    return 0


#########################################################################################################


def ip_route(file_name):
    # file_nameを分解して、どの障害点のどの機器の設定か取得する？
    linkfailure_point = file_name[:]
    

    file_path = ""
    ip_route_list = []
    with open(file_path + file_name, "r", encoding="shift-jis") as f:
        for line in f:
            line = line.replace("\n", "")
            line_list = list(line.split(" "))
            # filterでリスト内の空文字を取り除く
            line_list_val = list(filter(None, line_list))
            if len(line_list_val) != 0:
                ip_route_list.append(line_list_val)
        
        print(ip_route_list[10:])

    return 0


# お試し

# stp
# linkfailure_point のみでもyamlに記載しておく
# none = "none"
# with open('write_sample.yaml', 'r+') as f:
#     data = {none: None}
#     yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
# 
# file_name = "linkfailure-link-Cf2-Cf3-before-Cf1.txt"
# stp(file_name)

# ip route
# file_name = "linkfailure-link-Cf1-Cf2-after-Cf2.txt"
# ip_route(file_name)
