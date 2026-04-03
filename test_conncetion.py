import os
import httpx
from openai import OpenAI

API_KEY = os.getenv("NEBIUS_API_KEY", "") 
BASE_URL = "https://api.tokenfactory.nebius.com/v1/"

print(f"Testing connection to: {BASE_URL}")

try:
    # We add a custom http_client with verify=False to bypass strict local proxies
    custom_http_client = httpx.Client(verify=False)
    
    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
        http_client=custom_http_client,
        timeout=10.0 
    )
    
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "user", "content": "Say 'Connection successful!'"}
        ],
        max_tokens=10
    )
    
    print("\nSUCCESS!")
    print(f"Model replied: {response.choices[0].message.content}")

except Exception as e:
    print(f"\nFAILED!")
    print(f"Error details: {e}")