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


def calculate_routing_score(item_name: str, zone: dict) -> float:
    """
    Uses AI to semantically match the item against regional context, 
    then applies the mathematical deduction for port congestion in Python.
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
        
        # Extract the first sequence of digits to prevent parsing errors
        # if a model leaks conversational filler (e.g., "The score is 75")
        match = re.search(r'\d+', response_text)
        if match:
            ai_match_score = max(0, min(100, int(match.group())))
        else:
            ai_match_score = 0
    except Exception as e:
        print(f"AI Match Score Error: {e}")
        ai_match_score = 0

    # Calculate port congestion deduction mathematically in Python
    try:
        congestion = float(zone["portCapacity"].replace("% Full", "").strip())
    except ValueError:
        congestion = 50.0 
        
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
        return call_ai_with_failover(prompt)
    except Exception as e:
        print(f"AI API Error: {e}")
        return "Unknown"