import os
import time
import pandas as pd
from src.llm_client import NebiusClient

# 1. Configuration
API_KEY = os.getenv("")
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"

# Decoding Parameters
TEMPERATURE = 1  # Controls randomness (0.0 = deterministic, 1.0 = highly creative)
TOP_P = 0.9        # Nucleus sampling
TOP_K = 50         # Limits token choices to the top K

# Initialize our custom client
client = NebiusClient(api_key=API_KEY, model_name=MODEL_NAME)

# 2. Define the System Prompt
SYSTEM_PROMPT = """
You are an expert e-commerce copywriter. Your task is to write a persuasive product description based on the provided product name, attributes, material, and warranty. 

Strict constraints:
- The description MUST be exactly between 50 and 90 words.
- Maintain a friendly, credible sales voice.
- Stick strictly to the provided information. Do not hallucinate or invent features, materials, or warranties not explicitly given.
"""

def main():
    # 3. Load the dataset
    input_file = 'data/Assignment_01_product_dataset.csv'
    print(f"Loading dataset from {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}. Please ensure it is in the 'data' folder.")
        return

    results = []

    # 4. Generate descriptions
    print(f"Generating descriptions using {MODEL_NAME}...")
    print(f"Parameters: Temp={TEMPERATURE}, Top_p={TOP_P}, Top_k={TOP_K}")
    
    for index, row in df.iterrows():
        print(f"Processing ({index+1}/{len(df)}): {row['product_name']}")
        
        user_prompt = f"""
        Product Name: {row['product_name']}
        Attributes: {row['Product_attribute_list']}
        Material: {row['material']}
        Warranty: {row['warranty']}
        
        Write the product description:
        """
        
        # Call our client with the decoding parameters
        api_result = client.generate_text(
            system_prompt=SYSTEM_PROMPT, 
            user_prompt=user_prompt,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            top_k=TOP_K
        )
        
        row_result = row.to_dict()
        row_result["generated_description"] = api_result.get("generated_text", "ERROR")
        row_result["latency_ms"] = api_result.get("latency_ms", 0)
        row_result["input_tokens"] = api_result.get("input_tokens", 0)
        row_result["output_tokens"] = api_result.get("output_tokens", 0)
        
        if api_result.get("error"):
            print(f"  -> Error: {api_result['error']}")
            
        results.append(row_result)
        time.sleep(0.5)

    # 5. Create final DataFrame
    results_df = pd.DataFrame(results)
    
    # 6. Add blank columns for manual evaluation
    eval_columns = ['Fluency', 'Grammar', 'Tone', 'Length', 'Grounding', 'Cost', 'final_score']
    for col in eval_columns:
        results_df[col] = ""
        
    # 7. Save to CSV with temperature in the filename
    output_filename = f'data/assignment_01_temp_{TEMPERATURE}.csv'
    results_df.to_csv(output_filename, index=False)
    
    print(f"\nSuccess! Generation complete. Results saved to {output_filename}")

if __name__ == "__main__":
    main()