from fastapi import FastAPI
from .password_manager import data.json
import json

data_storage = data.json
api = FastAPI()

@api.get("/accounts")
async def get_accounts():
    with open(data_storage) as file:
        data = json.load(file)
    Return data

# FINISH GET ACCOUNTS AND CREATE ADD ACCOUNT WORK WITH OASSWORD MANAGER DATA STORE
