import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the updated matching logic from triage_service
from triage_service import extract_item_category, calculate_routing_score
from confirmation_service import load_confirmed_data, add_confirmed_aid, ConfirmedAid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CrisisZone(BaseModel):
    region: str
    priority: str
    portCapacity: str
    status: str
    dailyBurnRate: int # Added field

DB_FILE = "needs_database.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.get("/api/needs")
def get_needs():
    return load_data()

@app.post("/api/needs")
def add_need(zone: CrisisZone):
    data = load_data()
    data.append(zone.model_dump()) 
    save_data(data)
    return {"message": "Crisis zone added successfully!", "zone": zone}

class DonationManifest(BaseModel):
    raw_manifest: str

@app.post("/api/donate")
def process_donation(manifest: DonationManifest):
    zones = load_data()
    
    extracted_item = extract_item_category(manifest.raw_manifest)
    
    best_zone = "No suitable zone found"
    highest_score = -999 
    
    for zone in zones:
        score = calculate_routing_score(extracted_item, zone)
        if score > highest_score:
            highest_score = score
            best_zone = zone["region"]
            
    return {
        "status": "Triage Complete",
        "original_text": manifest.raw_manifest,
        "ai_directive": f" '{extracted_item}'. Suggested route: {best_zone} (Match Score: {highest_score}).",
        "extracted_item": extracted_item, 
        "best_zone": best_zone
    }

@app.get("/api/confirmed")
def get_confirmed_aid():
    return load_confirmed_data()

@app.post("/api/confirmed")
def confirm_aid(aid: ConfirmedAid):
    record = add_confirmed_aid(aid)
    return {"message": "Aid confirmed successfully", "record": record}