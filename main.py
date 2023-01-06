from fastapi import FastAPI
import json
# CONSIDER OS.GETPATH
data_storage = "./password_manager/example.json"
api = FastAPI()

@api.get("/accounts")
async def get_accounts():
    with open(data_storage) as file:
        data = json.load(file)
    Return data

# FINISH GET ACCOUNTS AND CREATE ADD ACCOUNT WORK WITH OASSWORD MANAGER DATA STORE
