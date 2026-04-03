# src/llm_client.py

import time
import httpx
from openai import OpenAI

class NebiusClient:
    def __init__(self, api_key: str, model_name: str, base_url: str = "https://api.tokenfactory.nebius.com/v1/"):
        """Initializes the OpenAI client pointing to the Nebius Token Factory."""
        
        # Bypass strict local proxies/SSL issues
        custom_http_client = httpx.Client(verify=False)
        
        self.client = OpenAI(
            base_url=base_url, 
            api_key=api_key,
            http_client=custom_http_client # This ensures we don't get the Connection error
        )
        self.model_name = model_name

    def generate_text(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, top_p: float = 1.0, top_k: int = 50) -> dict:
        """Used for Tasks 2 and 4: Generates a product description and tracks metrics."""
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                top_p=top_p,
                extra_body={"top_k": top_k} # Passing non-standard parameters to Nebius
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            return {
                "generated_text": response.choices[0].message.content.strip(),
                "latency_ms": round(latency_ms, 2),
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "error": None
            }
        except Exception as e:
            return {
                "generated_text": "",
                "latency_ms": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "error": str(e)
            }

    def generate_structured_output(self, system_prompt: str, user_prompt: str, response_format, temperature: float = 0.0) -> dict:
        """Used for Tasks 5 and 6: Generates evaluations using Pydantic schemas."""
        start_time = time.time()
        
        try:
            # We use the .parse method for structured outputs required in Task 5
            response = self.client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=response_format,
                temperature=temperature
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            return {
                "parsed_output": response.choices[0].message.parsed,
                "latency_ms": round(latency_ms, 2),
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "error": None
            }
        except Exception as e:
            return {
                "parsed_output": None,
                "latency_ms": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "error": str(e)
            }

    @staticmethod
    def calculate_cost(input_tokens: int, output_tokens: int, price_per_1k_input: float, price_per_1k_output: float) -> float:
        """Used for Task 3: Calculates the API cost based on token usage."""
        input_cost = (input_tokens / 1000.0) * price_per_1k_input
        output_cost = (output_tokens / 1000.0) * price_per_1k_output
        return input_cost + output_cost