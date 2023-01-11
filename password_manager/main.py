from fastapi import FastAPI
from enum import Enum
from typing import Union
from pydantic import BaseModel
import os 
import json


api = FastAPI()

class KeyModel(BaseModel):
    keys: list

class AccountModel(BaseModel):
    index: int
    website: str
    email: Union[str, None]
    username: str
    password: str

class AccountIndex(BaseModel):
    __root__: dict[str, AccountModel]

class JsonModel(BaseModel):
    accounts: AccountIndex

async def load_db():
    with open("db.json", "r") as file:
        data = json.load(file)
    return data

async def update_db(data):
    with open("./db.json", "w") as file:
        json.dump(data, file)



@api.post("/add_json")
async def add_json_data(json_data: JsonModel):
    key_list = []
    data = await load_db()
    new_data = json_data.dict()


    final_key = list(data["accounts"].keys())[-1]
    old_key = list(new_data["accounts"].keys())[0]
    new_key = int(final_key) + 1
    new_data["accounts"][str(new_key)] = new_data["accounts"].pop(old_key)

    data["accounts"].update(new_data["accounts"])

    await update_db(data=data)

    added_item = JsonModel.parse_obj(new_data)
    return { "id": new_key, "account added": True, "added_item": added_item }

@api.get("/website/{website_name}")
async def get_by_website(website_name: str):
    data = await load_db()
    
    new_data = data["accounts"]

    for val in new_data:
        if new_data[val]["website"] == website_name:
            item = data["accounts"][val]
            return dict(item)

@api.get("/id/{account_id}")
async def get_by_id(account_id: int):
    ac_id = str(account_id)
    data = await load_db()

    item = data["accounts"][ac_id]

    return dict(item)

@api.delete("/delete/{account_id}")
async def delete_by_id(account_id: int):
    ac_id = str(account_id)

    data = await load_db()

    del data["accounts"][ac_id]

    await update_db(data=data)

    return {"id": ac_id, "deleted": True}

@api.get("/")
async def get_data():
    data = await load_db()
    return dict(data)