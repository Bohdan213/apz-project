import requests
import json

def parse_and_execute_requests(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().split('\n')

    requests_list = []
    request_data = {}
    json_data = []

    for line in lines:
        line = line.strip()
        
        if line.startswith('###'):
            if request_data:
                # Join multi-line JSON data and load it
                if json_data:
                    request_data['data'] = json.loads(''.join(json_data))
                    json_data = []
                requests_list.append(request_data)
            request_data = {'description': line[4:].strip()}
        
        elif line.startswith('POST') or line.startswith('GET') or line.startswith('DELETE'):
            if json_data:  # If there's pending JSON data to process
                request_data['data'] = json.loads(''.join(json_data))
                json_data = []
            method, url = line.split()
            request_data['method'] = method
            request_data['url'] = url
            request_data['headers'] = {'Content-Type': 'application/json'}
        
        elif line.startswith('{'):
            json_data.append(line)
        elif line.startswith('}'):
            json_data.append(line)
        elif line.startswith('"') or line.startswith('[') or line.startswith(']'):
            json_data.append(line)

    if json_data:  # Final block of JSON data
        request_data['data'] = json.loads(''.join(json_data))
    if request_data:
        requests_list.append(request_data)

    for request_data in requests_list:
        method = request_data['method']
        url = request_data['url']
        headers = request_data['headers']
        data = request_data.get('data', {})
        
        response = None
        if method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'GET':
            response = requests.get(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, json=data)
        
        print(f"Description: {request_data['description']}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}\n")

file_path = 'test_user_management.http'
parse_and_execute_requests(file_path)
file_path = 'test_planning.http'
parse_and_execute_requests(file_path)
