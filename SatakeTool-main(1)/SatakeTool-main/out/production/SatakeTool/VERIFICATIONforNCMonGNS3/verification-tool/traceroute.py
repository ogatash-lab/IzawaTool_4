from telnetlib import Telnet
import time

# 
# vpcs用のtraceroute!!!!!!!!!!!!!!!!!!!!
# 

def traceroute(port, where, when, communication_node, node2_ip):
    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))
    # linkfailure-link-"どこの機器と"-"どこの機器の間の障害？"-"障害発生前？あと？"-"communication"-"どこの機器と"-"どこの機器の通信？".txt'
    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/linkfailure-link-' + str(where) + '-' + str(when) + '-communication-' + str(communication_node) + '.txt', 'w', encoding = 'shift-jis') as f:
        # 実行する前に記載されていたコマンド履歴を消す？
        tn.read_until(b">", wait_time)
        ping_command = "ping " + node2_ip
        tn.write(str.encode(ping_command+"\n\n"))
        
        # 機器のコンフィグにコマンド実行結果が表示されるのを待つ
        time.sleep(10)
        log = tn.read_until(b"more", wait_time).decode("ascii")
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)
    tn.close()

def icmp_traceroute(port, where, when, communication_node, node2_ip):
    host = "127.0.0.1"
    wait_time = 3
    tn = Telnet(host, str(port))
    # linkfailure-link-"どこの機器と"-"どこの機器の間の障害？"-"障害発生前？あと？"-"communication"-"どこの機器と"-"どこの機器の通信？".txt'
    with open('VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/traceroute/linkfailure-link-' + str(where) + '-' + str(when) + '-communication-' + str(communication_node) + '.txt', 'w', encoding = 'shift-jis') as f:
        # 実行する前に記載されていたコマンド履歴を消す？
        tn.read_until(b">", wait_time)
        ping_command = "trace " + node2_ip + " -m 10"
        tn.write(str.encode(ping_command+"\n\n"))
        
        # 機器のコンフィグにコマンド実行結果が表示されるのを待つ
        time.sleep(10)
        log = tn.read_until(b"more", wait_time).decode("ascii")
        tL = log.split("\n")[0:]
        for line in tL:
            f.write(line)
    tn.close()