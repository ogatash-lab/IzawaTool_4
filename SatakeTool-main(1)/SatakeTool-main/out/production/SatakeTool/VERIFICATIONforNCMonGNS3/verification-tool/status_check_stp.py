from telnetlib import Telnet
import time

# ポート番号と機器の登録番号を入力される関数にする
def status_check_stp(port, when, linkfailure_point, capture_node_name):

    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))

    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/linkfailure-link-' + linkfailure_point + '-' + when + '-' + capture_node_name + '-stp.txt', 'w', encoding = 'shift-jis') as f:
        # 'verification-tool/dansen_log/dansen_link_' + str(link_no) + '_' + str(when) + '_' + str(kiki_no) + '.txt'
        # sh spanを実行する前に記載されていたコマンド履歴を消す？
        tn.write(b"terminal length 0" + b"\r\n")
        tn.read_until(b"~$ ", wait_time)
        tn.write(b"\n" + b"\r\n")
        tn.write(b"\n" + b"\r\n")
        tn.read_until(b"#", wait_time)
        tn.write(b"sh spanning-tree brief" + b"\r\n")
        # 機器のコンフィグにコマンド実行結果が表示されるのを待つ
        time.sleep(10)
        log = tn.read_until(b"more", wait_time).decode("ascii")
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)
    tn.close()

