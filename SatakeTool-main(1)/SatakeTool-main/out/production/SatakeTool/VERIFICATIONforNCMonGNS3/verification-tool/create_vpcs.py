'''
・1つのnetworkconfigurationでノードの個数，リンクの個数，VPCSの個数を取得

'''

def create_vpcs(project_ID, name_vpcs):
    
    
    vpcs_create_commend = 'curl -X POST http://localhost:3080/v2/projects' + project_ID + '/nodes -d "{\"name\": \"' + name_vpcs + '\", \"node_type\": \"vpcs\", \"compute_id\": \"local\"}"'

# curl -i -X POST http://localhost:3080/v2/projects/f16e6883-4eb4-4e62-9e48-ae383e065a46/links -d "{""nodes"": [{""adapter_number"": 1, ""node_id"": ""39edb35e-5c3d-48aa-b954-3febf7c6ded9"", ""port_number"": 15}, {""adapter_number"": 0, ""node_id"": ""839fcdce-9dca-4ffa-96d7-0161729b8298"", ""port_number"": 0}]}"