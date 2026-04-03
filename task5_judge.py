import os
import time
import pandas as pd
from src.llm_client import NebiusClient
from src.schemas import AllCriteriaEvaluation

# 1. Configuration
API_KEY = os.getenv("NEBIUS_API_KEY", "")
# Switched from Gemma due to API 404 error, as permitted by the assignment
JUDGE_MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507" 

# Initialize our custom client
client = NebiusClient(api_key=API_KEY, model_name=JUDGE_MODEL)

# 2. Define the Judge System Prompt
# Includes the exact definitions from the Task 1 rubric (excluding Latency/Cost).
JUDGE_SYSTEM_PROMPT = """
You are an expert, highly objective QA evaluator for e-commerce product descriptions. 
Your task is to evaluate a generated product description based on the following strictly defined rubric.

### RUBRIC
1. Length:
   - good: Exactly 50-90 words.
   - ok: 40-49 words or 91-110 words.
   - bad: Under 40 words or over 110 words.
2. Fluency:
   - good: Natural, easy-to-read sentences with smooth transitions.
   - ok: Readable, but contains 1-2 instances of awkward phrasing.
   - bad: Hard to read, disjointed, or highly unnatural.
3. Grammar:
   - good: Correct spelling & punctuation with zero errors.
   - ok: Contains 1-2 minor spelling or punctuation errors.
   - bad: 3+ errors, or severe grammatical mistakes.
4. Tone:
   - good: Perfectly matches a friendly, credible sales voice.
   - ok: Appropriate, but occasionally drifts into being too dry/technical or overly clichéd.
   - bad: Unprofessional, lacks credibility, or inappropriate tone.
5. Grounding:
   - good: Sticks strictly to the provided product information.
   - ok: Includes all provided facts but adds minor, harmless generic fluff.
   - bad: Hallucinates features, materials, or warranties NOT present in the provided facts.

For each criterion, provide a detailed 'explanation' first, followed by the final 'verdict' (good, ok, or bad).
"""

def main():
    # Load the CSV generated in Task 2
    input_file = 'data/assignment_01_temp_1.csv' 
    print(f"Loading dataset from {input_file}...")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}.")
        return

    # FIX: Force evaluation columns to be type 'object' (string) so we don't get a TypeError
    eval_columns = ['Fluency', 'Grammar', 'Tone', 'Length', 'Grounding', 'Cost', 'final_score']
    for col in eval_columns:
        if col in df.columns:
            df[col] = df[col].astype(object)

    # We will run a sanity check on just 5 products first, as requested in Task 6.1
    sanity_check_limit = 5
    df_subset = df.head(sanity_check_limit).copy()
    
    print(f"Running judge model ({JUDGE_MODEL}) on the first {sanity_check_limit} products for a sanity check...\n")
    
    # Iterate through the rows to judge them
    for index, row in df_subset.iterrows():
        print(f"Judging ({index+1}/{sanity_check_limit}): {row['product_name']}")
        
        # We must provide the original facts SO the judge can evaluate Grounding!
        user_prompt = f"""
        ### ORIGINAL PRODUCT FACTS
        Product Name: {row['product_name']}
        Attributes: {row['Product_attribute_list']}
        Material: {row['material']}
        Warranty: {row['warranty']}
        
        ### GENERATED DESCRIPTION TO EVALUATE
        {row['generated_description']}
        """
        
        # Call our client using the structured output parser
        api_result = client.generate_structured_output(
            system_prompt=JUDGE_SYSTEM_PROMPT, 
            user_prompt=user_prompt,
            response_format=AllCriteriaEvaluation,
            temperature=0.0 # Strict 0.0 temperature for consistent grading
        )
        
        parsed_eval = api_result.get("parsed_output")
        error = api_result.get("error")
        
        if error or not parsed_eval:
            print(f"  -> Error parsing evaluation: {error}")
            continue
            
        # Store verdicts back into the dataframe
        df_subset.at[index, 'Length'] = parsed_eval.length.verdict.value
        df_subset.at[index, 'Fluency'] = parsed_eval.fluency.verdict.value
        df_subset.at[index, 'Grammar'] = parsed_eval.grammar.verdict.value
        df_subset.at[index, 'Tone'] = parsed_eval.tone.verdict.value
        df_subset.at[index, 'Grounding'] = parsed_eval.grounding.verdict.value
        
        # Print the reasoning for the Sanity Check
        print(f"  - Grounding Verdict: {parsed_eval.grounding.verdict.value.upper()}")
        print(f"    Explanation: {parsed_eval.grounding.explanation}\n")
        
        time.sleep(1) # Respect rate limits

    # Save the sanity check to a new file so you can review it
    output_filename = 'data/assignment_01_judge_sanity_check.csv'
    df_subset.to_csv(output_filename, index=False)
    print(f"Sanity check complete. Results saved to {output_filename}")

if __name__ == "__main__":
    main()