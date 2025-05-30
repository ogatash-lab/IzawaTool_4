import threading
import time
from telnetlib import Telnet

# icmp_traceroute 関数の定義
def icmp_traceroute(port, where, when, communication_node, node2_ip):
    host = "127.0.0.1"
    tn = Telnet(host, port)
    log = ""

    # Telnet セッションの初期化
    tn.read_until(b">", timeout=5)  # 初期プロンプトをクリア
    ping_command = "trace " + node2_ip + " -m 10"
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

    # ログファイルへの書き込み
    filename = 'test_txt/linkfailure-link-' + str(where) + '-' + str(when) + '-communication-' + str(communication_node) + '.txt'
    with open(filename, 'w', encoding='shift-jis') as f:
        #f.write(output)
        tl = output.split("\n")[0:]
        for line in tl:
            f.write(line)

        # トレースルートをロック付きで実行する関数
def run_traceroute_with_lock(port, where, when, communication_node, node2_ip, lock):
    with lock:
        icmp_traceroute(port, where, when, communication_node, node2_ip)

# メインのコード
if __name__ == "__main__":
    # 処理開始時間を記録
    start_time = time.time()

    dynamips_num=9
    dynamips_name_id_list=[['5018', 'Cf1', 'b4a03300-b72c-43e6-b578-8d950cec826a'], ['5019', 'Cf2', 'acaa1875-c71c-4d3b-baa3-154fd7b9be0d'], ['5020', 'Cf3', 'e974bb96-06b5-4258-8b81-f2c6b8ebfa83'], ['5021', 'Cf4', '7ccbf70a-f802-4795-8f27-083900335265'], ['5022', 'Cf5', 'f2e4caa2-bce0-4887-98af-77a5de2afe1b'], ['5023', 'Cf6', '70bcf06d-d33a-4f49-9159-1684927f7279'], ['5024', 'Cf7', '76c69863-b876-4e98-a420-ace5b6675518'], ['5025', 'Cf8', '8cc66ad6-90df-4237-9cc4-44fa06f0a20b'], ['5026', 'Cf9', '056bb06b-643f-4f3b-bd4d-ba63b2bc920c']]
    vpcs_name_id_list=[['5000', 'Cl1', 'd50eb754-9b49-4e1f-835c-97baac410ff5'], ['5002', 'Cl2', '7703830a-e66b-4bd1-9277-fa3ad03e3c91'], ['5004', 'Cl3', '60535735-492f-4085-8e5a-4d6c26f036ff'], ['5006', 'Cl4', 'a6dbf0b7-18f2-4698-b9af-bfec65db307e'], ['5008', 'Cl5', 'fbfa64aa-4c41-412c-8870-12d466ba2a02'], ['5010', 'Cl6', 'e5d26340-133b-4e4b-a475-3535a6acf80d'], ['5012', 'Cl7', 'a52c53e8-f3c5-420d-a9d6-26e3543e3523'], ['5014', 'Cl8', 'cb3206c0-131f-45f3-9f19-a65f3c815994'], ['5016', 'Cl9', 'a42f24b5-53a1-4c63-8583-5e636a38da17']]
    vpcs_name_ip_list=[['Cl9', '10.0.17.1'], ['Cl1', '10.0.19.1'], ['Cl2', '10.0.18.2'], ['Cl8', '10.0.16.1'], ['Cl7', '10.0.15.1'], ['Cl5', '10.0.13.1'], ['Cl3', '10.0.11.1'], ['Cl4', '10.0.12.1'], ['Cl6', '10.0.14.1']]
    all_link_list=[[['Cf2', '1', '10'], ['Cf6', '1', '10'], '68dd1ede-6f22-4206-8675-68dab91d14ef'], [['Cl9', '0', '0'], ['Cf9', '1', '15'], 'd79ba7bf-e230-41ec-be75-156f6e09fd1d'], [['Cf3', '1', '4'], ['Cf4', '1', '4'], 'ea16e471-e32a-42e6-b703-16db49893e4f'], [['Cl3', '0', '0'], ['Cf3', '1', '15'], 'f5de132e-0fc0-4e76-8a6f-4241a6c39178'], [['Cl1', '0', '0'], ['Cf1', '1', '15'], '79ac0adc-08af-4fd4-bed1-f6bb4af28ab0'], [['Cl7', '0', '0'], ['Cf7', '1', '15'], 'c1a1c1a0-ab4f-4575-933a-f3b925ca16d3'], [['Cf8', '1', '9'], ['Cf9', '1', '9'], '9384b192-08ad-4dc3-9e3f-401095687dd2'], [['Cf1', '1', '2'], ['Cf2', '1', '2'], '0a0abc6f-2f4a-4733-93db-761499466035'], [['Cf2', '1', '4'], ['Cf9', '1', '4'], '13aa049d-1a32-4163-a559-50f4d93f80d1'], [['Cl2', '0', '0'], ['Cf2', '1', '15'], '61bbb556-e4d0-4edc-989b-88e065616ab6'], [['Cl8', '0', '0'], ['Cf8', '1', '15'], '30a2d649-7274-4792-b34d-175e86295b71'], [['Cl6', '0', '0'], ['Cf6', '1', '15'], 'ce458ddd-0086-45ef-bba5-63df4d0bac56'], [['Cf5', '1', '6'], ['Cf6', '1', '6'], '657065f2-b376-4c85-992f-440c5580c063'], [['Cl5', '0', '0'], ['Cf5', '1', '15'], '8ec5bdc1-b819-47c8-bed3-4087dfedc039'], [['Cf7', '1', '8'], ['Cf8', '1', '8'], '12d655ef-c22e-4e77-86fa-b297cfdd6bc1'], [['Cf4', '1', '5'], ['Cf5', '1', '5'], '95aa5d70-0270-4a0f-a09f-f503946f0bbb'], [['Cf6', '1', '7'], ['Cf7', '1', '7'], '5f0ec003-b199-4367-830e-9e04bc22cd52'], [['Cf2', '1', '3'], ['Cf3', '1', '3'], 'f7aae866-db59-4394-95f1-6f7724d7fcf4'], [['Cl4', '0', '0'], ['Cf4', '1', '15'], '4a4f0005-e7e8-40ba-ab86-f90774ff7754']]


    # VPCS名からTelnetポートへのマッピングを作成
    vpcs_name_to_port = {entry[1]: entry[0] for entry in vpcs_name_id_list}

    # VPCSポートごとのロックを作成
    vpcs_port_locks = {port: threading.Lock() for port in vpcs_name_to_port.values()}

    # リンク障害発生後　通信経路を取得
    for j in range(len(vpcs_name_ip_list)):  # 受信先VPCSごとに繰り返し
        dst_node_name = vpcs_name_ip_list[j][0]  # 受信先の端末名
        dst_node_ip = vpcs_name_ip_list[j][1]    # 受信先IPアドレス

        threads = []  # スレッドリストを初期化

        for k in range(len(vpcs_name_ip_list)):  # 送信元VPCSごとに繰り返し
            if vpcs_name_ip_list[k][0] != dst_node_name:  # 受信先と異なる場合
                src_node_name = vpcs_name_ip_list[k][0]  # 送信元の端末名
                src_node_ip = vpcs_name_ip_list[k][1]    # 送信元IPアドレス

                src_node_telport = vpcs_name_to_port.get(src_node_name)  # 送信元のTelnetポートを取得

                if src_node_telport:
                    print(f"traceroute start linkfailure-link-AAA-after-{src_node_name}-{dst_node_name}")

                    lock = vpcs_port_locks[src_node_telport]

                    # スレッドを作成してトレースルートを並列実行
                    thread = threading.Thread(
                        target=run_traceroute_with_lock,
                        args=(src_node_telport, "AAA", "after", f"{src_node_name}-{dst_node_name}", dst_node_ip, lock)
                    )
                    thread.start()
                    threads.append(thread)
                else:
                    print(f"Telnetポートが見つかりませんでした: {src_node_name}")

        # すべてのスレッドが終了するまで待機
        for thread in threads:
            thread.join()

    # 処理終了時間を記録
    end_time = time.time()

    # 実行時間を計算
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
