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
import re  # 追加：正規表現モジュールをインポート

# pandasのオプションを設定して全ての列を表示
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)  # 必要に応じて幅を調整

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

        check_route_l2 = False  # True
        check_route_l3 = True  # True
        check_stp = False  # True
        check_ospf = True  # False
        check_route_table = False  # False

        # ウィンドウサイズを指定（px単位）
        windowWidth = 1000  # ウィンドウの横幅
        windowHeight = 1200  # ウィンドウの高さ

        # 設計者が理想とする各機器の状態を表すファイル
        #path_crd = "../izawa_result/cmd_kiki_none.yaml"
        path_crd = "../izawa_result/cmd_kiki_temp.yaml"
        #path_crd = "../izawa_result/cmd_kiki_temp.yaml"
        #path_crd = "../izawa_result/cmd_kiki_cost_temp-1.yaml"


        with open(path_crd) as file:
            crd = yaml.safe_load(file)

        # Get list of crd_model files
        #crd_model_dir = "./izawa"
        #crd_model_dir = "./result_table_ospf"

        #crd_model_dir = "./result_table_ospf_2-6"
        #crd_model_dir = "./result_table_interface_2-6"
        #crd_model_dir = "./result_table_id_2-6"
        crd_model_dir = "./result_table_id"
        # crd_model_dir = "./izawa"

        crd_model_files = [f for f in os.listdir(crd_model_dir) if f.endswith('.yaml') and f != 'cmd_kiki_none.yaml']
        # Build full paths
        crd_model_paths = [os.path.join(crd_model_dir, f) for f in crd_model_files]

        # ウィンドウサイズの変更
        self.resize(windowWidth, windowHeight)

        # ラベルを表示するメソッド
        ng_count_list = self.SetTree(crd, crd_model_paths, check_route_l2, check_route_l3, check_stp, check_ospf, check_route_table)

        self.SetLabel(ng_count_list)


    # ラベルは別のメソッドに分けました
    def SetLabel(self, ng_count_list):
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
        ng_count_sum.setText("NG count (total: " + str(sum(ng_count_list)) + ", route: " + str(
            ng_count_list[0]) + ", stp: " + str(ng_count_list[1]) + ", ospf: " + str(ng_count_list[2]) + ")")
        ng_count_sum.move(150, 15)

    # ツリーのウィジェット
    def SetTree(self, crd, crd_model_paths, check_route_l2, check_route_l3, check_stp, check_ospf, check_route_table):
        all_link_list = [
            [['Cf4', '1', '5'], ['Cf5', '1', '5'], '24ef7c05-3a14-4714-823a-d394e6fe0c87'],
            [['Cf2', '1', '3'], ['Cf3', '1', '3'], '34a19a78-5cf7-4308-9b23-6de198ce76c9'],
            [['Cl3', '0', '0'], ['Cf3', '1', '15'], '39419595-4e13-471e-a911-00884eb0ac14'],
            [['Cl8', '0', '0'], ['Cf8', '1', '15'], 'c2e01387-d12a-42b4-9391-18c2004019ba'],
            [['Cf2', '1', '4'], ['Cf9', '1', '4'], 'c1062df7-5f4c-460b-972b-a7f65f1e70c9'],
            [['Cf3', '1', '4'], ['Cf4', '1', '4'], '838af801-136a-45f9-af29-a7f992a341cc'],
            [['Cf6', '1', '7'], ['Cf7', '1', '7'], '51c10075-bff0-47ac-9e19-33f32c21bc48'],
            [['Cl5', '0', '0'], ['Cf5', '1', '15'], '8860b0b0-065c-4e43-b3c8-75666993619f'],
            [['Cf7', '1', '8'], ['Cf8', '1', '8'], 'f484e524-b960-418d-b195-b8b8a8469873'],
            [['Cf8', '1', '9'], ['Cf9', '1', '9'], 'bcd8fa18-160b-41e5-a988-25ea1634d1d3'],
            [['Cl7', '0', '0'], ['Cf7', '1', '15'], '6990af3e-ab7a-4de3-8606-5daac678ca33'],
            [['Cf1', '1', '2'], ['Cf2', '1', '2'], '06498e1d-da8e-4713-8863-aac3ac80eb14'],
            [['Cl2', '0', '0'], ['Cf2', '1', '15'], '3efb11bd-d83a-4023-bec1-9b44d451f1d6'],
            [['Cf5', '1', '6'], ['Cf6', '1', '6'], '556c8d27-d1c8-4b8a-afd0-be8a60a59398'],
            [['Cl1', '0', '0'], ['Cf1', '1', '15'], '9ee0b100-d046-4a23-969b-4a5f0eeedb8f'],
            [['Cl9', '0', '0'], ['Cf9', '1', '15'], 'c619835f-8fcb-4552-9809-ba36c49fc7e4'],
            [['Cl4', '0', '0'], ['Cf4', '1', '15'], 'dd8d008d-2de1-468a-a4f4-b5967f41fb59'],
            [['Cl6', '0', '0'], ['Cf6', '1', '15'], '0eda0bda-e02f-4b75-b1d6-33110cd76a6c']]

        # NGの個数の集計
        ng_count_route_total = 0
        ng_count_stp_total = 0
        ng_count_ospf_total = 0
        ng_count_route_table_total = 0
        qw_tree = QtWidgets.QTreeWidget(self)

        # 最初からツリーの中を表示するかどうか
        # qw_tree.expandAll()
        qw_tree.resize(1000, 1000)
        qw_tree.move(0, 30)
        qw_tree.header().resizeSection(1000, 1000)
        qw_tree.header().setStretchLastSection(False)
        qw_tree.setHeaderLabels(["ファイル名", "", "", "", ""])

        # ルータ名のリストを作成
        routers = ['Cf' + str(n) for n in range(1, 10)]
        # RISKとSCOREを集計するためのDataFrameを初期化
        risk_df = pd.DataFrame(index=routers)
        score_df = pd.DataFrame(index=routers)
        risk2_df = pd.DataFrame(index=routers)

        for crd_model_path in crd_model_paths:
            with open(crd_model_path) as file:
                crd_model = yaml.safe_load(file)

            # Get the file name from the path
            file_name = os.path.basename(crd_model_path)

            # ファイル名から機器名を抽出（末尾に近い方のCfXを取得）
            # device_names = re.findall(r'Cf\d+', file_name)
            device_names = re.findall(r'cmd_kiki_([^_]+)_', file_name)
            if device_names:
                device_name = device_names[-1]  # 最後の機器名を取得
            else:
                # デフォルト値としてファイル名全体を使用
                device_name = file_name

            # Create a top-level item for the file
            file_item = QtWidgets.QTreeWidgetItem([file_name])

            # NG counts for this file
            ng_count_route = 0
            ng_count_stp = 0
            ng_count_ospf = 0
            ng_count_route_table = 0

            # 重みづけ誤り箇所特定に用いる二次元配列のデータ
            data = [["Router", "NG", "DOWN", "ERROR", "RISK"]]
            for n in range(1, 10):
                data.append(["Cf" + str(n), 0, 0, 0, 0])

            route_data = [["Router", "SCORE"]]
            for n in range(1, 10):
                route_data.append(["Cf" + str(n), 0])

            table_data = [["Router", "RISK2"]]
            for n in range(1, 10):
                table_data.append(["Cf" + str(n), 0])

            for i in range(len(crd)):
                linkfailure_point = list(crd.keys())[i]
                qw_tree_parent_item = QtWidgets.QTreeWidgetItem([linkfailure_point])

                ############################## 通信経路の比較 ###############################################################

                communication_route = QtWidgets.QTreeWidgetItem(["communication_route"])

                for communication_section in crd[linkfailure_point]["communication-route"]:
                    val = QtWidgets.QTreeWidgetItem([communication_section])
                    val.addChild(
                        QtWidgets.QTreeWidgetItem(["検証結果", "プロトコル", "通信経路(L2L3通信経路設計記述)", "通信経路(ネットワーク構成モデル)"]))

                    for protocol in crd[linkfailure_point]["communication-route"][communication_section]:
                        crd_route = crd[linkfailure_point]["communication-route"][communication_section][protocol]
                        crd_model_route = crd_model[linkfailure_point]["communication-route"][communication_section][protocol]

                        ans = "OK"
                        if crd_route != crd_model_route:
                            ans = "NG"
                            ng_count_route += 1

                            for router in crd_route:
                                if not "Cf" in router:
                                    continue

                                if not router in crd_model_route:
                                    for k in range(1, len(route_data)):
                                        if route_data[k][0] == router:
                                            route_data[k][1] += 1  # SCOREに加算

                        crd_route_str = " -> ".join(crd_route)
                        crd_model_route_str = " -> ".join(crd_model_route)

                        val.addChild(QtWidgets.QTreeWidgetItem([ans, protocol, crd_route_str, crd_model_route_str]))
                        if ans == "OK":
                            val.setBackground(0, QtGui.QBrush(QtCore.Qt.green))
                        else:
                            val.setBackground(0, QtGui.QBrush(QtCore.Qt.red))

                    communication_route.addChild(val)

                #
                # OSPFの設定の比較
                #

                if check_ospf:
                    ospf = QtWidgets.QTreeWidgetItem(["ospf"])
                    for node_name in crd[linkfailure_point]["ospf"]:
                        val = QtWidgets.QTreeWidgetItem([node_name])
                        val.addChild(QtWidgets.QTreeWidgetItem(["検証結果", "L2L3通信経路設計記述", "ネットワーク構成モデル"]))

                        ng_count_ospf_val = 0
                        for i in range(len(crd[linkfailure_point]["ospf"][node_name])):
                            crd_val2 = crd[linkfailure_point]["ospf"][node_name][i]
                            crd_model_val2 = ["error", "error", "error"]

                            try:
                                if ("ospf" in crd_model[linkfailure_point] and
                                        node_name in crd_model[linkfailure_point]["ospf"] and
                                        crd_model[linkfailure_point]["ospf"][node_name] is not None):
                                    for j in range(len(crd_model[linkfailure_point]["ospf"][node_name])):
                                        if crd_val2[0] == crd_model[linkfailure_point]["ospf"][node_name][j][0] and crd_val2[1] == \
                                                crd_model[linkfailure_point]["ospf"][node_name][j][1]:
                                            crd_model_val2 = crd_model[linkfailure_point]["ospf"][node_name][j]
                                            break
                            except Exception as e:
                                print(f"error in file {file_name}: {e}")
                                crd_model_val2 = ["error", "error", "error"]

                            ans = "OK"
                            if crd_val2 != crd_model_val2:
                                ans = "NG"

                                for k in range(1, len(data)):
                                    if data[k][0] == node_name:
                                        data[k][1] += 1
                                        if crd_model_val2[2] == "DOWN":
                                            data[k][2] += 1
                                            data[k][4] += 1

                                        if crd_model_val2[2] == "error":
                                            data[k][3] += 1
                                            data[k][4] += 3

                                if crd_model_val2[2] == "DOWN":
                                    for link in all_link_list:
                                        neighbor = ""
                                        if link[0][0] == node_name:
                                            neighbor = link[1][0]
                                        if link[1][0] == node_name:
                                            neighbor = link[0][0]
                                        if neighbor:
                                            for k in range(1, len(data)):
                                                if data[k][0] == neighbor:
                                                    data[k][4] += 1

                                ng_count_ospf_val += 1

                            crd_str = f"{crd_val2[0]}, エリア: {crd_val2[1]}, status: {crd_val2[2]}"
                            crd_model_str = f"{crd_model_val2[0]}, エリア: {crd_model_val2[1]}, status: {crd_model_val2[2]}"
                            val.addChild(QtWidgets.QTreeWidgetItem([ans, crd_str, crd_model_str]))

                        if ng_count_ospf_val == 0:
                            val.setBackground(0, QtGui.QBrush(QtCore.Qt.green))
                        else:
                            val.setBackground(0, QtGui.QBrush(QtCore.Qt.red))
                        ospf.addChild(val)
                        ng_count_ospf += ng_count_ospf_val

                #
                # 各要素を追加
                #

                if check_ospf:
                    qw_tree_parent_item.addChildren(
                        [QtWidgets.QTreeWidgetItem(["設計項目"]), communication_route, ospf])
                file_item.addChild(qw_tree_parent_item)

            ######################################################ルーティングテーブル################################################################
                """
                if check_route_table:
                    routing_table = QtWidgets.QTreeWidgetItem(["routing_table"])
                    for node_name in crd[linkfailure_point]["routing_table"]:
                        val = QtWidgets.QTreeWidgetItem([node_name])
                        val.addChild(QtWidgets.QTreeWidgetItem(["検証結果", "L2L3通信経路設計記述", "ネットワーク構成モデル"]))

                        ng_count_route_table_val = 0
                        for i in range(len(crd[linkfailure_point]["routing_table"][node_name])):
                            crd_val2 = crd[linkfailure_point]["routing_table"][node_name][i]
                            crd_model_val2 = ["error", "error", "error"]

                            try:
                                if ("routing_table" in crd_model[linkfailure_point] and
                                        node_name in crd_model[linkfailure_point]["routing_table"] and
                                        crd_model[linkfailure_point]["routing_table"][node_name] is not None):
                                    for j in range(len(crd_model[linkfailure_point]["routing_table"][node_name])):
                                        if crd_val2[0] == crd_model[linkfailure_point]["routing_table"][node_name][j][0] and crd_val2[1] == \
                                                crd_model[linkfailure_point]["routing_table"][node_name][j][1]:
                                            crd_model_val2 = crd_model[linkfailure_point]["routing_table"][node_name][j]
                                            break
                            except Exception as e:
                                print(f"error in file {file_name}: {e}")
                                crd_model_val2 = ["error", "error", "error"]

                            ans = "OK"
                            if crd_val2 != crd_model_val2:
                                ans = "NG"

                                for k in range(1, len(table_data)):
                                    if table_data[k][0] == node_name:
                                        table_data[k][1] += 1  # エラーカウントのみを増加
                                        break  # 該当ノードが見つかったらループを抜ける

                                ng_count_route_table_val += 1

                            crd_str = f"宛先: {crd_val2[0]}, 次ホップ: {crd_val2[1]}, {crd_val2[2]}"
                            crd_model_str = f"宛先: {crd_model_val2[0]}, 次ホップ: {crd_model_val2[1]}, {crd_model_val2[2]}"
                            val.addChild(QtWidgets.QTreeWidgetItem([ans, crd_str, crd_model_str]))

                        if ng_count_route_table_val == 0:
                            val.setBackground(0, QtGui.QBrush(QtCore.Qt.green))
                        else:
                            val.setBackground(0, QtGui.QBrush(QtCore.Qt.red))
                        routing_table.addChild(val)
                        ng_count_route_table += ng_count_route_table_val
                    """
                    #
                    # 各要素を追加
                    #
                if check_route_table:
                    qw_tree_parent_item.addChildren(
                        [QtWidgets.QTreeWidgetItem(["設計項目"]), communication_route, ospf, routing_table])
                file_item.addChild(qw_tree_parent_item)

            # Add the file_item to the tree
            qw_tree.addTopLevelItem(file_item)

            print(f"\nProcessing file: {file_name}\n")

            # 名前を縦軸に設定してデータフレームを作成（RISK）
            df_risk = pd.DataFrame(data[1:], columns=data[0]).set_index("Router")
            print(df_risk)
            print("------------------------------------------------------------------")

            # 名前を縦軸に設定してデータフレームを作成（SCORE）
            df_score = pd.DataFrame(route_data[1:], columns=route_data[0]).set_index("Router")
            print(df_score)

            print("------------------------------------------------------------------")
            df_risk2 = pd.DataFrame(table_data[1:], columns=table_data[0]).set_index("Router")
            print(df_risk2)

            # Update total NG counts
            ng_count_route_total += ng_count_route
            ng_count_stp_total += ng_count_stp
            ng_count_ospf_total += ng_count_ospf
            ng_count_route_table_total += ng_count_route_table

            # dataのRISKをrisk_dfに追加、列名をdevice_nameに変更
            risk_df[device_name] = df_risk['RISK']
            # route_dataのSCOREをscore_dfに追加、列名をdevice_nameに変更
            score_df[device_name] = df_score['SCORE']
            # dataのRISKをrisk_dfに追加、列名をdevice_nameに変更
            risk2_df[device_name] = df_risk2['RISK2']

        # 全ファイル処理後に、risk_dfとscore_dfを表示
        print("\nCombined RISK Table across all files:\n")
        print(risk_df)

        print("\nCombined SCORE Table across all files:\n")
        print(score_df)

        print("\nCombined RISK2 Table across all files:\n")
        print(risk2_df)

        file_path = "izawa_memo.txt"
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        return [ng_count_route_total, ng_count_stp_total, ng_count_ospf_total]


if __name__ == '__main__':
    app = QApplication(sys.argv)    # PySide6の実行
    window = MainWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了
