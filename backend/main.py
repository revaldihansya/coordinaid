import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

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

# Point Python to your new file
DB_FILE = "needs_database.json"

# Helper function to read the JSON file
def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as file:
        return json.load(file)

# Helper function to save back to the JSON file
def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Updated GET route to read from the file
@app.get("/api/needs")
def get_needs():
    return load_data()

# Updated POST route to write to the file
@app.post("/api/needs")
def add_need(zone: CrisisZone):
    data = load_data()
    # Convert the Pydantic object to a standard dictionary so JSON can read it
    data.append(zone.model_dump()) 
    save_data(data)
    return {"message": "Crisis zone added successfully!", "zone": zone}

# 1. Define the data structure for the incoming messy text
class DonationManifest(BaseModel):
    raw_manifest: str

# 2. Route to receive the messy donation text
@app.post("/api/donate")
def process_donation(manifest: DonationManifest):
    # TODO: This is where we will inject the AI logic later!
    # For now, we are just catching the text and returning a placeholder response.
    
    return {
        "status": "Received by Triage",
        "original_text": manifest.raw_manifest,
        "ai_directive": "Pending LLM NLP Integration..."
    }