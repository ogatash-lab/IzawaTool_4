import PySide6
from PySide6 import QtCore
from PySide6 import QtWidgets
import os
import sys
import yaml
import time_count

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget


time_filename = "VERIFICATIONforNCMonGNS3/verification-tool/time_count.txt"

# 環境変数にPySide6を登録
dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class MainWindow(QWidget):
    root_ideal = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/3Cf-3Cl-ring-ideal.yaml"
    root_test = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/3Cf-3Cl-ring-test.yaml"

    with open(root_ideal) as file:
        yml_ideal = yaml.safe_load(file)

    with open(root_test) as file:
        yml_test = yaml.safe_load(file)
    
    print('ok')

    def __init__(self, parent=None):
        # 親クラスの初期化
        super().__init__(parent)
        # ウィンドウタイトル
        self.setWindowTitle("検証結果表")

        # ウィンドウサイズを指定（px単位）
        windowWidth = 1000  # ウィンドウの横幅
        windowHeight = 800  # ウィンドウの高さ

        root_ideal = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/3Cf-3Cl-ring-ideal.yaml"
        root_test = "VERIFICATIONforNCMonGNS3/verification-tool/communication_root/3Cf-3Cl-ring-test.yaml"
        with open(root_ideal) as file:
            yml_ideal = yaml.safe_load(file)
        with open(root_test) as file:
            yml_test = yaml.safe_load(file)

        # ウィンドウサイズの変更
        self.resize(windowWidth, windowHeight)

        # ラベルを表示するメソッド
        ng_count = self.SetTree(yml_ideal, yml_test)

        self.SetLabel(yml_ideal, yml_test, ng_count)


    # ラベルは別のメソッドに分けました
    def SetLabel(self, yml_ideal, yml_test, ng_count):
        # ラベルを使うことを宣言（引数のselfはウィンドウのことで、ウィンドウにラベルが表示されます）

        execution_time = QtWidgets.QLabel(self)
        
        # ラベルに文字を指定
        time_count.culcurate_time(time_filename)
        execution_time.setText("実行時間: " + time_count.culcurate_time(time_filename))
        execution_time.move(10, 0)

        # yamlファイルから合計を取得すればいいかな
        num = 0
        for i in range(len(yml_ideal)):
            num += len(list(yml_ideal[i].values())[0])

        testcase_total = QtWidgets.QLabel(self)
        testcase_total.setText("runs: " + str(num))
        testcase_total.move(10, 15)


        # 経路が異なるものの合計
        failures = QtWidgets.QLabel(self)
        failures.setText("failures: " + str(ng_count))
        failures.move(150, 15)

        # 検証できなかった場合、どんなパターンがあるかな
        # errors = QtWidgets.QLabel(self)
        # errors.setText("errors: " + str(0))
        # errors.move(290, 15)

    # ツリーのウィジェット
    def SetTree(self, yml_ideal, yml_test):
        ng_count = 0
        qw_tree = QtWidgets.QTreeWidget(self)
        # QtWidgets.QTreeWidgetItem.sizeHint(200)
        
        # 最初からツリーの中を表示するかどうか
        # qw_tree.expandAll()
        qw_tree.resize(1000, 800)
        qw_tree.move(0, 30)
        qw_tree.header().resizeSection(1000, 1000)
        qw_tree.header().setStretchLastSection(False)
        qw_tree.setHeaderLabels(["検証結果", "通信区間", "通信経路(通信経路の仕様)", "通信経路(ネットワーク構成モデル)"])

        # ここで試験結果に表示する項目を追加するか否かのfor分を回すかな
        for i in range(len(yml_ideal)):
            linkfailure_point = str(list(yml_ideal[i].keys())[0])
            print(linkfailure_point)
            qw_tree_parent_item = QtWidgets.QTreeWidgetItem([linkfailure_point])
            for j in range(len(list(yml_ideal[i].values())[0])):
                communication_node = list(yml_ideal[i][linkfailure_point][j].keys())[0]
                communication_root_ideal = list(list(yml_ideal[i].values())[0][j].values())[0]
                communication_root_test = list(list(yml_test[i].values())[0][j].values())[0]
                
                # 設計者の意図と，モデルの設計の通信経路が等しいか比較する
                if communication_root_ideal == communication_root_test:
                    judge = "OK"
                else:
                    judge = "NG"
                    ng_count += 1
                
                # リストだと表示されないみたいだからテキストに直す
                communication_root_ideal_str = ""
                for k in range(len(communication_root_ideal)):
                    communication_root_ideal_str += communication_root_ideal[k]
                    if len(communication_root_ideal) != k + 1:
                        communication_root_ideal_str += " -> "

                communication_root_test_str = ""
                for k in range(len(communication_root_test)):
                    communication_root_test_str += communication_root_test[k]
                    if len(communication_root_test) != k + 1:
                        communication_root_test_str += " -> "

                append_list = [judge, communication_node, communication_root_ideal_str, communication_root_test_str]
                print("append_list = ")
                print(append_list)
                qw_tree_parent_item.addChild(QtWidgets.QTreeWidgetItem(append_list))
                qw_tree.addTopLevelItem(qw_tree_parent_item)
        print(ng_count)
        return ng_count


app = QApplication(sys.argv)    # PySide6の実行
window = MainWindow()           # ユーザがコーディングしたクラス
window.show()                   # PySide6のウィンドウを表示
sys.exit(app.exec())            # PySide6の終了
