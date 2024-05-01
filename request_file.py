# request_file.py

import requests

def upload_files(file_paths):
    files = {'operations': '{"query": "mutation ($files: [Upload!]!) { read_typeA_pdf(folderInput: { files: $files }) }", "variables": { "files": null }'}

    for idx, file_path in enumerate(file_paths):
        files[f'file-{idx}'] = open(file_path, 'rb')

    response = requests.post('http://localhost:8000/graphql', files=files)
    return response
