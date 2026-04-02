def build_prompt(symptoms):
    return f"""
You are a healthcare assistant.

Based on these symptoms:
{symptoms}

Strictly return ONLY valid JSON in this format:

{{
  "conditions": ["condition1", "condition2"],
  "next_steps": ["step1", "step2"],
  "disclaimer": "This is not medical advice"
}}

Do not add any extra text.
"""