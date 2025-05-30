url = "http://127.0.0.1:5000/get_submit"

import requests 
# Send GET request with query parameter
params = {'name': 'shinki'}
response = requests.get(url, params=params)

# Handle response
if response.ok:
    print(f"name: {response.json()['message']}")          
else:
    print(f"Error {response.status_code}: {response.text}")   