# [cite_start]Nebius Academy: From AI Model to AI Agent - Assignment 1 [cite: 1, 3]

[cite_start]**Due Date:** 5.4.26 [cite: 4]

## Overview
[cite_start]This project is a hands-on dive into Large Language Model (LLM) evaluation[cite: 5]. [cite_start]The objective is to navigate the entire evaluation pipeline: understanding a business use-case, defining explicit evaluation criteria, and performing evaluations using both human grading and an automated Judge Model (LLM-as-a-judge)[cite: 5]. [cite_start]It explores the strengths, trade-offs, and inherent challenges of evaluating generative outputs that lack a single "correct" answer[cite: 6].

## Business Use Case
[cite_start]**Generate E-commerce Product Descriptions** [cite: 7]
[cite_start]Using a provided dataset of e-commerce products (containing name, structured attributes, material, and warranty), the goal is to use an LLM to craft persuasive, 50-90 word descriptions for each item[cite: 8, 9].

## Evaluation Criteria
[cite_start]The generated descriptions are evaluated against the following metrics[cite: 11]:
* [cite_start]**Fluency:** Natural, easy-to-read sentences[cite: 11].
* [cite_start]**Grammar:** Correct spelling & punctuation[cite: 11].
* [cite_start]**Tone:** Matches friendly, credible sales voice[cite: 11].
* [cite_start]**Length:** 50-90 words[cite: 11].
* [cite_start]**Grounding:** Sticks strictly to the provided product information[cite: 11].
* [cite_start]**Latency:** Average time per call (Time to first byte / full response)[cite: 11].
* [cite_start]**Cost:** Average price per call (Relative inference or API cost per 1K tokens)[cite: 11].

---

## Project Tasks

### [cite_start]Task 1: Define Your Rubric (15 points) [cite: 13]
* [cite_start]**Criterion Definitions:** Establish explicit definitions for *good*, *ok*, and *bad* for each criterion to minimize subjectivity[cite: 17, 18].
* **Pass/Fail Rules:**
    * [cite_start]*Cumulative Pass Bar:* Define the minimum combination of ratings needed to pass[cite: 21].
    * [cite_start]*Go/No-go Rules:* Define single-criterion triggers for automatic failure (e.g., failing Grounding)[cite: 23, 24].

### [cite_start]Task 2: Generate Descriptions (20 points) [cite: 26]
* [cite_start]**Model Selection:** Use either `Gemma-2-9b-it` or `Meta-Llama-3.1-8B-Instruct` from the Nebius Token Factory[cite: 31, 32, 33].
* [cite_start]**Generation:** Write a system prompt applying class guidelines to generate a 50-90 word description for every product[cite: 27, 28, 29].
* [cite_start]**Structured Output & Storage:** For each API call, collect `generated_description`, `latency_ms`, `input_tokens`, and `output_tokens`[cite: 35, 36, 37, 38, 39]. [cite_start]Save all results, along with blank evaluation columns, into `assignment_01.xlsx`[cite: 41, 42].

### [cite_start]Task 3: Manual (Human) Evaluation (10 points) [cite: 47]
* [cite_start]**Cost Calculation:** Convert input/output tokens into USD costs based on model pricing[cite: 49].
* [cite_start]**Evaluation:** Manually rate 10-15 products across all criteria using the Task 1 rubric[cite: 50].
* [cite_start]**Baseline Analysis:** Apply pass/fail rules to determine a `final_score`, and analyze which criteria performed best/worst to guide improvements[cite: 51, 52, 53].

### [cite_start]Task 4: Improvement Cycle (15 points) [cite: 55]
* [cite_start]Iterate on the baseline by experimenting with prompt engineering, changing the model, adjusting decoding parameters, or adding post-processing[cite: 56, 58, 59, 60, 62].
* [cite_start]**Documentation:** For each experiment, document what was changed, why it was expected to help, and the new evaluation scores[cite: 63, 64, 65, 66].

### [cite_start]Task 5: Create a Judge Model (20 points) [cite: 68]
* [cite_start]**Setup:** Automate the evaluation process by building an LLM-as-a-judge using the model *not* chosen in Task 2 (switching to a larger model if necessary)[cite: 70, 72].
* [cite_start]**Judge Prompt:** Include the Task 1 rubric definitions so the model applies consistent standards (excluding latency and cost)[cite: 74, 75].
* [cite_start]**Output Schema:** Use Pydantic to enforce a structured output returning an `explanation` (string) followed by a `verdict` (enum: good/ok/bad)[cite: 76, 77, 79].

### [cite_start]Task 6: Run and Analyze the Judge (20 points) [cite: 82]
* [cite_start]**Sanity Check & Full Run:** Test the judge on 5 products, adjust if needed, and then run it on the entire dataset, calculating the final score[cite: 83, 84, 85].
* [cite_start]**Comparison:** Compare the automated judge's verdicts against the human evaluation scores from Task 3 to compute an agreement rate[cite: 86].
* [cite_start]**Criterion-by-Criterion:** Run the judge separately for each criterion to see if isolated context improves agreement[cite: 88, 89, 90].
* [cite_start]**Final Analysis:** Reflect on the practical trade-offs between human evaluation and LLM-as-a-judge, and recommend an approach for a large-scale production system[cite: 91, 92, 93].

---
*Generated for Nebius Academy Assignment 1.*
---
## Solution
### Directory structure

```
assignment_1/
│
├── data/
│   ├── Assignment_01_product_dataset.csv   # Original dataset
│   ├── assignment_01_task2_generated.xlsx  # Output from Task 2
│   └── assignment_01_task3_graded.xlsx     # Your manually graded version
│
├── src/
│   ├── __init__.py
│   ├── llm_client.py       # Shared class to handle Nebius API calls & cost calculation
│   └── schemas.py          # Pydantic models for your Judge (Task 5)
│
├── task2_generate.py       # Script to run prompt & generate descriptions
├── task4_improve.py        # Script for your iterative experiments
├── task5_6_judge.py        # Script to run the LLM-as-a-judge and compare scores
│
├── README.md               # Overview of the project
└── EVALUATION.md           # Your rubric definitions
```
---
### Instruction:
```
python3 -m venv venv
source venv/bin/activate
```

