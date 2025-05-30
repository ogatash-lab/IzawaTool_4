"""
提案ツールを実行するために、特定のフォルダ内のファイルを削除するコード
検証後のyamlファイルとtime_count.txtの内容
"""

import os
import shutil

def remove():
    root_path = "VERIFICATIONforNCMonGNS3/verification-tool/"
    target_dir_list = ["kikisettei", "link_create_info", "node_create_info/kiki_create_info", "node_create_info/vpcs_create_info"]
    #target_dir_list += ["linkfailure-log/sh_ip_ospf_interface_brief", "linkfailure-log/traceroute"]

    for i in range(len(target_dir_list)):
        shutil.rmtree(root_path + target_dir_list[i])
        os.makedirs(root_path + target_dir_list[i])

"""
shutil.rmtree(root_path + "cmd_node/cmd_kiki")
os.mkdir(root_path + "cmd_node/cmd_kiki")
"""