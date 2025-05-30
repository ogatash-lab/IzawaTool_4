import shutil
import yaml


# yaml_file_root = 'VERIFICATIONforNCMonGNS3/verification-tool/communication_root/'
crd_folder_path = 'VERIFICATIONforNCMonGNS3/verification-tool/communication_root/'

# 
def main(crd_name):

    # モデル用の通信経路仕様を作成
    crd_model_create(crd_name)

    with open(crd_folder_path + crd_name) as file:
        yml = yaml.safe_load(file)
    return 0

# ネットワーク構成モデルの通信経路を示す用のyamlファイルを複製
def crd_model_create(crd_name):
    # 理想のyamlファイルを複製して、それを編集する形でモデルの経路を反映させる
    crd_name_model = crd_name + "_model.yaml"
    shutil.copyfile(crd_folder_path + crd_name, crd_folder_path + crd_name_model)
    return 0 