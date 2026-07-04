import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Initialize the Gemini Client here
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def calculate_routing_score(item_name: str, zone: dict) -> float:
    """Uses Gemini to semantically match the item against regional context, 

    then applies the mathematical deduction for port congestion in Python.
    """
    # Combine region and priority text to maximize AI situational context
    context_string = f"Region: {zone['region']}. Current Priority Needs: {zone['priority']}."
    
    prompt = f"""
    You are an expert humanitarian logistics matcher. 
    Evaluate how critical or useful the donated item category is to the crisis zone context provided.
    
    Donated Item: "{item_name}"
    Crisis Zone Context: "{context_string}"
    
    Assign a Match Score from 0 to 100:
    - 100: Absolute perfect match or life-saving necessity for this specific disaster context (e.g., food/water to a flood zone, blankets to an earthquake zone).
    - 75: High utility item that significantly aids relief or recovery efforts in this scenario.
    - 50: Moderate utility item; helpful but not immediately critical.
    - 25: Low utility item; has very peripheral relevance to this type of crisis.
    - 0: Completely irrelevant or potentially hazardous/useless for this specific zone.
    """
    
    try:
        # Use structured output to guarantee an integer score between 0 and 100
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=int,
                temperature=0.1 # Low temperature for consistent matching
            ),
        )
        # Ensure the score stays within the intended boundaries
        ai_match_score = max(0, min(100, int(response.text.strip())))
    except Exception as e:
        print(f"AI Match Score Error: {e}")
        # Default fallback to 0 if the API fails so it doesn't break execution
        ai_match_score = 0

    # Calculate port congestion deduction mathematically in Python
    try:
        congestion = float(zone["portCapacity"].replace("% Full", "").strip())
    except ValueError:
        congestion = 50.0 
        
    # Final calculation combines AI situational awareness with logical port caps
    score = ai_match_score - (congestion * 0.5)
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
            model='gemini-3.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"AI API Error: {e}")
        return "Unknown"