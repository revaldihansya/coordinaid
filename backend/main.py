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
    # Load confirmed data to check pipeline congestion
    confirmed_data = load_confirmed_data() 
    
    # This now returns a list of dictionaries: [{"item": "tents", "quantity": 500}, ...]
    extracted_data = extract_item_category(manifest.raw_manifest)
    
    # 1. FIX THE UI OUTPUT FORMATTING
    if isinstance(extracted_data, list):
        item_names = [f"{d.get('quantity', '')} {d.get('item', '')}".strip() for d in extracted_data]
        formatted_items = ", ".join(item_names)
    else:
        formatted_items = "Unknown Items"
        
    # 2. MULTI-ITEM ROUTING & RANKING
    zone_scores = []
    
    for zone in zones:
        total_score = 0
        for item_obj in extracted_data:
            score = calculate_routing_score(item_obj.get("item", ""), zone, confirmed_data)
            total_score += score
            
        avg_score = total_score / len(extracted_data) if extracted_data else 0
        zone_scores.append({
            "zone": zone["region"], 
            "score": round(avg_score, 1)
        })
        
    # Sort zones by score descending
    zone_scores.sort(key=lambda x: x["score"], reverse=True)
    
    # NEW: Filter out any zones that fall below our "worth considering" threshold (e.g., 20)
    viable_zones = [z for z in zone_scores if z["score"] >= 20]
    
    # Now grab up to 3 of ONLY the viable zones
    top_zones = viable_zones[:3]
    
    best_zone = top_zones[0]["zone"] if top_zones else "No suitable zone found"
    highest_score = top_zones[0]["score"] if top_zones else -999
            
    return {
        "status": "Triage Complete",
        "original_text": manifest.raw_manifest,
        "ai_directive": f"AI Extracted: {formatted_items}. Suggested route: {best_zone} (Match Score: {highest_score}).",
        "extracted_item": formatted_items, # Passes the clean string to the confirmation DB
        "best_zone": best_zone,
        "top_routes": top_zones # Sent to the frontend for Phase 3 counter-offers
    }

@app.get("/api/confirmed")
def get_confirmed_aid():
    return load_confirmed_data()

@app.post("/api/confirmed")
def confirm_aid(aid: ConfirmedAid):
    record = add_confirmed_aid(aid)
    return {"message": "Aid confirmed successfully", "record": record}