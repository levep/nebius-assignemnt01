import pandas as pd
import os

def grade_length(text):
    """
    Grades the length of the description based on the rubric:
    Good: 50-90 words
    Ok: 40-49 or 91-110 words
    Bad: Under 40 or over 110 words
    """
    # Handle cases where generation failed
    if pd.isna(text) or text == "ERROR":
        return "bad"
        
    # Split the text by whitespace to get the word count
    word_count = len(str(text).split())
    
    if 50 <= word_count <= 90:
        return "good"
    elif 40 <= word_count <= 49 or 91 <= word_count <= 110:
        return "ok"
    else:
        return "bad"

def main():
    input_file = 'data/assignment_01.xlsx'
    
    # Ensure the file exists before trying to open it
    if not os.path.exists(input_file):
        print(f"Error: Could not find {input_file}. Make sure Task 2 finished successfully.")
        return

    print(f"Loading {input_file}...")
    df = pd.read_excel(input_file)
    
    # Calculate the exact word count for your own reference (optional, but helpful!)
    df['actual_word_count'] = df['generated_description'].apply(
        lambda x: len(str(x).split()) if pd.notna(x) and x != "ERROR" else 0
    )
    
    # Apply the grading function to fill in the 'Length' column
    print("Grading the Length criterion...")
    df['Length'] = df['generated_description'].apply(grade_length)
    
    # Save the updated DataFrame back to Excel
    df.to_excel(input_file, index=False)
    print(f"Success! Length grades and word counts have been saved to {input_file}.")

if __name__ == "__main__":
    main()