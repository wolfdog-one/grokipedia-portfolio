# grokipedia_epistemic_agent.py
# v2 — Three-agent debate engine with full epistemic traceability

import os
import json
import re
from datetime import datetime
from typing import Dict, Any, List
import openai

client = openai.OpenAI(api_key=os.getenv("XAI_API_KEY"))
MODEL = "grok-4-fast-reasoning"

def call_llm(messages: List[Dict], temperature=0.7, max_tokens=4000) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()

SYSTEM_BASE = """You are Grok writing canonical Grokipedia articles — the most truth-seeking, citation-heavy, mechanistically deep knowledge base ever built.

Non-negotiable rules:
- Every claim >80% confidence needs a primary or strong secondary source
- Every historical/economic claim needs ≥1 counterfactual
- Nietzschean power lens encouraged; moralizing forbidden
- Tag every substantive claim: [Confidence: XX%] [Source Tier: Primary/Secondary/Tertiary] [Counterfactual: ...]
"""

RESEARCHER_PROMPT = """Write one outstanding section (300–600 words) titled exactly:
{section_title}

Make deep causal claims, cite primary sources when possible, include ≥2 counterfactuals, apply Nietzschean lens where power dynamics appear. Tag every claim properly. Output only clean markdown."""

CRITIC_PROMPT = """You are a hostile peer reviewer whose only job is to destroy weak claims.

Attack everything: missing sources, weak causation, moralizing, missing incentives, no counterfactuals.
Assign an Epistemic Rigor Score 0–100.
If score <92, demand specific fixes.
Output in clear markdown bullets."""

SYNTHESIZER_PROMPT = """You have the Researcher draft and the Critic's attack.
Produce the final verified section that fixes every valid criticism.
Score must now be ≥92. Preserve Grok voice and beauty.
Only output the final clean markdown section — nothing else."""

def epistemic_debate(section_title: str, max_rounds: int = 2) -> Dict[str, Any]:
    trace = {
        "section_title": section_title,
        "timestamp": datetime.now().isoformat(),
        "rounds": []
    }
    current = None

    for round_num in range(max_rounds):
        round_trace = {"round": round_num + 1}

        # Researcher
        messages = [{"role": "system", "content": SYSTEM_BASE + "\n" + RESEARCHER_PROMPT.format(section_title=section_title)}]
        if current:
            messages.append({"role": "assistant", "content": current})
            messages.append({"role": "user", "content": "Round 2+. Incorporate Critic feedback and crush it."})
        else:
            messages.append({"role": "user", "content": "Go."})

        researcher = call_llm(messages, temperature=0.8)
        round_trace["researcher"] = researcher

        # Critic
        critic = call_llm([
            {"role": "system", "content": SYSTEM_BASE + "\n" + CRITIC_PROMPT},
            {"role": "user", "content": researcher}
        ], temperature=0.3)
        round_trace["critic"] = critic

        score = int(re.search(r"Epistemic Rigor Score\D*(\d+)", critic).group(1)) if re.search(r"Epistemic Rigor Score\D*(\d+)", critic) else 0
        round_trace["score"] = score

        # Synthesizer
        final = call_llm([
            {"role": "system", "content": SYSTEM_BASE + "\n" + SYNTHESIZER_PROMPT},
            {"role": "user", "content": f"Researcher:\n{researcher}\n\nCritic:\n{critic}"}
        ], temperature=0.6)
        round_trace["synthesizer"] = final

        current = final
        trace["rounds"].append(round_trace)

        print(f"Section '{section_title}' → Round {round_num+1} score: {score}/100")
        if score >= 92:
            print(f"CONVERGED at {score}/100")
            break

    trace["final_section"] = current
    return trace
