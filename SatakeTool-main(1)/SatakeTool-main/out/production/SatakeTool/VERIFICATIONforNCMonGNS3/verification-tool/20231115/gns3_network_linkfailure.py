import status_check_allcover
import subprocess
import time
import traceroute
import route_table
import threading

import functools
print = functools.partial(print, flush=True)

"""引数
dynamips_name_id_list=[['5018', 'Cf1', 'ce8a08ae-2e93-4224-b84b-1a276d4f433e'], ['5019', 'Cf2', 'e1eb69f6-1ffd-4872-96ec-757c480eabad'], ['5020', 'Cf3', 'bf3e8f5b-dba4-440f-ae99-0a687fd3d7de'], ['5021', 'Cf4', '5f9beffe-0dd4-493b-9587-287782ac926e'], ['5022', 'Cf5', '2e67279f-c70b-45f9-902e-d02388df83ea'], ['5023', 'Cf6', '6f5de95f-69b1-44e6-863e-6f18ce4887d9'], ['5024', 'Cf7', 'ecc29f49-07d1-494e-812c-4b750ce550db'], ['5025', 'Cf8', '8bcc6671-423c-4b22-b215-a73aa9737a2b'], ['5026', 'Cf9', 'b82cc5f6-66f3-469b-bdef-b8f95948d15a']]
vpcs_name_id_list=[['5000', 'Cl1', 'd86464a5-0b92-4796-9428-f838b4ce5f9e'], ['5002', 'Cl2', 'c8b4cbfa-8de6-49ce-a299-9e2e2eaec870'], ['5004', 'Cl3', '6e6d81d7-622b-4a96-b327-4f34758d9bbe'], ['5006', 'Cl4', '490cfce3-6c88-4eeb-bf04-1804a76313f9'], ['5008', 'Cl5', 'f7c663cf-1068-401c-b9d8-d72a741f798f'], ['5010', 'Cl6', 'c9a213b0-657e-424f-b5dc-7375baa0245e'], ['5012', 'Cl7', '5d57c6e0-29c2-43f4-8654-9c803a6105bd'], ['5014', 'Cl8', '6d2e3543-00cf-4baa-baec-9241255938ed'], ['5016', 'Cl9', '648eaacd-3dbe-4d69-8b02-fc8a9f66867d']]
vpcs_name_ip_list=[['Cl9', '10.0.17.1'], ['Cl7', '10.0.15.1'], ['Cl3', '10.0.11.1'], ['Cl2', '10.0.18.2'], ['Cl1', '10.0.19.1'], ['Cl5', '10.0.13.1'], ['Cl6', '10.0.14.1'], ['Cl4', '10.0.12.1'], ['Cl8', '10.0.16.1']]
all_link_list=[
[['Cl7', '0', '0'], ['Cf7', '1', '15'], 'f41cda2c-ddf8-43ac-ac01-fa32a4faf0d5'], 
[['Cl5', '0', '0'], ['Cf5', '1', '15'], '714785cc-00b3-4d70-bd90-7a545fe60f8d'],
[['Cl2', '0', '0'], ['Cf2', '1', '15'], '338dca35-f7b6-4cb8-903d-570a37e481c7'], 
[['Cf8', '1', '9'], ['Cf9', '1', '9'], 'dbcb809a-f86b-4248-99e9-7176981b6196'], 
[['Cl3', '0', '0'], ['Cf3', '1', '15'], 'eefdc142-464b-42b2-9f88-f2562951bcca'], 
[['Cf6', '1', '7'], ['Cf7', '1', '7'], '60b8ad7c-b813-4bd9-bd71-2f942a2e5c8d'], 
[['Cf4', '1', '5'], ['Cf5', '1', '5'], 'ef62e6e2-f176-45ed-985d-4ac4d92e0a01'], 
[['Cl4', '0', '0'], ['Cf4', '1', '15'], '9eef66f0-9d45-4dd7-bb87-82575e5f0873'], 
[['Cl6', '0', '0'], ['Cf6', '1', '15'], 'b5e09394-ed5d-446a-b1c8-7153a5610ca3'],
[['Cl9', '0', '0'], ['Cf9', '1', '15'], '6aa68ab9-534c-4620-a38a-62898e2dbbe0'], 
[['Cl8', '0', '0'], ['Cf8', '1', '15'], 'ee6ccef4-abf7-4b45-9489-70b943b764c3'], 
[['Cf3', '1', '4'], ['Cf4', '1', '4'], 'a29be3ed-4a26-4008-9ceb-6e7bb12d4a5c'], 
[['Cf2', '1', '4'], ['Cf9', '1', '4'], '773c166f-173d-447d-a9c8-ab8005612fc1'], 
[['Cf7', '1', '8'], ['Cf8', '1', '8'], '9e456485-2989-4498-bf4e-71494b8001ca'], 
[['Cf5', '1', '6'], ['Cf6', '1', '6'], '20102f34-8f0e-4b9f-a35c-60eca0f390a6'], 
[['Cf1', '1', '2'], ['Cf2', '1', '2'], '41065641-7d72-4eac-a65d-68de80c9a332'], 
[['Cf2', '1', '3'], ['Cf3', '1', '3'], '89037731-58f7-43e1-adfa-17689bc520ba'], 
[['Cl1', '0', '0'], ['Cf1', '1', '15'], 'fd41a1c8-4a5f-47db-b583-bd9b951951cc']]
"""
def ospf(project_id, dynamips_num, dynamips_name_id_list, vpcs_name_id_list, vpcs_name_ip_list, all_link_list):

    # トレースルートをロック付きで実行する関数
    def run_traceroute_with_lock(port, where, when, communication_node, node2_ip, lock):
        with lock:
            traceroute.icmp_traceroute(port, where, when, communication_node, node2_ip)

    # シミュレーション開始
    print('GNS3-network-simulation ospf start')

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()

    # 機器設定手順内にSNS("ospf")がある機器には1，ない機器には0
    all_node_name_ospf_list = []
    for i in range(dynamips_num):
        node_name_ospf_list = []
        # VERIFICATIONforNCMonGNS3/を付けないから動かない？
        with open('VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/' + selected_folder + '/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f: # 機器設定プログラムで判断
            print("OPEN1")
            node_name_ospf_list.append(dynamips_name_id_list[i][1])
            for line in f:
                if "ospf" in line and len(node_name_ospf_list) == 1:

                    node_name_ospf_list.append(1)
                    break
            if len(node_name_ospf_list) == 1:
                node_name_ospf_list.append(0)
        all_node_name_ospf_list.append(node_name_ospf_list)

    #追加
    #all_node_name_ospf_list = [['Cf1', 1], ['Cf2', 1], ['Cf3', 1], ['Cf4', 0], ['Cf5', 1], ['Cf6', 1], ['Cf7', 1], ['Cf8', 1], ['Cf9', 1]]
    all_node_name_ospf_list = [['Cf1', 1], ['Cf2', 1], ['Cf3', 1], ['Cf4', 1], ['Cf5', 1], ['Cf6', 1], ['Cf7', 1], ['Cf8', 1], ['Cf9', 1]]
    print("all_node_name_ospf_list",end="")
    print(all_node_name_ospf_list)
    # 断線対象のリンクを示したリスト
    ospf_target_list = []
    for i in range(len(all_link_list)):
        # 互いの機器にOSPFが設定されているか判断する
        ospf_num = 0
        for j in range(len(all_node_name_ospf_list)):
            if all_link_list[i][0][0] == all_node_name_ospf_list[j][0]: #送信側の機器にospfの設定アリ
                ospf_num += all_node_name_ospf_list[j][1]
        for k in range(len(all_node_name_ospf_list)):
            if all_link_list[i][1][0] == all_node_name_ospf_list[k][0]: #受信側の機器にospfの設定アリ
                ospf_num += all_node_name_ospf_list[k][1]

        if ospf_num == 2:
            ospf_target_list.append(1)
            #print(all_link_list[i][0][0] + all_link_list[i][1][0])
        else:
            ospf_target_list.append(0)

    print("ospf_target_list=",end="")
    print(ospf_target_list)
    kaisuu = len(ospf_target_list)
    # kaisuu = 1
    for i in range(kaisuu): #全てのリンクに対して以下の処理を行う
        if ospf_target_list[i] == 0: #リンクが断線対象でなければ何もしない
            print("continue")
            continue
        else:
            # リンクの削除
            print('     link-delete           link-' + str(all_link_list[i][0][0]) + '-' + all_link_list[i][1][0] + ' start..........', end='')
            #curlコマンドで削除したいリンクのIDを指定
            link_delete_command = 'curl -i -X DELETE http://localhost:3080/v2/projects/' + project_id + '/links/' + str(all_link_list[i][2])
            #ここ修正　エラーハンドリングとサブプロセスの終了を取得する必要あり
            cp = subprocess.run(link_delete_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            cp.stdout
            print('complete')

            # 設定反映待ち
            print('     device-fault-handling..........')
            time.sleep(20)

            "------------------------------トレースルート--------------------------------------"
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
                            print("traceroute start linkfailure-link-"+str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0])+"-after-"+str(src_node_name + "-" + dst_node_name))

                            lock = vpcs_port_locks[src_node_telport]

                            # スレッドを作成してトレースルートを並列実行
                            thread = threading.Thread(
                                target=run_traceroute_with_lock,
                                args=(src_node_telport, str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0]), "after", f"{src_node_name}-{dst_node_name}", dst_node_ip, lock)
                            )
                            thread.start()
                            threads.append(thread)
                        else:
                            print(f"Telnetポートが見つかりませんでした: {src_node_name}")

                # すべてのスレッドが終了するまで待機
                for thread in threads:
                    thread.join()

            """
            #旧ver　送信元を決めて、全ての受信先に１つずつtracerouteを行っている
            for j in range(len(vpcs_name_ip_list)): #vpcsの数だけ繰り返す
                src_node_name = vpcs_name_ip_list[j][0] #送信元の端末名
                for k in range(len(vpcs_name_id_list)):
                    if vpcs_name_ip_list[j][0] == vpcs_name_id_list[k][1]: #送信側の端末(vpcs)のポート番号を検索
                        src_node_telport = vpcs_name_id_list[k][0]  #送信元のtelnet接続用ポートを取得
                        print("src_node_telport=",end="")
                        print(src_node_telport)
                        break
                for l in range(len(vpcs_name_ip_list)):
                    if src_node_name != vpcs_name_ip_list[l][0]: #送信元に選択中以外の端末を検索し、受信元に設定
                        dst_node_name = vpcs_name_ip_list[l][0] #受信元に設定する端末名
                        dst_node_ip = vpcs_name_ip_list[l][1] #受信元ipアドレス
                        print("traceroute start linkfailure-link-"+str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0])+"-after-"+str(src_node_name + "-" + dst_node_name))
                        ################################ キャプチャ（トレースルート）開始 #####################################################
                        traceroute.icmp_traceroute(src_node_telport, str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0]), "after", str(src_node_name + "-" + dst_node_name), dst_node_ip)
            """

            "------------------------------インターフェース--------------------------------------"
            # リンク削除後の機器の状態取得
            for j in range(dynamips_num):
                print('     device-status-capture device-' + str(dynamips_name_id_list[j][1]) + '   start..........', end='')
                #旧ver
                #status_check_allcover.status_check_ospf(str(dynamips_name_id_list[j][0]), int(j), 'after', int(i), all_link_list, dynamips_name_id_list)

                # スレッドを作成してインターフェースの状態取得
                thread = threading.Thread(
                    target=status_check_allcover.status_check_ospf,
                    args=(str(dynamips_name_id_list[j][0]), int(j), 'after', int(i), all_link_list, dynamips_name_id_list)
                )
                thread.start()
                threads.append(thread)
                print('complete')
            # すべてのスレッドが終了するまで待機
            for thread in threads:
                thread.join()

            "------------------------------ルーティングテーブル--------------------------------------"
            """
            # リンク削除後の機器の状態取得
            for j in range(dynamips_num):
                print('     device-status-capture device-' + str(dynamips_name_id_list[j][1]) + '   start..........', end='')

                # スレッドを作成してインターフェースの状態取得
                thread = threading.Thread(
                    target=status_check_allcover.route_table_check_ospf,
                    args=(str(dynamips_name_id_list[j][0]), int(j), 'after', int(i), all_link_list, dynamips_name_id_list)
                )
                thread.start()
                threads.append(thread)
                print('complete')
            # すべてのスレッドが終了するまで待機
            for thread in threads:
                thread.join()
            """

            # linkの復旧
            for j in range(dynamips_num):
                if all_link_list[i][0][0] == dynamips_name_id_list[j][1]:
                    node_ID_1 = dynamips_name_id_list[j][2]
                if all_link_list[i][1][0] == dynamips_name_id_list[j][1]:
                    node_ID_2 = dynamips_name_id_list[j][2]
            link_create_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + project_id +'/links -d "{""nodes"": [{""adapter_number"": ' + all_link_list[i][0][1] + ', ""node_id"": ""' + str(node_ID_1) + '"", ""port_number"": ' + all_link_list[i][0][2] + '}, {""adapter_number"": ' + all_link_list[i][1][1] + ', ""node_id"": ""' + str(node_ID_2) + '"", ""port_number"": ' + all_link_list[i][1][2] + '}]}"'
            file_path = f'VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_{i + 1}.txt'
            try:
                # リンク生成（復旧）のコマンドを実行した結果をファイルに書き込み
                with open(file_path, 'w', encoding='shift-jis') as f:
                    print("Recovery " + str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0]))
                    cp = subprocess.run(link_create_command, shell=False, encoding='shift-jis', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    f.write(cp.stdout)

                # ファイルの読み込み
                with open(file_path, 'r', encoding='shift-jis') as f:
                    j = 0
                    for line in f:
                        #######修正必要　14行目に'link_id'の記述ナシ　20行目または21行目に含まれている###############################################################################
                        if j == 14: #14行目に'link_id'という記述が含まれるか？
                            if 'link_id' in line:
                                link_ID = line[16:52]
                                all_link_list[i][2] = link_ID #新たに生成されたリンクのIDを取得し更新
                                print('link_ID Update')
                                break
                            else:
                                print('link_ID not found')
                        else:
                            j += 1

            except FileNotFoundError:
                print(f'ファイル {file_path} が見つかりませんでした。')
            except subprocess.CalledProcessError as e:
                print(f'サブプロセスの実行中にエラーが発生しました: {e}')
            except UnicodeDecodeError:
                print('ファイルのデコード中にエラーが発生しました。エンコーディングを確認してください。')
            except Exception as e:
                print(f'予期せぬエラーが発生しました: {e}')

            # 設定反映待ち
            #time.sleep(40)
            time.sleep(20)

    print('GNS3-network-simulation complete')

    return 0

#######################################################################################################################################

def stp(project_id, dynamips_num, dynamips_name_id_list, vpcs_name_id_list, vpcs_name_ip_list, all_link_list):
    all_node_name_stp_list = []
    for i in range(dynamips_num):
        node_name_stp_list = []
        # VERIFICATIONforNCMonGNS3/を付けないから動かない？
        with open('VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/cmd_kiki/cmd_kiki_Cf' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f: # 機器設定プログラムで判断
            node_name_stp_list.append(dynamips_name_id_list[i][1])
            for line in f:
                if "spanning-tree" in line and len(node_name_stp_list) == 1:
                    node_name_stp_list.append(1)
                    break
            if len(node_name_stp_list) == 1:
                node_name_stp_list.append(0)
        all_node_name_stp_list.append(node_name_stp_list)

    # 断線対象のリンクを示したリスト
    stp_target_list = []
    for i in range(len(all_link_list)):
        # 互いの機器にOSPFが設定されているか判断する
        stp_num = 0
        for j in range(len(all_node_name_stp_list)):
            if all_link_list[i][0][0] == all_node_name_stp_list[j][0]:
                stp_num += all_node_name_stp_list[j][1]
        for k in range(len(all_node_name_stp_list)):
            if all_link_list[i][1][0] == all_node_name_stp_list[k][0]:
                stp_num += all_node_name_stp_list[k][1]
        if stp_num == 2:
            stp_target_list.append(1)
        else:
            stp_target_list.append(0)

    kaisuu = len(stp_target_list)
    # kaisuu = 1



    # 障害発生後を確認
    first_time = True
    for i in range(kaisuu):
        # ここで障害発生前の状態を確認する
        if first_time:
            # ここで障害前の挙動を確認しておこうかな
            print(' link failure link-' + str(all_link_list[i][0][0]) + '-' + all_link_list[i][1][0])
            # もともとの機器の状態を取得
            for j in range(dynamips_num):# node_nameからkiki_nameに変更
                print('     device-status-capture device-' + str(dynamips_name_id_list[j][1]) + '   start..........', end='')
                status_check_allcover.status_check_stp(str(dynamips_name_id_list[j][0]), int(j), 'before', int(i), all_link_list, dynamips_name_id_list)
                print('complete')
            # 各クライアントの通信，通信経路をキャプチャ開始して終了まで
            # 今回はキャプチャして放置すればエンジニアが確認してくれる想定かな
            # リンクの個数(all_link_list)だけ回す

            time.sleep(100)
            for j in range(len(all_link_list)):
                # 各リンクのキャプチャを開始する
                # 断線してる箇所のキャプチャは例外処理？
                # capture_file_name = none-cf1-cf2.pcap
                # shell = Trueにすると動かない　なぜかはしらん
                capture_file_name = "linkfailure-link-none-" + "before" + "-capture-" + str(all_link_list[j][0][0]) + "-" + str(all_link_list[j][1][0]) + ".pcap"
                link_ID = str(all_link_list[j][2])
                # print('capture_file_name = ' + capture_file_name)
                ###########captureファイル生成########################################################
                capture_start_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + project_id + '/links/' + link_ID + '/start_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
                # print(capture_start_command)
                cp = subprocess.run(capture_start_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                # print('----------------------')
            # 各クライアント同士の疎通確認
            # name_ip_listから最初のノードを取得
            # 最初のノードに接続して、ほかのIPへping
            # 2つ目以降のノードにも繰り返す
            # vpcs_name_ip_list = 
            # [['Cl2', '192.168.1.2'], ['Cl3', '192.168.1.3'], ['Cl1', '192.168.1.1']]
            # tool.vpcs_name_ip_list
            for j in range(len(vpcs_name_ip_list)):
                src_node_name = vpcs_name_ip_list[j][0]
                for k in range(len(vpcs_name_id_list)):
                    if vpcs_name_ip_list[j][0] == vpcs_name_id_list[k][1]:
                        # 送信元のtelnet接続用ポートを取得
                        src_node_telport = vpcs_name_id_list[k][0]
                        print("src_node_telport = ")
                        print(src_node_telport)
                        break
                for l in range(len(vpcs_name_ip_list)):
                    if src_node_name != vpcs_name_ip_list[l][0]:
                        dst_node_name = vpcs_name_ip_list[l][0]
                        dst_node_ip = vpcs_name_ip_list[l][1]
                        print("traceroute start")
                        traceroute.traceroute(src_node_telport, str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0]), "before", str(src_node_name + "-" + dst_node_name), dst_node_ip)

            # [[node_accessport, node_name, node_id], [...]]
            # tool.vpcs_name_ID_list
            # キャプチャの終了
            for j in range(len(all_link_list)):
                # 各リンクのキャプチャを開始する
                # 断線してる箇所のキャプチャは例外処理？
                # capture_file_name = none-cf1-cf2.pcap
                # shell = Trueにすると動かない　なぜかはしらん
                capture_file_name = "linkfailure-link-none-" + "before" + "-capture-" + str(all_link_list[j][0][0]) + "-" + str(all_link_list[j][1][0]) + ".pcap"
                link_ID = str(all_link_list[j][2])
                print('capture_file_name = ' + capture_file_name)
                capture_stop_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + project_id + '/links/' + link_ID + '/stop_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
                print(capture_stop_command)
                cp = subprocess.run(capture_stop_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                print('----------------------')
            time.sleep(10)

            # 初めて以外の時はスキップするためにfalseにする
        first_time = False


        # 障害発生後に関して
        if stp_target_list[i] == 0:
            continue
        else:
            # リンクの削除
            print('     link-delete           link-' + str(all_link_list[i][0][0]) + '-' + all_link_list[i][1][0] + ' start..........', end='')
            link_delete_command = 'curl -i -X DELETE http://localhost:3080/v2/projects/' + project_id + '/links/' + str(all_link_list[i][2])
            cp = subprocess.run(link_delete_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            cp.stdout
            print('complete')

            # 設定反映待ち
            print('     device-fault-handling..........')
            time.sleep(40)

            # リンク削除後の機器の状態取得
            for j in range(dynamips_num):
                print('     device-status-capture device-' + str(dynamips_name_id_list[j][1]) + '   start..........', end='')
                status_check_allcover.status_check_stp(str(dynamips_name_id_list[j][0]), int(j), 'after', int(i), all_link_list, dynamips_name_id_list)
                print('complete')

            for j in range(len(all_link_list)):
                # 各リンクのキャプチャを開始する

                # 断線してる箇所のキャプチャは例外処理？

                # capture_file_name = none-cf1-cf2.pcap
                # shell = Trueにすると動かない　なぜかはしらん
                capture_file_name = "linkfailure-link-" + str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0]) + "-" + "after" + "-capture-" + str(all_link_list[j][0][0]) + "-" + str(all_link_list[j][1][0]) + ".pcap"
                link_ID = str(all_link_list[j][2])
                # print('capture_file_name = ' + capture_file_name)
                capture_start_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + project_id + '/links/' + link_ID + '/start_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
                # print(capture_start_command)
                cp = subprocess.run(capture_start_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                # print('----------------------')

            # 各クライアント同士の疎通確認
            # name_ip_listから最初のノードを取得
            # 最初のノードに接続して、ほかのIPへping
            # 2つ目以降のノードにも繰り返す

            # vpcs_name_ip_list = 
            # [['Cl2', '192.168.1.2'], ['Cl3', '192.168.1.3'], ['Cl1', '192.168.1.1']]
            # tool.vpcs_name_ip_list

            for j in range(len(vpcs_name_ip_list)):
                src_node_name = vpcs_name_ip_list[j][0]
                for k in range(len(vpcs_name_id_list)):
                    if vpcs_name_ip_list[j][0] == vpcs_name_id_list[k][1]:
                        # 送信元のtelnet接続用ポートを取得
                        src_node_telport = vpcs_name_id_list[k][0]
                        print("src_node_telport = ")
                        print(src_node_telport)
                        break
                for l in range(len(vpcs_name_ip_list)):
                    if src_node_name != vpcs_name_ip_list[l][0]:
                        dst_node_name = vpcs_name_ip_list[l][0]
                        dst_node_ip = vpcs_name_ip_list[l][1]
                        print("traceroute start")
                        traceroute.traceroute(src_node_telport, str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0]), "after", str(src_node_name + "-" + dst_node_name), dst_node_ip)


            # [[node_accessport, node_name, node_id], [...]]
            # tool.vpcs_name_ID_list

            # キャプチャの終了
            for j in range(len(all_link_list)):
                # 各リンクのキャプチャを開始する
                # 断線してる箇所のキャプチャは例外処理？
                # capture_file_name = none-cf1-cf2.pcap
                # shell = Trueにすると動かない　なぜかはしらん
                capture_file_name = "linkfailure-link-" + str(all_link_list[i][0][0]) + '-' + str(all_link_list[i][1][0]) + "-" + "after" + "-capture-" + str(all_link_list[j][0][0]) + "-" + str(all_link_list[j][1][0]) + ".pcap"
                link_ID = str(all_link_list[j][2])
                print('capture_file_name = ' + capture_file_name)
                capture_stop_command = 'curl -i -X POST "http://localhost:3080/v2/projects/' + project_id + '/links/' + link_ID + '/stop_capture" -d "{""capture_file_name"": ""' + capture_file_name + '"", ""data_link_type"": ""DLT_EN10MB""}"'
                print(capture_stop_command)
                cp = subprocess.run(capture_stop_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                print('----------------------')
            time.sleep(10)

            # linkの復旧
            for j in range(dynamips_num):
                if all_link_list[i][0][0] == dynamips_name_id_list[j][1]:
                    node_ID_1 = dynamips_name_id_list[j][2]
                if all_link_list[i][1][0] == dynamips_name_id_list[j][1]:
                    node_ID_2 = dynamips_name_id_list[j][2]

            link_create_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + project_id +'/links -d "{""nodes"": [{""adapter_number"": ' + all_link_list[i][0][1] + ', ""node_id"": ""' + str(node_ID_1) + '"", ""port_number"": ' + all_link_list[i][0][2] + '}, {""adapter_number"": ' + all_link_list[i][1][1] + ', ""node_id"": ""' + str(node_ID_2) + '"", ""port_number"": ' + all_link_list[i][1][2] + '}]}"'
            with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
                cp = subprocess.run(link_create_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                f.write(cp.stdout)
            with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
                j = 0
                for line in f:
                    if j == 14:
                        if 'link_id' in line:
                            link_ID = line[16:52]
                            #print(link_ID)
                            all_link_list[i][2] = link_ID
                            #print(tool.all_link_list)
                            break
                        #else:
                        #    print('error')
                    else:
                        j += 1

            # 設定反映待ち
            time.sleep(40)

    return 0