import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. Initialize AI clients with standard OpenAI SDK
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

github_client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ.get("GITHUB_TOKEN")
)

gemini_client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ.get("GEMINI_API_KEY")
)

# 2. Define the failover sequence: (Client Object, Model Name, Service Name)
# 2. Define the failover sequence: (Client Object, Model Name, Service Name)
PROVIDERS = [
    (openrouter_client, "openrouter/free", "OpenRouter"),
    (groq_client, "llama-3.3-70b-versatile", "Groq"),
    (github_client, "gpt-4o-mini", "GitHub Models"),
    (gemini_client, "gemini-3.5-flash", "Gemini")
]

def call_ai_with_failover(prompt: str) -> str:
    """Iterates through providers until an API call succeeds."""
    for client, model, name in PROVIDERS:
        try:
            # Skip if the API key is missing to avoid unnecessary network requests
            if not client.api_key:
                print(f"[{name}] API key missing. Skipping.")
                continue
                
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a precise, data-extraction assistant. Only provide the requested output with no conversational filler."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[{name}] API call failed: {e}")
            continue # Attempt the next provider in the chain
            
    raise Exception("All AI providers failed or are misconfigured. Please check your .env file and network connection.")


# Add confirmed_data as an optional parameter
def calculate_routing_score(item_name: str, zone: dict, confirmed_data: list = None) -> float:
    """
    Uses AI to semantically match the item against regional context, 
    then applies deductions for port congestion AND en-route pipeline volume.
    """
    context_string = f"Region: {zone['region']}. Current Priority Needs: {zone['priority']}."
    
    prompt = f"""
    You are an expert humanitarian logistics matcher. 
    Evaluate how critical or useful the donated item category is to the crisis zone context provided.
    
    Donated Item: "{item_name}"
    Crisis Zone Context: "{context_string}"
    
    Assign a Match Score from 0 to 100:
    - 100: Absolute perfect match or life-saving necessity for this specific disaster context.
    - 75: High utility item that significantly aids relief or recovery efforts in this scenario.
    - 50: Moderate utility item; helpful but not immediately critical.
    - 25: Low utility item; has very peripheral relevance to this type of crisis.
    - 0: Completely irrelevant or potentially hazardous/useless for this specific zone.
    
    Respond ONLY with the integer number. Do not include any text, symbols, or punctuation.
    """
    
    try:
        response_text = call_ai_with_failover(prompt)
        
        match = re.search(r'\d+', response_text)
        if match:
            ai_match_score = max(0, min(100, int(match.group())))
        else:
            ai_match_score = 0
    except Exception as e:
        print(f"AI Match Score Error: {e}")
        ai_match_score = 0

    # 1. Calculate static port congestion deduction
    try:
        congestion = float(zone["portCapacity"].replace("% Full", "").strip())
    except ValueError:
        congestion = 50.0 
        
    # 2. Calculate dynamic EN-ROUTE pipeline penalty
    pipeline_penalty = 0
    if confirmed_data:
        # Count how many shipments are actively routed to this specific region
        en_route_count = sum(1 for aid in confirmed_data if aid.get("destination_route") == zone["region"])
        
        # Deduct 10 points for every active shipment heading there to prevent future bottlenecks
        pipeline_penalty = en_route_count * 10 
        
    # Final Score Calculation
    score = ai_match_score - (congestion * 0.5) - pipeline_penalty
    return score

def extract_item_category(raw_manifest: str) -> list:
    """Uses AI to extract multiple items and quantities into a structured JSON array."""
    prompt = f"""
    You are an AI triage agent for a humanitarian logistics platform. 
    Read the following unstructured donation manifest and extract ALL relief items and their quantities.
    
    Respond ONLY with a valid JSON array of objects. Do not include markdown formatting, backticks, or conversational text.
    Format: [{{"item": "string", "quantity": integer}}]
    If no quantity is specified, estimate a logical default (e.g., 100) or extract the items without quantities if impossible.
    
    Manifest: "{raw_manifest}"
    """
    
    try:
        response_text = call_ai_with_failover(prompt)
        
        # Clean up potential markdown formatting the AI might inject
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        
        import json
        extracted_data = json.loads(clean_json)
        
        # Ensure it's a list
        if isinstance(extracted_data, list):
            return extracted_data
        return [{"item": "Unknown", "quantity": 0}]
        
    except Exception as e:
        print(f"AI JSON Extraction Error: {e}")
        return [{"item": "Unknown Extraction", "quantity": 0}]