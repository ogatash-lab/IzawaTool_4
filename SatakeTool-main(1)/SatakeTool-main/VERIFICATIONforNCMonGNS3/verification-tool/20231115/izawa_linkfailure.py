import status_check_allcover
import subprocess
import time
import traceroute
import threading
import functools
print = functools.partial(print, flush=True)

def ospf(project_id, dynamips_num, dynamips_name_id_list, vpcs_name_id_list, vpcs_name_ip_list, all_link_list):

    def run_traceroute_with_lock(port, where, when, communication_node, node2_ip, lock):
        with lock:
            traceroute.icmp_traceroute(port, where, when, communication_node, node2_ip)

    time.sleep(20)

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
                    print("traceroute start linkfailure-link-none-before-"+str(src_node_name + "-" + dst_node_name))

                    lock = vpcs_port_locks[src_node_telport]

                    # スレッドを作成してトレースルートを並列実行
                    thread = threading.Thread(
                        target=run_traceroute_with_lock,
                        args=(src_node_telport, "none", "before", f"{src_node_name}-{dst_node_name}", dst_node_ip, lock)
                    )
                    thread.start()
                    threads.append(thread)
                else:
                    print(f"Telnetポートが見つかりませんでした: {src_node_name}")

        # すべてのスレッドが終了するまで待機
        for thread in threads:
            thread.join()

    # リンク削除後の機器の状態取得
    for j in range(dynamips_num):
        print('     device-status-capture device-' + str(dynamips_name_id_list[j][1]) + '   start..........', end='')

        # スレッドを作成してトレースルートを並列実行
        thread = threading.Thread(
            target=status_check_allcover.status_check_ospf,
            args=(str(dynamips_name_id_list[j][0]), int(j), 'before', int(j), all_link_list, dynamips_name_id_list)
        )
        thread.start()
        threads.append(thread)
        print('complete')
    # すべてのスレッドが終了するまで待機
    for thread in threads:
        thread.join()

    print('GNS3-network-simulation complete')

    return 0