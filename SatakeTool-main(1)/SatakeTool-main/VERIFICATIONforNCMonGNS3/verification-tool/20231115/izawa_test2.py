import os

# 指定するフォルダーのパス
folder_path = 'test_txt'

# フォルダー内のファイルを走査
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                consecutive_count = 0
                for line in file:
                    # 行に '*  *  *' が含まれているかチェック
                    if '*  *  *' in line.strip():
                        consecutive_count += 1
                        # 2回連続して現れたらファイル名を出力して終了
                        if consecutive_count >= 2:
                            print(f"'{filename}' は条件を満たします。")
                            break
                    else:
                        consecutive_count = 0  # リセット
        except Exception as e:
            print(f"'{filename}' の読み込み中にエラーが発生しました: {e}")
