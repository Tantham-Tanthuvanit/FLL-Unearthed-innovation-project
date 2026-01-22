# uvicorn api:app --host 0.0.0.0 --port 8000 --reload

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

app.state.current_data = {}

class Telemetry(BaseModel):
    fan1: bool
    fan2: bool

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
def update_telemetry(data: Telemetry):
    # save data to seperate variable to be used later on
    app.state.current_data = data.model_dump()


    return data

@app.get("/get-telemetry")
def get_telemetry_data():
    return app.state.current_data