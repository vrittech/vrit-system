import requests

# Figma API token and file key
FIGMA_API_TOKEN = 'figd_Bp1Xt-STs7fWAzWS5dlV8Jw_hbKhgeX6F6FJPGAT'
FILE_KEY = 'zsBl7rVWJVubnqSGoZz2I2'
NODE_ID = '509-43593'  # Parent frame of the form (e.g., "Add Blog")

# API endpoint to fetch specific node data
url = f'https://api.figma.com/v1/files/{FILE_KEY}/nodes?ids={NODE_ID}'

headers = {
    'X-Figma-Token': FIGMA_API_TOKEN
}

# Recursive function to extract text and input fields
def extract_fields(node, fields=None):
    if fields is None:
        fields = []

    # Check if the node is of type 'TEXT' (for labels)
    if node['type'] == 'TEXT':
        fields.append({
            'type': 'label',
            'text': node.get('characters', ''),
            'name': node['name'],
            'id': node['id']
        })
    
    # Check if the node is a frame or instance (could be an input field)
    elif node['type'] == 'FRAME' or node['type'] == 'INSTANCE':
        fields.append({
            'type': 'input',
            'name': node['name'],
            'id': node['id'],
            'children': len(node.get('children', []))
        })

    # Recursively check the node's children
    if 'children' in node:
        for child in node['children']:
            extract_fields(child, fields)
    
    return fields

# Make the request to fetch the node
response = requests.get(url, headers=headers)

if response.status_code == 200:
    node_data = response.json()
    document = node_data['nodes'][NODE_ID]['document']

    # Extract fields from the document
    fields = extract_fields(document)
    for field in fields:
        # print(f"{field['type'].capitalize()} - Name: {field['name']}, Text: {field.get('text', 'N/A')}, ID: {field['id']}")
        if field['type'].lower() == "label" and field['name'].lower() == "label":
            print(f"{field['type'].capitalize()} - Name: {field['name']}, Text: {field.get('text', 'N/A')}, ID: {field['id']}")
else:
    print(f'Error: {response.status_code}')
