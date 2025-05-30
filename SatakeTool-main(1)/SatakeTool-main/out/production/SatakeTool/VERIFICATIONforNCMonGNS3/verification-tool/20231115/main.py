import os
import yaml
import shutil

import gns3_network_build
# import communication_root_design
import protocol_status_coding
import gns3_network_linkfailure
import izawa_linkfailure
import file_remove
import time_count

# gns3のプロジェクトのID
project_id = "acbe138d-1064-45c9-9248-f7b1bf97bf2c"

# 実行時間 計測開始
time_count_file_name = "VERIFICATIONforNCMonGNS3/verification-tool/20231115/time_count.txt"
time_count.count_start(time_count_file_name)

is_file_remove = True
if is_file_remove:
    file_remove.remove()


################################################################################################
is_GNS3_build = True


dynamips_num = 0
dynamips_name_id_list = []
vpcs_name_id_list = []
#vpcs_name_ip_list = []
vpcs_name_ip_list = [['Cl9', '10.0.17.1'], ['Cl7', '10.0.15.1'], ['Cl3', '10.0.11.1'], ['Cl2', '10.0.18.2'], ['Cl1', '10.0.19.1'], ['Cl5', '10.0.13.1'], ['Cl6', '10.0.14.1'], ['Cl4', '10.0.12.1'], ['Cl8', '10.0.16.1']]
all_link_list = []
"""
dynamips_num=9
dynamips_name_id_list=[['5018', 'Cf1', '6b151a30-ef92-420a-bfd5-e8cbd9ec8451'], ['5019', 'Cf2', '46534973-92d8-483e-b07e-d5a0c1a7f352'], ['5020', 'Cf3', '0d933cf1-f4af-4b78-82ea-29bde88e3fe4'], ['5021', 'Cf4', '6af2a1d5-bcc0-4183-a89d-ad60c8d209ed'], ['5022', 'Cf5', '509ea907-02b9-4ad5-b30a-b0531485b992'], ['5023', 'Cf6', 'dd34ad91-4694-4693-ab71-17ec75457ad9'], ['5024', 'Cf7', '9875e126-ff73-4ccf-98f1-f2ed05e8589a'], ['5025', 'Cf8', '829537c2-6864-4cbf-9842-c76bf13e7c50'], ['5026', 'Cf9', 'd6b1d488-2111-4584-9e3a-bed262e1ae02']]
vpcs_name_id_list=[['5000', 'Cl1', '294aa1b0-89a1-48b0-bac1-654b15d30a3b'], ['5002', 'Cl2', 'b39f2a6a-9dd2-42c5-b545-1f7fd00990a8'], ['5004', 'Cl3', '48c56ac2-7f1e-4e0e-9303-06fe3d4648bd'], ['5006', 'Cl4', 'cbbe9467-ac21-4fe8-8558-0bd9ba9e0f51'], ['5008', 'Cl5', '05668757-dece-4757-ac97-70a93fee5700'], ['5010', 'Cl6', '46ebcea8-9d0f-4363-baf6-73f1e91e2b56'], ['5012', 'Cl7', '6bb923fa-be58-49be-a46f-a761977d4c9e'], ['5014', 'Cl8', 'c2d9cb3e-89ee-48c3-bcbb-5f009edb7f32'], ['5016', 'Cl9', '0ed17987-864a-49bd-b04a-297524aa6fdb']]
vpcs_name_ip_list=[['Cl4', '10.0.12.1'], ['Cl5', '10.0.13.1'], ['Cl9', '10.0.17.1'], ['Cl1', '10.0.19.1'], ['Cl7', '10.0.15.1'], ['Cl8', '10.0.16.1'], ['Cl3', '10.0.11.1'], ['Cl2', '10.0.18.2'], ['Cl6', '10.0.14.1']]
all_link_list=[[['Cl9', '0', '0'], ['Cf9', '1', '15'], '336ab1de-97f9-44cc-9cac-ac7f92f6443a'], [['Cf2', '1', '10'], ['Cf6', '1', '10'], '058c576d-0b05-440c-8d33-f7ba602701a2'], [['Cf1', '1', '2'], ['Cf2', '1', '2'], '32657736-9bae-4de5-b4ba-98bc8fd03775'], [['Cf3', '1', '4'], ['Cf4', '1', '4'], '575a42be-a027-4a4b-92de-166a8cfad032'], [['Cl6', '0', '0'], ['Cf6', '1', '15'], '5e8f3511-f772-49bd-adaf-337f3429e49e'], [['Cf8', '1', '9'], ['Cf9', '1', '9'], '3d8a6bea-d574-4b37-ae47-1a0ab1b8d97b'], [['Cl7', '0', '0'], ['Cf7', '1', '15'], '256e65dc-0353-4574-93c8-44cef182c14a'], [['Cf6', '1', '7'], ['Cf7', '1', '7'], '85e9950c-75a1-42f4-bb95-5637f3234b59'], [['Cf2', '1', '4'], ['Cf9', '1', '4'], '52165f18-d8f1-4db1-93aa-8e8b1fea8fd9'], [['Cl5', '0', '0'], ['Cf5', '1', '15'], 'df4a2f7f-2718-4da9-a944-0a74f034b3c3'], [['Cf5', '1', '6'], ['Cf6', '1', '6'], 'bef91e54-27d2-4417-946f-323a90062c3f'], [['Cl2', '0', '0'], ['Cf2', '1', '15'], 'fd431488-2f07-4fd8-b1a8-cde6684b9a0b'], [['Cl8', '0', '0'], ['Cf8', '1', '15'], '5a1dad85-12b4-4a5c-914f-049ea238c8d0'], [['Cl3', '0', '0'], ['Cf3', '1', '15'], '94628018-c6c8-45fd-a0ba-1b1d7ae99e02'], [['Cf7', '1', '8'], ['Cf8', '1', '8'], 'd8494768-c958-42fe-992f-e6425718f65b'], [['Cl1', '0', '0'], ['Cf1', '1', '15'], 'cddb5c36-7875-4b16-a0a0-42fc7a03b017'], [['Cf2', '1', '3'], ['Cf3', '1', '3'], 'd5dd2b70-af8f-4efb-bc7e-8300b1e123fc'], [['Cl4', '0', '0'], ['Cf4', '1', '15'], 'e8313910-d006-41d5-9831-e710a7c92a7b'], [['Cf4', '1', '5'], ['Cf5', '1', '5'], 'da163593-30d9-4974-9843-b1790549304e']]
"""
if is_GNS3_build:
    #vpcs_name_ip_list = []
    # gns3のネットワークを構築する
    dynamips_num, dynamips_name_id_list, vpcs_name_id_list, vpcs_name_ip_list, all_link_list = gns3_network_build.gns3_network_build(project_id)
    #ここがGNS３の実行箇所
################################################################################################
#キャプチャを行うか？
capture_ospf = True

## 網羅的に検証する
# 何を検証する？
check_route_l2 = False
check_route_l3 = True #ip
check_stp = False
check_ospf = True


#検証中のフォルダ名取得
filename = 'VERIFICATIONforNCMonGNS3/verification-tool/20231115/folder_name.txt'
with open(filename, 'r', encoding='utf-8') as file:
    selected_folder = file.read()

if capture_ospf:
    # 親ディレクトリのパスを指定
    parent_dir_path = 'VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/' + selected_folder

    # 親ディレクトリと同じ名前のディレクトリが既に存在する場合は削除
    if os.path.exists(parent_dir_path):
        shutil.rmtree(parent_dir_path)

    # 親ディレクトリを作成
    os.makedirs(parent_dir_path)

    # 子ディレクトリの名前を指定
    child_dir1 = os.path.join(parent_dir_path, 'sh_ip_ospf_interface_brief')
    child_dir2 = os.path.join(parent_dir_path, 'traceroute')
    #child_dir3 = os.path.join(parent_dir_path, 'sh_ip_route')

    # 子ディレクトリを作成
    os.makedirs(child_dir1)
    os.makedirs(child_dir2)
    #os.makedirs(child_dir3)

    izawa_linkfailure.ospf(project_id, dynamips_num, dynamips_name_id_list, vpcs_name_id_list, vpcs_name_ip_list, all_link_list) #リンク障害発生前のキャプチャ
    gns3_network_linkfailure.ospf(project_id, dynamips_num, dynamips_name_id_list, vpcs_name_id_list, vpcs_name_ip_list, all_link_list) #リンク障害発生後のキャプチャ

    #yamlファイル作成
    # コピー元のファイルパスを指定
    #結線なし
    #original_file = './VERIFICATIONforNCMonGNS3/verification-tool/izawa_result/crd-ospf-9_IZAWA_original.yaml'

    #2-6結線
    original_file = './VERIFICATIONforNCMonGNS3/verification-tool/izawa_result/crd-ospf-9_IZAWA_original_test.yaml'

    # コピー先のファイルパス（同じディレクトリで名前を変更）
    new_file = './VERIFICATIONforNCMonGNS3/verification-tool/izawa_result/' + selected_folder + '.yaml'

    # ファイルをコピー
    try:
        if os.path.exists(original_file):
            shutil.copy(original_file, new_file)
        else:
            print(f'コピー元のファイルが存在しません: {original_file}')
    except Exception as e:
        print(f'ospfの作成でエラーが発生しました: {e}')

"""
#l2の検証に利用するキャプチャファイルの生成も兼ねる
if check_stp:
    gns3_network_linkfailure.stp(project_id, dynamips_num, dynamips_name_id_list, vpcs_name_id_list, vpcs_name_ip_list, all_link_list)
"""

################################################################################################

# 最初に辞書型の値として記憶させる
"""
none = "none"
with open(yaml_file_name, 'w') as f:
    data = {none: None}
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
"""

# 
# communication_route に関してyamlにまとめる
# 

# test
# all_link_list = [[['Cf1', '1', '1'], ['Cf3', '1', '0'], '9845f684-9573-4448-aaa2-de951435692a'], [['Cf2', '1', '15'], ['Cl2', '0', '0'], 'df2d79ce-43fd-409d-84cb-893d7f62252f'], [['Cf1', '1', '0'], ['Cf2', '1', '1'], 'c431ba79-d704-4aaf-8254-80482d5fa248'], [['Cl1', '0', '0'], ['Cf1', '1', '15'], 'dc42c664-0882-40cc-b8b4-68c032e7183c'], [['Cf3', '1', '15'], ['Cl3', '0', '0'], '3cce2834-08c0-4211-afd8-9cb37fc8322a'], [['Cf2', '1', '0'], ['Cf3', '1', '1'], '106e625e-6174-4a1b-834d-6c5c4bc00e33']]
# vpcs_name_ip_list = [['Cl2', '192.168.1.2'], ['Cl3', '192.168.1.3'], ['Cl1', '192.168.1.1']]

# ospf
# all_link_list = [[['Cf5', '1', '6'], ['Cf6', '1', '6']], [['Cl9', '0', '0'], ['Cf9', '1', '15']], [['Cf4', '1', '5'], ['Cf5', '1', '5']], [['Cf6', '1', '7'], ['Cf7', '1', '7']], [['Cf1', '1', '2'], ['Cf2', '1', '2']], [['Cl3', '0', '0'], ['Cf3', '1', '15']], [['Cl5', '0', '0'], ['Cf5', '1', '15']], [['Cl8', '0', '0'], ['Cf8', '1', '15']], [['Cl4', '0', '0'], ['Cf4', '1', '15']], [['Cl7', '0', '0'], ['Cf7', '1', '15']], [['Cl2', '0', '0'], ['Cf2', '1', '15']], [['Cf2', '1', '3'], ['Cf3', '1', '3']], [['Cl6', '0', '0'], ['Cf6', '1', '15']], [['Cl1', '0', '0'], ['Cf1', '1', '15']], [['Cf7', '1', '8'], ['Cf8', '1', '8']], [['Cf3', '1', '4'], ['Cf4', '1', '4']], [['Cf2', '1', '4'], ['Cf9', '1', '4']], [['Cf8', '1', '9'], ['Cf9', '1', '9']]]
# vpcs_name_ip_list = [['Cl6', '10.0.14.1'], ['Cl2', '10.0.18.2'], ['Cl9', '10.0.17.1'], ['Cl1', '10.0.19.1'], ['Cl8', '10.0.16.1'], ['Cl3', '10.0.11.1'], ['Cl5', '10.0.13.1'], ['Cl4', '10.0.12.1'], ['Cl7', '10.0.15.1']]

# all_link_list = [[['Cl2', '0', '0'], ['Cf2', '1', '15'], '5b82716a-94ad-49f5-b948-d7b513462167'], [['Cl4', '0', '0'], ['Cf4', '1', '15'], 'b81acf6d-52dd-4998-a7da-dfa10ac2739a'], [['Cl3', '0', '0'], ['Cf3', '1', '15'], '0b2e86f7-7fbb-4c05-a964-d42ae62d9521'], [['Cl7', '0', '0'], ['Cf7', '1', '15'], '2db34220-89a2-4323-9ee0-a03406625953'], [['Cl8', '0', '0'], ['Cf8', '1', '15'], '253379dc-4490-46fa-a05e-783ba3fd18ce'], [['Cf3', '1', '4'], ['Cf4', '1', '4'], '2d16e561-5509-4e8e-9b96-a3447b33e916'], [['Cl9', '0', '0'], ['Cf9', '1', '15'], '99887e53-da91-4775-9ac2-3716dd6f2596'], [['Cf4', '1', '5'], ['Cf5', '1', '5'], '960fb17f-43e6-4308-b95d-ff7e6666aee1'], [['Cf6', '1', '7'], ['Cf7', '1', '7'], 'c106ae87-e4b0-4c3d-8073-b201cf60554a'], [['Cf5', '1', '6'], ['Cf6', '1', '6'], 'a89dd43d-6c29-45c0-8564-4c29f58dcee4'], [['Cf8', '1', '9'], ['Cf9', '1', '9'], 'f2046de3-2c9d-4229-9fbd-2effed243f7d'], [['Cf1', '1', '2'], ['Cf2', '1', '2'], 'bf05b5ea-8b59-468a-8c46-0165d20edcbf'], [['Cf2', '1', '3'], ['Cf3', '1', '3'], '647e7baf-3951-49d8-b403-eb5fbb9cc630'], [['Cl6', '0', '0'], ['Cf6', '1', '15'], 'f0b45ad4-26e2-4574-be19-b3e0dc935c2c'], [['Cf2', '1', '4'], ['Cf9', '1', '4'], '0bcf9c9b-07ca-4f55-85b1-8eb2dbaedba8'], [['Cl1', '0', '0'], ['Cf1', '1', '15'], 'd8a7516c-51fd-466a-9d43-4423757dab84'], [['Cf7', '1', '8'], ['Cf8', '1', '8'], '3b79af7d-3358-4c80-88c1-2918b204573f'], [['Cl5', '0', '0'], ['Cf5', '1', '15'], '66fe97a0-f1b1-421a-9762-8eb1b89d8c4e']]
# vpcs_name_ip_list = [['Cl9', '10.0.17.1'], ['Cl6', '10.0.14.1'], ['Cl1', '10.0.19.1'], ['Cl3', '10.0.11.1'], ['Cl7', '10.0.15.1'], ['Cl4', '10.0.12.1'], ['Cl2', '10.0.18.1'], ['Cl8', '10.0.16.1'], ['Cl5', '10.0.13.1']]

print("Enter")

## 通信経路仕様と比較して結果を出力する
# 通信経路仕様のファイル名
# 設計者が理想とする各機器の状態を表すファイル
#crd_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-stp-9.yaml"
crd_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9.yaml"
#GNS3で障害を発生させ検証した結果（機器の状態）
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_IZAWA_Cf4NotOSPF.yaml"
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_IZAWA_NoMistake_test.yaml"
yaml_file_name  = "./VERIFICATIONforNCMonGNS3/verification-tool/izawa_result/" + selected_folder + ".yaml"
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_IZAWA_Cf4IntNotOSPF.yaml"
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_IZAWA_Cf4Cf6SameRouterId.yaml"
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_IZAWA_Cf5Cf6SameRouterId.yaml"
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_IZAWA_Cf3Cf6SameRouterId.yaml"
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_IZAWA_Cf3Cf6SameRouterId_Cf4IntNotOSPF.yaml"
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-ospf-9_IZAWA_NoMistake.yaml"
#yaml_file_name = "./VERIFICATIONforNCMonGNS3/verification-tool/communication_root/crd-stp-9_model.yaml"

#crd_name = "../communication_root/crd-stp-9.yaml"
#yaml_file_name = "../communication_root/crd-stp-9_model.yaml"

#all_link_list = [[['Cl6', '0', '0'], ['Cf6', '1', '15']], [['Cf4', '1', '5'], ['Cf5', '1', '5']], [['Cf8', '1', '9'], ['Cf9', '1', '9']], [['Cf2', '1', '3'], ['Cf3', '1', '3']], [['Cl7', '0', '0'], ['Cf7', '1', '15']], [['Cl9', '0', '0'], ['Cf9', '1', '15']], [['Cf7', '1', '8'], ['Cf8', '1', '8']], [['Cf1', '1', '2'], ['Cf2', '1', '2']], [['Cl8', '0', '0'], ['Cf8', '1', '15']], [['Cf3', '1', '4'], ['Cf4', '1', '4']], [['Cl1', '0', '0'], ['Cf1', '1', '15']], [['Cf6', '1', '7'], ['Cf7', '1', '7']], [['Cf2', '1', '4'], ['Cf9', '1', '4']], [['Cl5', '0', '0'], ['Cf5', '1', '15']], [['Cl2', '0', '0'], ['Cf2', '1', '15']], [['Cf5', '1', '6'], ['Cf6', '1', '6']], [['Cl3', '0', '0'], ['Cf3', '1', '15']], [['Cl4', '0', '0'], ['Cf4', '1', '15']]]
#vpcs_name_ip_list = [['Cl9', '10.0.50.9'], ['Cl1', '10.0.50.1'], ['Cl2', '10.0.50.2'], ['Cl8', '10.0.50.8'], ['Cl7', '10.0.50.7'], ['Cl4', '10.0.50.4'], ['Cl5', '10.0.50.5'], ['Cl6', '10.0.50.6'], ['Cl3', '10.0.50.3']]

if check_route_l2:
    print("ok")

    # どうせ全てのプロトコルを検証してyamlに記録するんだから、yamlで定義しているプロトコルを全部リストにしてもいいかも
    protocol = "icmp"

    path = "test"
    #C:\Users\yukiy\GNS3\projects\test\project-files\captures
    folder_path = "C:/Users/yukiy/GNS3/projects/" + path + "/project-files/captures/"
    #指定されたディレクトリパス（folder_path）内の全てのファイルとディレクトリの名前をリストとして返します。
    files = os.listdir(folder_path)

    #読み書きモード（r+）で開いています。with ステートメントを使用することで、ファイル操作が完了した後にファイルが適切に閉じられることが保証されます。
    with open(crd_name, 'r+') as f:
        data = yaml.safe_load(f)
        crd_linkfailure_point_list = list(data.keys()) #リンク障害を発生させるルータ間
    print(crd_linkfailure_point_list)

    with open(crd_name, 'r+') as f:
        data = yaml.safe_load(f)
        for val in crd_linkfailure_point_list:
            crd_section_list = list(data[val]["communication-route"].keys()) #通信の検証を行うPC間
    print(crd_section_list)


    # pcap のファイルを一つずつ回す
    # for file_name in files:
    #     protocol_status_coding.communication_route_l2(file_name, yaml_file_name, all_link_list, vpcs_name_ip_list, folder_path, protocol)

    # 通信区間のリストとpcapのリストを送る
    for linkfailure_point in crd_linkfailure_point_list:
        print("linkfailure_point = " + linkfailure_point)
        print(len(crd_linkfailure_point_list))
        for i in range(len(crd_section_list)):
            protocol_status_coding.communication_route_l2(folder_path, files, linkfailure_point, crd_section_list[i], yaml_file_name, all_link_list, vpcs_name_ip_list, protocol, crd_linkfailure_point_list)

#------------------------------------------------------------------------------------------------------------------------------------------------------
#check_route_l3
if check_route_l3:

    protocol = "icmp"
    folder_path = ""
    # tracerouteフォルダとyamlなどを入力する
    # dynamips と ip のリストは関数の方で決める
    protocol_status_coding.communication_route_l3(crd_name, vpcs_name_ip_list, yaml_file_name, protocol)

# 
# stpに関する状態のフォルダ
# 


if check_stp:
    folder_path = "VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/sh_spanning-tree_brief/"
    files = os.listdir(folder_path)

    for file_name in files:
        protocol_status_coding.stp(file_name, yaml_file_name)


#
# ospfに関する状態のフォルダ
#
#check_ospf
#if capture_ospf:
if check_ospf:
    folder_path = "VERIFICATIONforNCMonGNS3/verification-tool/linkfailure-log/" + selected_folder + "/sh_ip_ospf_interface_brief/"
    files = os.listdir(folder_path)

    for file_name in files:
        print(file_name)
        protocol_status_coding.ospf(file_name, yaml_file_name)
        #protocol_status_coding.route_table(file_name, yaml_file_name)

# communication_root_design.main(crd_name)
# 通信経路仕様の形があれでいいか決めかねてるから開発しようがなくない？

# 実行時間
time_count.count_stop(time_count_file_name)