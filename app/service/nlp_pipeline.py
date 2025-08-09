import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    if not client.api_key:
        raise ValueError("GROQ_API_KEY not found in .env file or environment.")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    client = None

# --- API Client Initialization (remains the same) ---
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print("CRITICAL ERROR: GROQ_API_KEY environment variable not set.")
    client = None

# --- THE ONE AND ONLY SERVICE FUNCTION (UPDATED) ---

def process_query_with_groq_llm(text: str) -> dict:
    """
    Uses the powerful Llama 3 model via the Groq API to perform the entire NLP task
    in both English and French.
    """
    if not client:
        return {"english_product": "Error", "english_attributes": [], "french_product": "Error", "french_attributes": []}

    # --- THE NEW, DUAL-LANGUAGE PROMPT ---
    system_prompt = """
You are an expert AI assistant for an agro-food product search engine. Your sole job is to analyze a user's messy, multilingual query.
You must understand the user's intent, ignoring typos. Then, you will extract the main product and its attributes.
Finally, you must provide this structured information in BOTH English and French.
Your entire response must be ONLY a single, clean, valid JSON object with the keys "english_product", "english_attributes", "french_product", and "french_attributes".
Do not add any other text or explanations.
"""

    user_prompt = f"""
Here are some examples of how to perform the task:
---
User Query: "pomee de terra 5kg bio"
JSON Response: {{"english_product": "potato", "english_attributes": ["5kg", "organic"], "french_product": "pomme de terre", "french_attributes": ["5kg", "bio"]}}
---
User Query: "then a huile d'oluve"
JSON Response: {{"english_product": "tuna with olive oil", "english_attributes": [], "french_product": "thon à l'huile d'olive", "french_attributes": []}}
---
User Query: "organic apples 1kg"
JSON Response: {{"english_product": "organic apples", "english_attributes": ["1kg"], "french_product": "pommes bio", "french_attributes": ["1kg"]}}
---

Now, process the following query. Remember, respond with ONLY the JSON object.

User Query: "{text}"
JSON Response:
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model="llama3-8b-8192",
            temperature=0.2,
            max_tokens=400, # Increased slightly for the longer output
            response_format={"type": "json_object"},
        )
        
        raw_output = chat_completion.choices[0].message.content
        print(f"DEBUG: Raw LLM output: '{raw_output}'")
        
        data = json.loads(raw_output)
        return data

    except Exception as e:
        print(f"CRITICAL ERROR processing Groq API call: {e}")
        return {"english_product": "Error", "english_attributes": [], "french_product": "Error", "french_attributes": []}