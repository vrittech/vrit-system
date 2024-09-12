import requests

# Figma API token and file key
FIGMA_API_TOKEN = 'figd_Bp1Xt-STs7fWAzWS5dlV8Jw_hbKhgeX6F6FJPGAT'
FILE_KEY = 'zsBl7rVWJVubnqSGoZz2I2'

# API endpoint to fetch the entire Figma file
url = f'https://api.figma.com/v1/files/{FILE_KEY}'

headers = {
    'X-Figma-Token': FIGMA_API_TOKEN
}

# Recursive function to extract text and input fields from all nodes
def extract_fields_from_node(node, fields=None):
    if fields is None:
        fields = []

    # Check if the node is of type 'TEXT' (for labels)
    if node['type'] == 'TEXT' and node['name'].lower() == 'label':
        fields.append({
            'type': 'label',
            'text': node.get('characters', ''),
            'name': node['name'],
            'id': node['id']
        })

    # Recursively check the node's children
    if 'children' in node:
        for child in node['children']:
            extract_fields_from_node(child, fields)

    return fields

# Make the request to fetch the entire file
response = requests.get(url, headers=headers)

if response.status_code == 200:
    file_data = response.json()
    document = file_data['document']

    # Extract fields from the entire document
    fields = extract_fields_from_node(document)

    # Print all labels found
    for field in fields:
        print(f"{field['type'].capitalize()} - Name: {field['name']}, Text: {field.get('text', 'N/A')}, ID: {field['id']}")
else:
    print(f'Error: {response.status_code}')
