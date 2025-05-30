# import status_check
import subprocess
import time
import functools
print = functools.partial(print, flush=True)

# リンクの削除
def link_delete(project_ID, all_link_list, linkfailure_point):
    # linkfailure_point から削除するリンクのIDを見つける
    node1 = linkfailure_point[:3]
    node2 = linkfailure_point[4:]
    print("link_delete = " + node1 + node2)
    for i in range(len(all_link_list)):
        if (node1 == all_link_list[i][0][0] and node2 == all_link_list[i][1][0]) or (node1 == all_link_list[i][1][0] and node2 == all_link_list[i][0][0]):
            link_ID = all_link_list[i][2]
            link_create_num = i
            break

    link_delete_command = 'curl -i -X DELETE http://localhost:3080/v2/projects/' + project_ID + '/links/' + link_ID
    cp = subprocess.run(link_delete_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    cp.stdout
    print("link_create_num = " + str(link_create_num))
    return link_create_num

# リンクの再生成
def link_recreate(link_create_num, all_link_list, project_ID, kiki_name_ID_list):
    # link_create_numが、リンクを削除した時にfor文で回した際の値
    for i in range(len(kiki_name_ID_list)):
            if all_link_list[link_create_num][0][0] == kiki_name_ID_list[i][1]:
                node_ID_1 = kiki_name_ID_list[i][2]
            if all_link_list[link_create_num][1][0] == kiki_name_ID_list[i][1]:
                node_ID_2 = kiki_name_ID_list[i][2]
    link_create_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + project_ID +'/links -d "{""nodes"": [{""adapter_number"": ' + all_link_list[link_create_num][0][1] + ', ""node_id"": ""' + str(node_ID_1) + '"", ""port_number"": ' + all_link_list[link_create_num][0][2] + '}, {""adapter_number"": ' + all_link_list[link_create_num][1][1] + ', ""node_id"": ""' + str(node_ID_2) + '"", ""port_number"": ' + all_link_list[link_create_num][1][2] + '}]}"'
    with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(link_create_num + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
        cp = subprocess.run(link_create_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        f.write(cp.stdout)
    with open('VERIFICATIONforNCMonGNS3/verification-tool/link_create_info/link_create_info_' + str(link_create_num + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
        j = 0
        for line in f:
            if j == 14:
                if 'link_id' in line:
                    link_ID = line[16:52]
                    #print(link_ID)
                    # all_link_list[i][2] = link_ID
                    #print(tool.all_link_list)
                    break
                #else:
                #    print('error')
            else:
                j += 1
    return link_ID

"""
for i in range(kaisuu):
    if ver_list[i] == 0:
        continue
    else:
        print(' link failure link-' + str(tool.all_link_list[i][0][0]) + '-' + tool.all_link_list[i][1][0])
        # もともとの機器の状態を取得
        for j in range(tool.kiki_num):# node_nameからkiki_nameに変更
            print('     device-status-capture device-' + str(tool.kiki_name_ID_list[j][1]) + '   start..........', end='')
            status_check.status_check(str(tool.kiki_name_ID_list[j][0]), int(j), 'before', int(i))
            print('complete')

        # リンクの削除
        print('     link-delete           link-' + str(tool.all_link_list[i][0][0]) + '-' + tool.all_link_list[i][1][0] + ' start..........', end='')
        link_delete_command = 'curl -i -X DELETE http://localhost:3080/v2/projects/' + tool.project_ID + '/links/' + str(tool.all_link_list[i][2])
        cp = subprocess.run(link_delete_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        cp.stdout
        print('complete')

        # 設定反映待ち
        print('     device-fault-handling..........')
        time.sleep(40)
        
        # リンク削除後の機器の状態取得
        for j in range(tool.kiki_num):
            print('     device-status-capture device-' + str(tool.kiki_name_ID_list[j][1]) + '   start..........', end='')
            status_check.status_check(str(tool.kiki_name_ID_list[j][0]), int(j), 'after', int(i))
            print('complete')

        # linkの復旧
        for j in range(tool.kiki_num):
            if tool.all_link_list[i][0][0] == tool.kiki_name_ID_list[j][1]:
                node_ID_1 = tool.kiki_name_ID_list[j][2]
            if tool.all_link_list[i][1][0] == tool.kiki_name_ID_list[j][1]:
                node_ID_2 = tool.kiki_name_ID_list[j][2]

        link_create_command = 'curl -i -X POST http://localhost:3080/v2/projects/' + tool.project_ID +'/links -d "{""nodes"": [{""adapter_number"": ' + tool.all_link_list[i][0][1] + ', ""node_id"": ""' + str(node_ID_1) + '"", ""port_number"": ' + tool.all_link_list[i][0][2] + '}, {""adapter_number"": ' + tool.all_link_list[i][1][1] + ', ""node_id"": ""' + str(node_ID_2) + '"", ""port_number"": ' + tool.all_link_list[i][1][2] + '}]}"'
        with open('verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'w', encoding = 'shift-jis') as f:
            cp = subprocess.run(link_create_command, shell = False, encoding = 'shift-jis', stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            f.write(cp.stdout)
        with open('verification-tool/link_create_info/link_create_info_' + str(i + 1) + '.txt', 'r', encoding = 'shift-jis') as f:
            j = 0
            for line in f:
                if j == 14:
                    if 'link_id' in line:
                        link_ID = line[16:52]
                        #print(link_ID)
                        tool.all_link_list[i][2] = link_ID
                        #print(tool.all_link_list)
                        break
                    #else:
                    #    print('error')
                else:
                    j += 1

        # 設定反映待ち
        time.sleep(40)

print('GNS3-network-simulation complete')
"""
