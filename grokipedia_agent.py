# grokipedia_agent.py — FINAL VERSION (serialization-safe + auto-Markdown formatting)
import ray
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

ray.init(ignore_reinit_error=True)

@ray.remote
def research_task(sub_topic: str) -> str:
    # Client created fresh on each worker → no serialization issue
    client = OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
    
    prompt = f"""
You are a maximally truth-seeking historian with Durant/Nietzsche/Bostrom-level depth.
Write a rigorous 600–800 word section on: {sub_topic}
Focus on primary causal mechanisms, monetary mechanics, incentive structures,
master vs slave morality dynamics where relevant, and one sharp counterfactual.
Cite real historical sources. No moralizing, no presentism.
"""
    response = client.chat.completions.create(
        model="grok-4-fast-reasoning",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.7
    )
    return response.choices[0].message.content

@ray.remote
def format_task(raw_sections: list[str]) -> str:
    # Client created here too
    client = OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
    
    prompt = f"""
Convert the following raw research sections into a complete, publication-ready Grokipedia Markdown article.
Requirements:
- Title: "Hard vs Soft Money in Civilizational Outcomes"
- Use proper # ## ### headings
- Add 2–3 clean Markdown tables (case comparison, master/slave morality, counterfactuals)
- Bullet-point causal chains
- End with References section (extract all citations)
- Keep word count ~1500
- Preserve all rigor and counterfactuals

Raw sections:
{"\n\n===\n\n".join(raw_sections)}
"""
    response = client.chat.completions.create(
        model="grok-4-fast-reasoning",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.3
    )
    return response.choices[0].message.content

print("🚀 Starting Grokipedia agent with auto-formatting...\n")

topics = [
    "Roman denarius debasement 50–270 AD and its role in imperial collapse",
    "Spanish price revolution 1500–1650: mechanics and counterfactuals",
    "Nietzschean reading of tribute empires vs productive empires",
    "What monetary standard could have prevented Spanish collapse?"
]

print(f"Spawning {len(topics)} parallel research tasks...\n")
futures = [research_task.remote(t) for t in topics]
raw_sections = ray.get(futures)

print("Running final formatting task...\n")
formatted_article = ray.get(format_task.remote(raw_sections))

# Save files
with open("latest_raw.txt", "w") as f:
    f.write("\n\n===\n\n".join(raw_sections))
with open("latest_grokipedia_article.md", "w") as f:
    f.write(formatted_article)

print(formatted_article)
print("\nSaved as latest_grokipedia_article.md — ready to publish!")

ray.shutdown()