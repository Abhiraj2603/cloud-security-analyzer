import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def generate_ai_summary(scan_results):
    """
    Send AWS scan results to Ollama and return an AI-generated
    security assessment.
    """

    prompt = f"""
You are a Senior AWS Cloud Security Consultant.

Analyze the following AWS security scan results.

Return your response in this format:

Overall Security Score: XX/100

Risk Level:
(Low / Medium / High / Critical)

Executive Summary:
(2-3 sentences)

Top Risks:
- Risk 1
- Risk 2
- Risk 3

Recommended Actions:
1.
2.
3.
4.

AWS Scan Results:

{json.dumps(scan_results, indent=2)}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json().get(
            "response",
            "AI summary not available."
        )

    except Exception as e:
        return f"Unable to generate AI summary.\n\nError: {str(e)}"
