# generate_synthetic_data.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")

# Read your latest formatted article
with open("latest_grokipedia_article.md", "r") as f:
    article = f.read()

prompt = f"""
You are an expert synthetic-data engineer for Grokipedia.
From the following article, generate **220** high-quality training examples in JSONL format.
Include:
- 100 standard Q&A pairs
- 70 chain-of-thought reasoning traces
- 50 preference pairs (good = truth-seeking, non-resentful; bad = moralizing, presentist, or slave-morality answer)

Output ONLY valid JSONL (one JSON object per line). No markdown, no explanation.

Article:
{article}
"""

response = client.chat.completions.create(
    model="grok-4-fast-reasoning",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=4000,
    temperature=0.4
)

with open("synthetic_data_hard_vs_soft_money.jsonl", "w") as f:
    f.write(response.choices[0].message.content)

print("220 synthetic examples saved to synthetic_data_hard_vs_soft_money.jsonl")
print("Cost: ~$0.05 — ready for fine-tuning!")