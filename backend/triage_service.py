# triage_service.py
import os
from google import genai
from dotenv import load_dotenv

# Initialize the Gemini Client here
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def calculate_routing_score(item_name: str, zone: dict) -> float:
    """Calculates the match score between the donated item and regional needs."""
    priority_match = 1 if item_name.lower() in zone["priority"].lower() else 0
    try:
        congestion = float(zone["portCapacity"].replace("% Full", "").strip())
    except ValueError:
        congestion = 50.0 
        
    score = (priority_match * 100) - (congestion * 0.5)
    return score

def extract_item_category(raw_manifest: str) -> str:
    """Uses AI to extract the primary item category from a raw text manifest."""
    prompt = f"""
    You are an AI triage agent for a humanitarian logistics platform. 
    Read the following unstructured donation manifest and identify the single most prominent or useful category of relief items being offered. 
    Respond ONLY with the name of the item category (e.g., "Tents", "Water", "Winter Coats", "Medical Supplies"). Do not include any other words or punctuation.
    
    Manifest: "{raw_manifest}"
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash', # Using the updated, active model
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"AI API Error: {e}")
        return "Unknown"