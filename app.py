from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import re
from prompt import build_prompt

app = FastAPI()

# 📌 Input Model
class SymptomRequest(BaseModel):
    symptoms: str


# 🔹 Severity Logic
def get_severity(symptoms: str):
    symptoms = symptoms.lower()

    if "chest pain" in symptoms or "breathing problem" in symptoms:
        return "high"
    elif "fever" in symptoms or "body pain" in symptoms or "vomiting" in symptoms:
        return "medium"
    else:
        return "low"


# 🔹 API Endpoint
@app.post("/check")
def check_symptoms(request: SymptomRequest):
    prompt = build_prompt(request.symptoms)

    try:
        # 🔗 Call Ollama (llama3)
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json().get("response", "")
        print("RAW RESULT:", result)  # 🔍 Debug

        try:
            # 🔥 Extract JSON part
            json_match = re.search(r"\{.*\}", result, re.DOTALL)

            if json_match:
                cleaned = json_match.group()

                # 🔹 First parse
                parsed = json.loads(cleaned)

                # 🔹 Handle escaped JSON (double parsing)
                if isinstance(parsed, str):
                    parsed = json.loads(parsed)
            else:
                parsed = {"raw_output": result}

            # ✅ Add severity manually
            parsed["severity"] = get_severity(request.symptoms)

            return parsed

        except Exception as e:
            return {
                "error": "Parsing failed",
                "severity": get_severity(request.symptoms),
                "raw_output": result
            }

    except Exception as e:
        return {
            "error": "Ollama connection failed",
            "details": str(e)
        }


# 🔹 Home Route
@app.get("/")
def home():
    return {"message": "Healthcare Symptom Checker API is running"}    