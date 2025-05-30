import os
import filecmp

def list_text_files(directory):
    """ 指定されたディレクトリ内のすべてのテキストファイルのリストを返す """
    files = []
    for item in os.listdir(directory):
        if item.endswith('.txt'):
            files.append(os.path.join(directory, item))
    return files

def compare_files(files1, files2):
    """ 二つのファイルリストを比較し、内容が一致しているか確認する """
    paired_files = zip(sorted(files1), sorted(files2))
    all_match = True
    for file1, file2 in paired_files:
        if not filecmp.cmp(file1, file2, shallow=False):
            print(f"ファイル{file2} は一致しません。")
            all_match = False
    return all_match

def compare_folders(folder1, folder2):
    """ 二つのフォルダ内のテキストファイルを比較する """
    files1 = list_text_files(folder1)
    files2 = list_text_files(folder2)

    if len(files1) != len(files2):
        print("ファイルの数が一致しません。")
        return False

    if compare_files(files1, files2):
        print("両方のフォルダ内のすべてのテキストファイルが一致しています。")
        return True
    else:
        print("一部のファイルが一致しません。")
        return False

# フォルダパスを指定
folder1 = '../cmd_node/cmd_kiki0'
for i in range(1,999):
    folder2 = '../cmd_node/cmd_kiki' + str(i)
    compare_folders(folder1, folder2)