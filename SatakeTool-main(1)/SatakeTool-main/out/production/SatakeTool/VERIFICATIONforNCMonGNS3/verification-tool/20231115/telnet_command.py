import time
import threading
from telnetlib import Telnet

def execute_telnet_command(command, filepath, port):
    host = "127.0.0.1"
    wait_time = 3

    # Telnet セッションの開始
    tn = Telnet(host, port)
    tn.read_until(b">", wait_time)
    tn.write(str.encode(command + "\n"))
    # コマンドの実行結果が表示されるのを待つ
    time.sleep(10)

    # コマンドの実行結果をすべて読み取る
    log = tn.read_very_eager().decode("ascii")
    tL = log.split("\n")
    with open(filepath, 'w', encoding='shift-jis') as f:
        for line in tL:
            f.write(line)
    # Telnet セッションの終了
    tn.close()

ping_commands = ["trace 10.0.15.1 -m 10", "trace 10.0.16.1 -m 10", "trace 10.0.17.1 -m 10"]
filepaths = ['aaa.txt', 'bbb.txt', 'ccc.txt']
ports = [5000, 5002, 5004]  # 各コマンドに対応するポート

threads = []
for i in range(len(ping_commands)):
    thread = threading.Thread(target=execute_telnet_command, args=(ping_commands[i], filepaths[i], ports[i]))
    thread.start()
    threads.append(thread)

# すべてのスレッドが終了するまで待機
for thread in threads:
    thread.join()
