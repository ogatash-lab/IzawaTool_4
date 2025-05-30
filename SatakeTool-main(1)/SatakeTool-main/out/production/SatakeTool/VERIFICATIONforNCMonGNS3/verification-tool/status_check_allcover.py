from telnetlib import Telnet
import tool
import time

# ポート番号と機器の登録番号を入力される関数にする
def status_check_stp(port, kiki_no, when, link_no):

    # link_no のall_link_listの名前を取得

    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))

    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/sh_spanning-tree_brief/linkfailure-link-' + str(tool.all_link_list[link_no][0][0]) + '-' + str(tool.all_link_list[link_no][1][0]) + '-' + str(when) + '-' + str(tool.kiki_name_ID_list[kiki_no][1]) + '.txt', 'w', encoding = 'shift-jis') as f:
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


def status_check_ospf(port, kiki_no, when, link_no):

    # link_no のall_link_listの名前を取得

    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/' + selected_folder + '/sh_ip_ospf_interface_brief/linkfailure-link-' + str(tool.all_link_list[link_no][0][0]) + '-' + str(tool.all_link_list[link_no][1][0]) + '-' + str(when) + '-' + str(tool.kiki_name_ID_list[kiki_no][1]) + '.txt', 'w', encoding = 'shift-jis') as f:
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
        tn.write(b"show ip ospf interface brief" + b"\r\n")
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


def status_check_route(port, kiki_no, when, link_no):

    # link_no のall_link_listの名前を取得

    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/' + selected_folder + '/sh_ip_route/linkfailure-link-' + str(tool.all_link_list[link_no][0][0]) + '-' + str(tool.all_link_list[link_no][1][0]) + '-' + str(when) + '-' + str(tool.kiki_name_ID_list[kiki_no][1]) + '.txt', 'w', encoding = 'shift-jis') as f:
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
    