from telnetlib import Telnet
import time

# ポート番号と機器の登録番号を入力される関数にする
def status_check_stp(port, kiki_no, when, link_no, all_link_list, dynamips_name_id_list):

    # link_no のall_link_listの名前を取得

    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))

    if when == "before":
        text = 'VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/sh_spanning-tree_brief/linkfailure-link-' + "none" + '-' + str(when) + '-' + str(dynamips_name_id_list[kiki_no][1]) + '.txt'
    else:
        text = 'VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/sh_spanning-tree_brief/linkfailure-link-' + str(all_link_list[link_no][0][0]) + '-' + str(all_link_list[link_no][1][0]) + '-' + str(when) + '-' + str(dynamips_name_id_list[kiki_no][1]) + '.txt'
    with open(text, 'w', encoding = 'shift-jis') as f:
        # 'verification-tool/dansen_log/dansen_link_' + str(link_no) + '_' + str(when) + '_' + str(kiki_no) + '.txt'
        # sh spanを実行する前に記載されていたコマンド履歴を消す？
        # tn.write(b"terminal length 0" + b"\r\n")
        tn.read_until(b"~$ ", wait_time)
        tn.write(b"\n" + b"\r\n")
        tn.write(b"\n" + b"\r\n")
        tn.read_until(b"#", wait_time)
        tn.write(b"enable" + b"\r\n")
        tn.read_until(b"#", wait_time)
        tn.write(b"terminal length 0" + b"\r\n")
        tn.read_until(b"#", wait_time)
        tn.write(b"sh spanning-tree brief" + b"\r\n")
        # 機器のコンフィグにコマンド実行結果が表示されるのを待つ
        time.sleep(20)
        log = tn.read_until(b"more", wait_time).decode("ascii")
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)
    tn.close()

"""
port：選択中のルータのポート番号
kiki_no：ルータの番号０～９
when="before"
link_no=選択中のリンク番号
all_link_list：全てのリンク
dynamips_name_id_list
"""
def status_check_ospf(port, kiki_no, when, link_no, all_link_list, dynamips_name_id_list):

    # link_no のall_link_listの名前を取得

    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))

    tn.read_until(b"~$ ", wait_time)
    tn.write(b"\n" + b"\r\n")
    tn.write(b"\n" + b"\r\n")
    tn.read_until(b"#", wait_time)
    tn.write(b"enable" + b"\r\n")
    tn.read_until(b"#", wait_time)
    tn.write(b"terminal length 0" + b"\r\n")
    tn.read_until(b"#", wait_time)

    tn.read_until(b"#", wait_time)
    tn.write(b"show ip ospf interface brief" + b"\r\n")

    #linkfailure-log/traceroute/にトレースルートの結果をテキストファイルに保存（生成）
    # linkfailure-link-"どこの機器と"-"どこの機器の間の障害？"-"障害発生前？あと？"-"communication"-"どこの機器と"-"どこの機器の通信？".txt'
    log = ""
    while True:
        line = tn.read_until(b"\n", timeout=5).decode('ascii')  # 各行を読む
        log += line
        if '#' in line:  # '>' プロンプトまたは特定の文字列が現れたら終了
            break
    tn.close()

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    #キャプチャファイル作成　linkfailure-link-Cf8-Cf9-before-Cf1.txt
    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/' + selected_folder + '/sh_ip_ospf_interface_brief/linkfailure-link-' + str(all_link_list[link_no][0][0]) + '-' + str(all_link_list[link_no][1][0]) + '-' + str(when) + '-' + str(dynamips_name_id_list[kiki_no][1]) + '.txt', 'w', encoding = 'shift-jis') as f:
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)

def route_table_check_ospf(port, kiki_no, when, link_no, all_link_list, dynamips_name_id_list):

    # link_no のall_link_listの名前を取得

    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))

    tn.read_until(b"~$ ", wait_time)
    tn.write(b"\n" + b"\r\n")
    tn.write(b"\n" + b"\r\n")
    tn.read_until(b"#", wait_time)
    tn.write(b"enable" + b"\r\n")
    tn.read_until(b"#", wait_time)
    tn.write(b"terminal length 0" + b"\r\n")
    tn.read_until(b"#", wait_time)

    tn.read_until(b"#", wait_time)
    tn.write(b"show ip route" + b"\r\n")

    #linkfailure-log/traceroute/にトレースルートの結果をテキストファイルに保存（生成）
    # linkfailure-link-"どこの機器と"-"どこの機器の間の障害？"-"障害発生前？あと？"-"communication"-"どこの機器と"-"どこの機器の通信？".txt'
    log = ""
    while True:
        line = tn.read_until(b"\n", timeout=5).decode('ascii')  # 各行を読む
        log += line
        if '#' in line:  # '>' プロンプトまたは特定の文字列が現れたら終了
            break
    tn.close()

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    #キャプチャファイル作成　linkfailure-link-Cf8-Cf9-before-Cf1.txt
    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/' + selected_folder + '/sh_ip_route/linkfailure-link-' + str(all_link_list[link_no][0][0]) + '-' + str(all_link_list[link_no][1][0]) + '-' + str(when) + '-' + str(dynamips_name_id_list[kiki_no][1]) + '.txt', 'w', encoding = 'shift-jis') as f:
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)

def status_check_route(port, kiki_no, when, link_no, all_link_list, dynamips_name_id_list):

    # link_no のall_link_listの名前を取得

    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))

    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/sh_ip_route/linkfailure-link-' + str(all_link_list[link_no][0][0]) + '-' + str(all_link_list[link_no][1][0]) + '-' + str(when) + '-' + str(dynamips_name_id_list[kiki_no][1]) + '.txt', 'w', encoding = 'shift-jis') as f:
        # 'verification-tool/dansen_log/dansen_link_' + str(link_no) + '_' + str(when) + '_' + str(kiki_no) + '.txt'
        # sh spanを実行する前に記載されていたコマンド履歴を消す？
        tn.read_until(b"~$ ", wait_time)
        tn.write(b"\n" + b"\r\n")
        tn.write(b"\n" + b"\r\n")
        tn.read_until(b"#", wait_time)
        tn.write(b"enable" + b"\r\n")
        tn.read_until(b"#", wait_time)
        tn.write(b"terminal length 0" + b"\r\n")
        tn.read_until(b"#", wait_time)
        tn.write(b"show ip route" + b"\r\n")
        # 機器のコンフィグにコマンド実行結果が表示されるのを待つ
        time.sleep(20)
        # tn.read_until(b"#", wait_time)
        # tn.write(b"terminal length 0" + b"\r\n")
        # tn.read_until(b"#", wait_time)
        # tn.write(b"show ip ospf neighbor" + b"\r\n")
        # time.sleep(20)
        log = tn.read_until(b"more", wait_time).decode("ascii")
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)
    tn.close()
    