
import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env")

client = Groq(api_key=GROQ_API_KEY)


def analyze_with_ai(audit_data: dict):

    prompt = f"""
You are an expert SEO and website audit assistant.

Analyze the following website audit data.

Give practical and easy-to-understand recommendations.

Focus on:
1. SEO
2. Broken Links
3. Images
4. Accessibility
5. Performance
6. Metadata

Audit Data:
{json.dumps(audit_data, indent=2)}

Return the response in this JSON format:

{{
    "summary": "Short overall summary",
    "priority_issues": [
        {{
            "category": "SEO",
            "issue": "Problem",
            "impact": "Why it matters",
            "recommendation": "How to fix it"
        }}
    ],
    "seo_recommendations": [],
    "performance_recommendations": [],
    "accessibility_recommendations": [],
    "metadata_recommendations": [],
    "image_recommendations": [],
    "link_recommendations": []
}}

Keep recommendations practical and concise.
Do not invent problems that are not present in the audit data.
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert AI website SEO auditor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2000
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "summary": content,
            "priority_issues": [],
            "seo_recommendations": [],
            "performance_recommendations": [],
            "accessibility_recommendations": [],
            "metadata_recommendations": [],
            "image_recommendations": [],
            "link_recommendations": []
        }