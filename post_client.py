import requests

# url = "http://localhost:5000/submit"
url = "http://127.0.0.1:5000/post_submit"
data = {"name": "shinki"}
response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Try parsing JSON only if successful
if response.ok:
    print(response.json())
else:
    print("Not a JSON response")