import requests

# Figma API token and file key
FIGMA_API_TOKEN = 'figd_Bp1Xt-STs7fWAzWS5dlV8Jw_hbKhgeX6F6FJPGAT'
FILE_KEY = 'zsBl7rVWJVubnqSGoZz2I2'
NODE_ID = '509:43593'  # Specific node ID from the URL

# API endpoint to fetch specific node data
url = f'https://api.figma.com/v1/files/{FILE_KEY}/nodes?ids={NODE_ID}'

headers = {
    'X-Figma-Token': FIGMA_API_TOKEN
}

# Recursive function to print all label nodes
def extract_labels(node, depth=0):
    indent = "  " * depth  # Indentation for child nodes

    # Check if the node is a label (TEXT node)
    if node['type'] == 'TEXT':
        label_text = node.get('characters', 'No Text')
        print(f"{indent}Label: {label_text}, Name: {node.get('name', 'Unnamed Node')}, ID: {node.get('id')}")

    # Recursively check the node's children
    if 'children' in node:
        for child in node['children']:
            extract_labels(child, depth + 1)

# Make the request to fetch the node data
response = requests.get(url, headers=headers)

if response.status_code == 200:
    node_data = response.json()
    document = node_data['nodes'][NODE_ID]['document']

    # Extract and print all labels from the node
    extract_labels(document)
else:
    print(f'Error: {response.status_code}')
