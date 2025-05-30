import yaml

#file_path = "../communication_root/crd-ospf-9_IZAWA_Cf4NotOSPF.yaml"
#file_path = "../communication_root/crd-ospf-9_IZAWA_NoMistake.yaml"
#file_path = "../communication_root/crd-ospf-9_IZAWA_NoMistake_test.yaml"
file_path = "../izawa_result/cmd_kiki_ int_Cf4.yaml"
#file_path = "../communication_root/crd-ospf-9_IZAWA_Cf4IntNotOSPF.yaml"
#file_path = "../communication_root/crd-ospf-9_IZAWA_Cf4Cf6SameRouterId.yaml"
#file_path = "../communication_root/crd-ospf-9_IZAWA_Cf5Cf6SameRouterId.yaml"
#file_path = "../communication_root/crd-ospf-9_IZAWA_Cf3Cf6SameRouterId.yaml"
#file_path = "../communication_root/crd-ospf-9_IZAWA_Cf3Cf6SameRouterId_Cf4IntNotOSPF.yaml"

# YAMLファイルを読み込む
with open(file_path, 'r') as file:
    data = yaml.safe_load(file)

# すべてのキーの値を空にする
def clear_values(d):
    for key in d:
        if isinstance(d[key], dict):  # キーの値が辞書の場合、再帰的に処理
            clear_values(d[key])
        else:  # キーの値が辞書でない場合、空にする
            d[key] = None

clear_values(data)

# 変更をファイルに書き戻す
with open(file_path, 'w') as file:
    yaml.dump(data, file, default_flow_style=False)