# uvicorn api:app --host 0.0.0.0 --port 8000

from fastapi import FastAPI
from datastore import DataHandler

from pydantic import BaseModel

class NFCTag(BaseModel):
    id: str

# root
# get sensor states
# get nfc tag data
# get send recommended temp

app = FastAPI()

valid_keys = DataHandler("keys.json")

current_data = {}

@app.get("/")
def root():
    # test to check if its actually working
    return {"status": "API is running fine"}

@app.post("/nfc-tag")
def check_nfc(tag: NFCTag):
    # read data keys
    data = valid_keys.read()

    # loop through each key to check if any of them match up with the nfc key taht we need
    for key in data:
        if key["id"] == tag.id:
            # if show then we show the data that is stored
            return {"permission": "granted"}
    
    return {"permission": "denied"}

@app.post("/update-telemetry")
def update_telemetry(data: dict):
    # save data to seperate variable to be used later on
    current_data = data
    return data

def get_telemetry_data():
    return current_data