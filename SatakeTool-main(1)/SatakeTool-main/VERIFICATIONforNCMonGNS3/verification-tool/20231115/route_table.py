from telnetlib import Telnet
import time

# 
# vpcs用のtraceroute!!!!!!!!!!!!!!!!!!!!
#
def route_table(port, where, when, communication_node, node2_ip):
    host = "127.0.0.1"
    tn = Telnet(host, port)
    log = ""

    # Telnet セッションの初期化
    tn.read_until(b">", timeout=5)  # 初期プロンプトをクリア
    ping_command = "show ip route"
    tn.write(ping_command.encode('ascii') + b"\n")  # コマンド実行

    # コマンドの実行結果をすべて読み取る
    output = ""
    while True:
        try:
            chunk = tn.read_until(b">", timeout=5).decode('ascii')
            output += chunk
            if ">" in chunk:
                break
        except EOFError:
            break

    tn.close()

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    # ログファイルへの書き込み
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/' + selected_folder + '/traceroute/linkfailure-link-' + str(where) + '-' + str(when) + '-route_table-' + str(communication_node) + '.txt'
    with open(filename, 'w', encoding='shift-jis') as f:
        #f.write(output)
        tl = output.split("\n")[0:]
        for line in tl:
            f.write(line)

"""
def icmp_traceroute(port, where, when, communication_node, node2_ip):
    host = "127.0.0.1"
    max_retries = 3  # 最大再試行回数
    retries = 0
    log = ""
    is_retry = True
    while is_retry:
        try:
            tn = Telnet(host, port)  # ポート番号はint型であるべき
            tn.read_until(b">", timeout=3)  # 初期プロンプトをクリア

            ping_command = f"trace {node2_ip} -m 10"
            tn.write(ping_command.encode('ascii') + b"\n")  # コマンド実行

            log = ""
            consecutive_stars = 0
            while True:
                line = tn.read_until(b"\n", timeout=5).decode('ascii')  # 各行を読む
                log += line
                if '*  *  *' in line:
                    consecutive_stars += 1

                if '>' in line:  # '>' プロンプトまたは特定の文字列が現れたら終了
                    is_retry = False  # 通常の終了の場合は再試行しない
                    tn.close()
                    break

            if retries >= max_retries:
                is_retry = False

        except Exception as e:
            log = f"エラーが発生しました: {str(e)}"
            retries = max_retries  # エラー発生時は再試行しない

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    # ログファイルへの書き込み
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/' + selected_folder + '/traceroute/linkfailure-link-' + str(where) + '-' + str(when) + '-communication-' + str(communication_node) + '.txt'
    with open(filename, 'w', encoding='shift-jis') as f:
        f.write("retries:"+str(retries))
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)   
"""


"""高速ver
def icmp_traceroute(port, where, when, communication_node, node2_ip):
    host = "127.0.0.1"
    tn = Telnet(host, str(port))
    log = ""

    tn.read_until(b">", timeout=3)  # 初期プロンプトをクリア
    ping_command = "trace " + node2_ip + " -m 10"
    tn.write(ping_command.encode('ascii') + b"\n") #コマンド実行

    while True:
        line = tn.read_until(b"\n", timeout=5).decode('ascii')  # 各行を読む
        log += line
        if '>' in line:  # '>' プロンプトまたは特定の文字列が現れたら終了
            break
    tn.close()

    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/traceroute/linkfailure-link-' + str(where) + '-' + str(when) + '-communication-' + str(communication_node) + '.txt', 'w', encoding = 'shift-jis') as f:
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)
"""

"""佐竹ver
def icmp_traceroute(port, where, when, communication_node, node2_ip):
    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))
    #linkfailure-log/traceroute/にトレースルートの結果をテキストファイルに保存（生成）
    # linkfailure-link-"どこの機器と"-"どこの機器の間の障害？"-"障害発生前？あと？"-"communication"-"どこの機器と"-"どこの機器の通信？".txt'
    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/traceroute/linkfailure-link-' + str(where) + '-' + str(when) + '-communication-' + str(communication_node) + '.txt', 'w', encoding = 'shift-jis') as f:
        # 実行する前に記載されていたコマンド履歴を消す？
        tn.read_until(b">", wait_time)
        ping_command = "trace " + node2_ip + " -m 10"
        #トレースルートコマンドをTelnetセッションに送信
        tn.write(str.encode(ping_command+"\n\n"))
        
        # 機器のコンフィグにコマンド実行結果が表示されるのを待つ
        time.sleep(20)
        log = tn.read_until(b"more", wait_time).decode("ascii") #トレースルートの結果を読み取り
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)
    tn.close()
"""