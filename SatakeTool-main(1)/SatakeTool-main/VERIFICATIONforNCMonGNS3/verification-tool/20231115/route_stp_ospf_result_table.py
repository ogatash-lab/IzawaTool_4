import PySide6
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui

import os
import sys
import yaml

import time_count

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget
import pandas as pd

# 環境変数にPySide6を登録
dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class MainWindow(QWidget):

    def __init__(self, parent=None):
        # 親クラスの初期化
        super().__init__(parent)
        # ウィンドウタイトル
        self.setWindowTitle("検証結果表")

        check_route_l2 = False #True
        check_route_l3 = False #True
        check_stp = False #True
        check_ospf = True #False

        # ウィンドウサイズを指定（px単位）
        windowWidth = 1000  # ウィンドウの横幅
        windowHeight = 1200  # ウィンドウの高さ

        # path_crd_model = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-stp-3_model.yaml"
        # path_crd = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-stp-3.yaml"

        # 設計者が理想とする各機器の状態を表すファイル
        #path_crd = "../communication_root/crd-ospf-9.yaml"
        #path_crd = "../communication_root/crd-ospf-9_IZAWA_NoMistake.yaml"
        path_crd = "../izawa_result/cmd_kiki_none.yaml"
        #path_crd = "../communication_root/crd-ospf-9_IZAWA_Cf4IntNotOSPF.yaml"
        #path_crd = "../communication_root/crd-stp-9.yaml"

        #GNS3で障害を発生させ検証した結果（機器の状態）
        #path_crd_model = "../communication_root/crd-ospf-9_model.yaml"
        #path_crd_model = "../communication_root/crd-ospf-9_IZAWA_Cf4NotOSPF.yaml" #Cf4にOSPFの設定なし
        #path_crd_model = "../communication_root/crd-ospf-9_IZAWA_NoMistake.yaml"
        #path_crd_model = "../communication_root/crd-ospf-9_IZAWA_Cf4IntNotOSPF.yaml" #Cf4のエリア３のインターフェースが未設定
        #path_crd_model = "../communication_root/crd-ospf-9_IZAWA_NoMistake_test.yaml"
        path_crd_model = "izawa/cmd_kiki_Cf4_int_2-6.yaml"
        #path_crd_model = "../communication_root/crd-ospf-9_IZAWA_Cf3Cf6SameRouterId.yaml" #Cf4とCf6のrouter-idが同一
        #path_crd_model = "../communication_root/crd-ospf-9_IZAWA_Cf4Cf6SameRouterId.yaml" #Cf4とCf6のrouter-idが同一
        #path_crd_model = "../communication_root/crd-ospf-9_IZAWA_Cf5Cf6SameRouterId.yaml" #Cf4とCf6のrouter-idが同一
        #path_crd_model = "../communication_root/crd-ospf-9-withCf4NotOSPF_model.yaml"
        #path_crd_model = "../communication_root/crd-stp-9_model.yaml"

        # path_crd_model = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_model.yaml"
        # path_crd_model = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9-withCf4NotOSPF_model.yaml"
        # path_crd_model = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9-withCf4IntNotOSPF_model.yaml"
        #path_crd_model = "../communication_root/crd-ospf-9-withCf4Cf6NotOSPF_model.yaml"
        # path_crd_model = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9-withCf4Cf6SameRouterId_model.yaml"
        # path_crd_model = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9-withJoma_model.yaml"
        # path_crd = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9.yaml"

        with open(path_crd) as file:
            crd = yaml.safe_load(file)
        with open(path_crd_model) as file:
            crd_model = yaml.safe_load(file)

        # ウィンドウサイズの変更
        self.resize(windowWidth, windowHeight)

        # ラベルを表示するメソッド
        ng_count_list = self.SetTree(crd, crd_model, check_route_l2, check_route_l3, check_stp, check_ospf)

        self.SetLabel(crd, crd_model, ng_count_list)


    # ラベルは別のメソッドに分けました
    def SetLabel(self, crd, crd_model, ng_count_list):
        # ラベルを使うことを宣言（引数のselfはウィンドウのことで、ウィンドウにラベルが表示されます）

        execution_time = QtWidgets.QLabel(self)
        
        # ラベルに文字を指定
        execution_time.setText("実行時間: ")
        execution_time.move(10, 0)

        time_count_file_name = "./time_count.txt"
        execution_time.setText("実行時間: " + time_count.culcurate_time(time_count_file_name))
        execution_time.move(10, 0)

        # NGの合計
        ng_count_sum = QtWidgets.QLabel(self)
        ng_count_sum.setText("NG count (total: " + str(sum(ng_count_list)) + ", route: " + str(ng_count_list[0]) + ", stp: " + str(ng_count_list[1]) + ", ospf: " + str(ng_count_list[2]) + ")")
        ng_count_sum.move(150, 15)


    # ツリーのウィジェット
    def SetTree(self, crd, crd_model, check_route_l2, check_route_l3, check_stp, check_ospf):
        # NGの個数の集計
        ng_count_route = 0
        ng_count_stp = 0
        ng_count_ospf = 0
        qw_tree = QtWidgets.QTreeWidget(self)

        # QtWidgets.QTreeWidgetItem.sizeHint(200)
        
        # 最初からツリーの中を表示するかどうか
        # qw_tree.expandAll()
        qw_tree.resize(1000, 1000)
        qw_tree.move(0, 30)
        qw_tree.header().resizeSection(1000, 1000)
        qw_tree.header().setStretchLastSection(False)
        # qw_tree.setHeaderLabels(["検証結果", "通信区間", "通信経路(通信経路の仕様)", "通信経路(ネットワーク構成モデル)"])
        # この""を追加しないと表示できる項目が増えない
        qw_tree.setHeaderLabels(["リンク障害発生箇所", "", "", "", ""])

        # 重みづけ誤り箇所特定に用いる二次元配列のデータ　可変長にまだしてない
        data = [["Router", "NG", "DOWN", "ERROR", "RISK"]]
        for n in range(1,10):
            data.append(["Cf"+str(n),0,0,0,0])

        for i in range(len(crd)):
            #list(crd.keys()) = ['Cf1-Cf2', 'Cf2-Cf3', 'Cf2-Cf9', 'Cf3-Cf4', 'Cf4-Cf5', 'Cf5-Cf6', 'Cf6-Cf7', 'Cf7-Cf8', 'Cf8-Cf9', 'none']
            linkfailure_point = list(crd.keys())[i] # [list(yaml_test.keys())[i]] で障害発生箇所を取得
            qw_tree_parent_item = QtWidgets.QTreeWidgetItem([linkfailure_point]) #GUIに新しいツリーアイテムを追加

            ############################## 通信経路の比較###############################################################

            communication_route = QtWidgets.QTreeWidgetItem(["communication_route"])
            
            # 通信区間というitemを追加してもいいかも
            # L2L3通信経路設計記述(理想としている通信経路：crd)
            for communication_section in crd[linkfailure_point]["communication-route"]: #１か所のリンク障害における全てのvpcs間通信の結果を取り出す
                val = QtWidgets.QTreeWidgetItem([communication_section])
                val.addChild(QtWidgets.QTreeWidgetItem(["検証結果", "プロトコル", "通信経路(L2L3通信経路設計記述)", "通信経路(ネットワーク構成モデル)"]))

                # 該当のプロトコルの分だけ回す protocol = "icmp"
                for protocol in crd[linkfailure_point]["communication-route"][communication_section]: #現状icmpのみ（ループせず１度だけ実行）
                    # yamlから通信経路を取得する
                    crd_route = crd[linkfailure_point]["communication-route"][communication_section][protocol] #理想としている通信経路
                    crd_model_route = crd_model[linkfailure_point]["communication-route"][communication_section][protocol] #シミュレーション結果の通信経路

                    ans = "OK"
                    if crd_route != crd_model_route: #理想と現実が一致していないなら
                        ans = "NG"
                        ng_count_route += 1
                        

                    # リストだと表示されないみたいだからテキストに直す
                    crd_route_str = ""
                    for k in range(len(crd_route)): #理想のvpcs間の通信で経由する全ての機器を取り出し矢印でつなぎ表示させる
                        crd_route_str += crd_route[k]
                        if len(crd_route) != k + 1:
                            crd_route_str += " -> "

                    crd_model_route_str = ""
                    for k in range(len(crd_model_route)): #現実のvpcs間の通信で経由する全ての機器を取り出し矢印でつなぎ表示させる
                        crd_model_route_str += crd_model_route[k]
                        if len(crd_model_route) != k + 1:
                            crd_model_route_str += " -> "

                    #作成した文字列を[communication_section]の子に追加
                    val.addChild(QtWidgets.QTreeWidgetItem([ans, protocol, crd_route_str, crd_model_route_str]))
                    if ans == "OK":
                        val.setBackground(0, QtGui.QBrush(QtCore.Qt.green))
                    else:
                        val.setBackground(0, QtGui.QBrush(QtCore.Qt.red))
                # 検証結果は色分けで判断 文言も追加した方がいいかな
                # そのためのラベルも追加しよかな
                
                communication_route.addChild(val)


            # 
            # STPの設定の比較？機器ごとに回そかな
            # 
            if check_stp == True:
                stp = QtWidgets.QTreeWidgetItem(["stp"])
                # stp.addChild(QtWidgets.QTreeWidgetItem(["機器", "VLAN", "port_status", "root bridge"]))
                # 機器ごとに役割を分けるため，機器ごとの検証結果を示す？
                for node_name in crd[linkfailure_point]["stp"]:
                    val = QtWidgets.QTreeWidgetItem([node_name])
                    val.addChild(QtWidgets.QTreeWidgetItem(["該当VLAN"]))
                    for vlan_name in crd[linkfailure_point]["stp"][node_name]:
                        val2 = QtWidgets.QTreeWidgetItem([vlan_name])
                        val2.addChild(QtWidgets.QTreeWidgetItem(["検証結果", "L2L3通信経路設計記述", "ネットワーク構成モデル"]))
                        # root_bridge の検証結果の追加
                        ans = "OK"
                        if str(crd[linkfailure_point]["stp"][node_name][vlan_name]["root_bridge"]) != str(crd_model[linkfailure_point]["stp"][node_name][vlan_name]["root_bridge"]):
                            ans = "NG"
                            ng_count_stp += 1
                        val2.addChild(QtWidgets.QTreeWidgetItem([ans, "root_bridge :  " + str(crd[linkfailure_point]["stp"][node_name][vlan_name]["root_bridge"]), "root_bridge :  " + str(crd_model[linkfailure_point]["stp"][node_name][vlan_name]["root_bridge"])]))
                        # port_status の検証結果の追加
                        for j in range(len(crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"])):
                            # print(yaml_test[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j])
                            # val2.addChild(QtWidgets.QTreeWidgetItem(["検証結果", yaml_test[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][0], "ネットワーク構成モデル(機器, VLAN, port status, root bridge)"]))
                            ans = "OK"
                            # model と crd　のポートの個数が異なるからエラー出てる
                            # ここから追加したよ
                            tst = 0
                            for k in range(len(crd_model[linkfailure_point]["stp"][node_name][vlan_name]["port_status"])):
                                # portが同じか確認
                                if crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][0] == crd_model[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][k][0]:
                                    # statusが同じか確認
                                    if crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][1] != crd_model[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][k][1]:
                                        ans = "NG"
                                        ng_count_stp += 1
                                    val2.addChild(QtWidgets.QTreeWidgetItem([ans, crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][0] + " :  " +  crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][1], crd_model[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][k][0] + " :  " +  crd_model[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][k][1]]))
                                    tst += 1
                                    break
                            # 対応ポートがなかった時の処理
                            if tst == 0:
                                ans = "NG"
                                ng_count_stp += 1
                                val2.addChild(QtWidgets.QTreeWidgetItem([ans, crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][0] + " :  " +  crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][1], "対応ポートないよ"]))
                            # if crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][1] != crd_model[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][1]:
                            #     ans = "NG"
                            #     ng_count_stp += 1
                            # val2.addChild(QtWidgets.QTreeWidgetItem([ans, crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][0] + " :  " +  crd[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][1], crd_model[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][0] + " :  " +  crd_model[linkfailure_point]["stp"][node_name][vlan_name]["port_status"][j][1]]))
                        val.addChild(val2)

                    stp.addChild(val)

            # 
            # OSPFの設定の比較？
            #

            if check_ospf == True:
                ospf = QtWidgets.QTreeWidgetItem(["ospf"]) #ツリーアイテムに"ospf"という項目を追加
                for node_name in crd[linkfailure_point]["ospf"]: #全てのルータ（Cf1～Cf9）
                    val = QtWidgets.QTreeWidgetItem([node_name])
                    val.addChild(QtWidgets.QTreeWidgetItem(["検証結果", "L2L3通信経路設計記述", "ネットワーク構成モデル"]))
                    
                    ng_count_ospf_val = 0
                    for i in range(len(crd[linkfailure_point]["ospf"][node_name])):
                        # この辺で比較項目を整理しよかな

                        crd_val2 = crd[linkfailure_point]["ospf"][node_name][i] #理想  crd_val2 = ['VLAN10', '0', 'DR']（[VLAN,エリア,状態]）
                        crd_model_val2 = ["error", "error", "error"] #現実
                        try:
                            for j in range(len(crd_model[linkfailure_point]["ospf"][node_name])):
                                # VLANの値とエリアが同じものを選択
                                if crd_val2[0] == crd_model[linkfailure_point]["ospf"][node_name][j][0] and crd_val2[1] == crd_model[linkfailure_point]["ospf"][node_name][j][1]:
                                    crd_model_val2 = crd_model[linkfailure_point]["ospf"][node_name][j] #シミュレーション結果を代入

                            # crd_model_val2 = crd_model[linkfailure_point]["ospf"][node_name][i]
                        except:
                            print("error")
                            crd_model_val2 = ["error", "error", "error"]
                        # モデルと設計記述の判定
                        ans = "OK"
                        if crd_val2 != crd_model_val2:
                            ans = "NG"

                            #誤り特定表
                            for k in range(1,len(data)):
                                if data[k][0] == node_name:
                                    data[k][1] += 1 #NGに１加算
                                    if crd_model_val2[2] == "DOWN":
                                        data[k][2] += 1 #DOWNに１加算
                                        data[k][4] += 1 #RISKに１加算

                                    if crd_model_val2[2] == "error":
                                        data[k][3] += 1 #ERORRに１加算
                                        data[k][4] += 3 #RISKに３加算

                            ng_count_ospf_val += 1

                        crd_str = crd_val2[0] + ", エリア: " + crd_val2[1] + ", status: " + crd_val2[2]
                        crd_model_str = crd_model_val2[0] + ", エリア: " + crd_model_val2[1] + ", status: " + crd_model_val2[2]
                        val.addChild(QtWidgets.QTreeWidgetItem([ans, crd_str, crd_model_str]))

                    # 背景の色付け
                    if ng_count_ospf_val == 0:
                        val.setBackground(0, QtGui.QBrush(QtCore.Qt.green))
                    else:
                        val.setBackground(0, QtGui.QBrush(QtCore.Qt.red))
                    ospf.addChild(val)
                    ng_count_ospf += ng_count_ospf_val


            #
            # 各要素を追加
            #
            if check_stp == True:
                qw_tree_parent_item.addChildren([QtWidgets.QTreeWidgetItem(["設計項目"]), communication_route, stp])
            if check_ospf == True:
                qw_tree_parent_item.addChildren([QtWidgets.QTreeWidgetItem(["設計項目"]), communication_route, ospf])
            qw_tree.addTopLevelItem(qw_tree_parent_item)

        # 名前を縦軸に設定してデータフレームを作成
        df = pd.DataFrame(data[1:], columns=data[0]).set_index("Router")
        print(df)
        return [ng_count_route, ng_count_stp, ng_count_ospf]


app = QApplication(sys.argv)    # PySide6の実行
window = MainWindow()           # ユーザがコーディングしたクラス
window.show()                   # PySide6のウィンドウを表示
sys.exit(app.exec())            # PySide6の終了
