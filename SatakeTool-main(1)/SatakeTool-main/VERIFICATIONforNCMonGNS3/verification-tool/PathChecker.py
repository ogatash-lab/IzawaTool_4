import os

def check_path_exists(path):
    # パスが存在するかどうかを確認
    if os.path.exists(path):
        print(f"指定されたパス '{path}' は存在します。")
    else:
        print(f"指定されたパス '{path}' は存在しません。")

# 使用例
check_path_exists("VERIFICATIONforNCMonGNS3/verification-tool")
