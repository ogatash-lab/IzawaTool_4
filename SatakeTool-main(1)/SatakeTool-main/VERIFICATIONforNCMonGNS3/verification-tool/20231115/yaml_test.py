import yaml

# YAMLファイルを読み込む
def read_yaml_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        print("読み込んだデータ:", data)
    return data

# YAMLファイルにデータを書き込む
def write_yaml_file(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)
    print("データを保存しました。")

# 使用例
if __name__ == "__main__":
    # YAMLファイルのパス
    filepath = 'example.yaml'

    # YAMLファイルを読み込む
    data = read_yaml_file(filepath)

    # データを変更する
    data['new_key'] = 'new_value'

    # 変更したデータを保存する
    write_yaml_file(filepath, data)