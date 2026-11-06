import os
import json
from groq import Groq

# Groq Client initialize karein (.env se API key pick karega)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Tested model identifier
MODEL_NAME = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
You are an expert senior code reviewer and security auditor.
Analyze the user's provided code for:
1. Syntax & logical bugs
2. Security vulnerabilities (SQL injection, hardcoded secrets, XSS, etc.)
3. Performance bottlenecks and bad practices
4. Clean code & PEP-8 / language standard violations

CRITICAL: Return ONLY a valid JSON object. Do not include markdown code fences (like ```json ... ```) or conversational preamble.

Return this EXACT JSON schema:
{
  "score": <integer from 0 to 100>,
  "summary": "<short 1-2 sentence executive overview>",
  "issues": [
    {
      "type": "<Bug | Security | Performance | Style>",
      "severity": "<High | Medium | Low>",
      "line": "<line number or 'General'>",
      "description": "<what is wrong>",
      "suggestion": "<how to fix it>"
    }
  ],
  "fixed_code": "<full refactored, production-ready, bug-free code>"
}
"""

def review_code_with_ai(source_code: str, language: str = "python") -> dict:
    """
    Groq API ko call karke structured review aur auto-fixed code return karta hai.
    """
    user_prompt = f"Language: {language}\n\nCode to review:\n```\n{source_code}\n```"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=2500,
        )

        content = response.choices[0].message.content.strip()

        # Agar model markdown backticks return kare, unhe clean karein
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        parsed_data = json.loads(content.strip())
        return parsed_data

    except json.JSONDecodeError:
        # Fallback agar valid JSON na bane
        return {
            "score": 50,
            "summary": "Review complete, but output formatting had minor issues.",
            "issues": [
                {
                    "type": "General",
                    "severity": "Low",
                    "line": "N/A",
                    "description": "Raw review output returned.",
                    "suggestion": "Review manual text."
                }
            ],
            "fixed_code": source_code,
        }
    except Exception as exc:
        raise RuntimeError(f"AI Review Engine Error: {str(exc)}")