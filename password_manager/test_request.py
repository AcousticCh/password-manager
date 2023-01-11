import requests
import json

endpoint_root = "http://127.0.0.1:8000/"
endpoint_add_json = "http://127.0.0.1:8000/add_json"
endpoint_get_by_id = "http://127.0.0.1:8000/id/"
endpoint_get_by_website = "http://127.0.0.1:8000/website/"
endpoint_delete = "http://127.0.0.1:8000/delete/"
body = { "accounts": {"6": {
    "index": 0,
    "website": "blr",
    "email": "hassenr@fil.com",
    "username": "acousticCh",
    "password": "peantac", 
    }}}

response = requests.post(endpoint_add_json, json=body)
# response = requests.get(endpoint_root)
print(response.json())
print("\n----------------------------------------------------\n")
# response = requests.get(f"{endpoint_get_by_website}github")
# response = requests.delete(f"{endpoint_delete}3")
# print(response.json())
# print("\n----------------------------------------------------\n")

# response = requests.get(endpoint_root)
# print(response.json())