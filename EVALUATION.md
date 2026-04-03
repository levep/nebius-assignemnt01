# Evaluation Rubric

This document outlines the explicit scoring framework used to evaluate the generated e-commerce product descriptions. [cite_start]It is designed to minimize subjectivity so that both human evaluators and the automated Judge Model reach consistent verdicts.

## 1. Criterion Definitions

[cite_start]Each description is evaluated across seven criteria [cite: 11] [cite_start]and assigned a rating of **Good**, **Ok**, or **Bad**[cite: 17]. 

| Criterion | Good | Ok | Bad |
| :--- | :--- | :--- | :--- |
| **Length** | Exactly 50-90 words. | 40-49 words or 91-110 words. | Under 40 words or over 110 words. |
| **Fluency** | Natural, easy-to-read sentences with smooth transitions. | Readable, but contains 1-2 instances of awkward phrasing. | Hard to read, disjointed, or highly unnatural. |
| **Grammar** | Correct spelling & punctuation with zero errors. | Contains 1-2 minor spelling or punctuation errors. | 3+ errors, or severe grammatical mistakes. |
| **Tone** | Perfectly matches a friendly, credible sales voice. | Appropriate, but occasionally drifts into being too dry/technical. | Unprofessional, lacks credibility, or inappropriate tone. |
| **Grounding** | Sticks strictly to the provided product information. | Includes all provided facts but adds minor, harmless generic fluff. | Hallucinates features, materials, or warranties. |
| **Latency** | Under 1500ms end-to-end generation time. | Between 1500ms and 3000ms. | Over 3000ms. |
| **Cost** | Falls below the defined baseline cost per call. | Exactly at or slightly above the baseline. | Exceeds acceptable budget limits. |

[cite_start]*Note: Latency and Cost are measured programmatically rather than by the LLM judge[cite: 75].*

---

## 2. Pass/Fail Definitions

[cite_start]To determine the final `pass` or `fail` status of a generated description, the following rules apply[cite: 20]:

* [cite_start]**Cumulative Pass Bar:** A description must achieve at least **four "Good" ratings** across the seven criteria and have **zero "Bad" ratings** to pass[cite: 21].
* [cite_start]**Go/No-Go Rules:** If the **Grounding** criterion is rated as "Bad" (meaning the model hallucinated facts not present in the dataset), the description triggers an automatic failure, regardless of its other scores[cite: 23, 24].