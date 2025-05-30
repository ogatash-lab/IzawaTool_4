import requests

# -------------------------全ノードを停止----------------------------------------
server_url = 'http://localhost:3080'
project_id = "acbe138d-1064-45c9-9248-f7b1bf97bf2c"

# プロジェクト内の全ノードを取得
nodes_response = requests.get(f'{server_url}/v2/projects/{project_id}/nodes')
nodes = nodes_response.json()

# 各ノードを削除
for node in nodes:
    node_id = node['node_id']
    delete_response = requests.delete(f'{server_url}/v2/projects/{project_id}/nodes/{node_id}')
    if delete_response.status_code == 204:  # 通常、削除に成功した場合のHTTPステータスコードは204です
        print(f"NODE {node_id} has been deleted successfully")
    else:
        print(f"Failed to delete NODE {node_id}: {delete_response.status_code}")