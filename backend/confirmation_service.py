import json
import os
from pydantic import BaseModel
from datetime import datetime

CONFIRMED_DB_FILE = "confirmed_aid_database.json"

class ConfirmedAid(BaseModel):
    destination_route: str
    donation: str
    donor: str
    manifest: str
    timestamp: str = None

def load_confirmed_data():
    if not os.path.exists(CONFIRMED_DB_FILE):
        return []
    with open(CONFIRMED_DB_FILE, "r") as file:
        return json.load(file)

def save_confirmed_data(data):
    with open(CONFIRMED_DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def add_confirmed_aid(aid_record: ConfirmedAid):
    data = load_confirmed_data()
    # Auto-generate timestamp if not provided by frontend
    if not aid_record.timestamp:
        aid_record.timestamp = datetime.now().isoformat()
        
    data.append(aid_record.model_dump())
    save_confirmed_data(data)
    return aid_record