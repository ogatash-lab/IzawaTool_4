import csv
import functools
print = functools.partial(print, flush=True)


"""
機器設定手順を回してcsvを回す
機器設定コマンドに対応するsortnumを取得して整形する
上のmodalがTrueのコマンドから下のexitまで
"""

def sort_cmd_cisco3725(all_file_num):
    csv_sort_list = []
    filename_csv = 'VERIFICATIONforNCMonGNS3/input/cmd_cisco3725ESW.csv'
    with open(filename_csv, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if row[6] == "TRUE":
                # row[5]の<>の要素を削除する
                # 例)interface fastethernet <slot>/<port>
                # interface fastethernet
                slice_num = 0
                if "<" in row[5]:
                    for moji in row[5]:
                        if moji == "<":
                            break
                        slice_num += 1
                    row_ins = row[5][0:slice_num]
                else:
                    row_ins = row[5]
                csv_sort_list.append([row[9], row_ins])
    # print(csv_sort_list)

    #検証中のフォルダ名取得
    filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        selected_folder = file.read()
    # modalがTRUEのとこからコマンドと順序も取ってきて、リスト内のリストのコマンドだけ一番最後のコマンドで並び変えれば？
    # コマンド手順をリスト化 [enable, conf t, [], [], hostname, []]
    filename_cmd = 'VERIFICATIONforNCMonGNS3/verification-tool/cmd_node/' + selected_folder
    for i in range(all_file_num):
        # modalがTRUEかFALSEか判断用の番号
        true_count = 0
        # 機器設定手順をリスト化する　後でファイルに書きなおす用
        cmd_list = []
        # このリストにmodal=True～exitまで追加する
        append_list = []

        filename = filename_cmd + "/cmd_kiki_Cf" + str(i + 1) + ".txt"
        with open(filename, "r", encoding='shift-jis') as line:
            #f = line.read()
            #print(f)
            for k in line:
                # print("k = ", k)
                if true_count == 0:
                    for j in range(len(csv_sort_list)):
                        # print("num j = " + str(j))
                        if csv_sort_list[j][1] in k:
                            # print("1")
                            append_list.append(csv_sort_list[j][0])
                            append_list.append(k)
                            true_count = 1
                            break
                    if true_count == 0:
                        cmd_list.append(k)
                        # print('4 cmd_list = ')
                        # print(cmd_list)

                # リストの中のリストのexitの場合
                elif true_count == 1 and "exit" in str(k):
                    # print("3")
                    true_count = 0
                    append_list.append(k)
                    cmd_list.append(append_list)
                    # print("append_list =", append_list)
                    # print("cmd_list =", cmd_list)
                    append_list = []

                # リストの中のリストに書くべきコマンドの場合
                elif true_count == 1:
                    # print("2")
                    append_list.append(k)
                    # print('4 cmd_list = ')
                    # print(cmd_list)

        print("filename = " + filename)
        print("cmd_list = ", cmd_list)
        print("")

        switch_list = []
        # cmd_listの何番目のリストで，何番の優先度なのかを保存する
        for num in range(len(cmd_list)):
            if type(cmd_list[num]) is str:
                print('string')
            else:
                # 何番目のリスト？，そのコマンドの優先度は？
                switch_list.append([num, int(cmd_list[num][0])])


        print(switch_list)
        for val in cmd_list:
            print(val)
        # switch_listと連動させてcmd_listも整地する
        num = 0
        while True:
            # 並び替え終えたと判断する条件　whileを抜ける
            if num == len(switch_list) - 1:
                print('while end')
                break
            # ただ配列を入れ替えただけだと，入れ替えた結果が保存されていない
            if switch_list[num][1] > switch_list[num + 1][1]:
                
                # cmd_list[switch_list[num][0]], cmd_list[switch_list[num + 1][0]] = cmd_list[switch_list[num + 1][0]], cmd_list[switch_list[num][0]]

                dummy_list = cmd_list[switch_list[num][0]]
                cmd_list[switch_list[num][0]] = cmd_list[switch_list[num + 1][0]]
                cmd_list[switch_list[num + 1][0]] = dummy_list

                switch_list[num][1], switch_list[num + 1][1] = switch_list[num + 1][1], switch_list[num][1]
                # 初めからやり直し
                num = 0

                print(switch_list)
                for val in cmd_list:
                    print(val)
                print('-------------------------------')
            else:
                num += 1

        print(switch_list)
        for val in cmd_list:
            print(val)

        print('end----------------------------------')

        # 終えたらファイルに書き込む
        # cmd_listのリストを番号を抜いて1つのリストにまとめる
        with open(filename, "w", encoding='shift-jis') as line:
            for num in range(len(cmd_list)):
                # おそらく文字列だと判定されていない
                if type(cmd_list[num]) is str:
                    line.write(cmd_list[num])
                else:
                    for num2 in range(len(cmd_list[num]) - 1):
                        line.write(cmd_list[num][num2 + 1])
