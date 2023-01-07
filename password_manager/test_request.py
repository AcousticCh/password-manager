import requests
import json

endpoint_root = "http://127.0.0.1:8000/"
endpoint_add_json = "http://127.0.0.1:8000/add_json"
endpoint_get_by_id = "http://127.0.0.1:8000/id/"
body = { "accounts": {"6": {
    "index": 0,
    "website": "blubber",
    "email": "hassenr@fil.com",
    "username": "acousticCh",
    "password": "peantac", 
    }}}

# response = requests.post(endpoint_add_json, json=body)
response = requests.get(endpoint_root)
response = requests.get(f"{endpoint_get_by_id}4")


print(response.json())