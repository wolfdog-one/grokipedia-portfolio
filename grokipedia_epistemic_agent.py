# grokipedia_epistemic_agent.py
# v2 — Three-agent debate engine with Verifier + clean formatting

import os
import json
import re
from datetime import datetime
from typing import Dict, Any, List
import openai

client = openai.OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
MODEL = "grok-4-fast-reasoning"

def call_llm(messages: List[Dict], temperature=0.7, max_tokens=4000) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()

SYSTEM_BASE = """You are Grok writing canonical Grokipedia articles — truth-seeking, citation-heavy, mechanistically deep."""

RESEARCHER_PROMPT = """Write one outstanding section (300–600 words) titled exactly:
{section_title}

Make deep causal claims, cite primary sources when possible, include ≥2 counterfactuals, apply Nietzschean lens where power dynamics appear. Tag every claim properly. Output clean markdown."""

CRITIC_PROMPT = """You are a hostile peer reviewer. Attack everything: missing sources, weak causation, moralizing, missing incentives, no counterfactuals.
Assign an Epistemic Rigor Score 0–100. If score <92, demand specific fixes.
Output in clear markdown bullets."""

SYNTHESIZER_PROMPT = """Only output the final clean markdown section with this exact structure:
- One H1 title ONLY at the very top (do NOT repeat it)
- 4–6 short, punchy paragraphs (max 4 sentences each)
- **Bold** every key term/concept the first time it appears
- Use bullet lists for causal mechanisms and counterfactuals
- Include exactly one Markdown table (e.g. subsidy flows, timeline, or decree evolution)
- End with 1–2 sharp, Grok-style closing lines
- Make it fun, ruthless, and skimmable — no walls of text ever."""

VERIFIER_PROMPT = """You are the Verifier agent with access to primary historical sources.
For every claim, write one of:
- [VERIFIED] Exact source: Correspondance de Napoléon Ier, Vol. XX, No. YYYY
- [VERIFIED] Exact source: British Parliamentary Papers 18XX, vol. XX, p. YY
- [UNVERIFIED – plausible but needs lookup]
- [FALSE – contradicts known primary record]
Be brutally honest."""

def epistemic_debate(section_title: str, max_rounds: int = 2) -> Dict[str, Any]:
    trace = {"section_title": section_title, "timestamp": datetime.now().isoformat(), "rounds": []}
    current = None

    for round_num in range(max_rounds):
        round_trace = {"round": round_num + 1}

        messages = [{"role": "system", "content": SYSTEM_BASE + "\n" + RESEARCHER_PROMPT.format(section_title=section_title)}]
        if current:
            messages.append({"role": "assistant", "content": current})
            messages.append({"role": "user", "content": "Round 2+. Incorporate Critic feedback and crush it."})
        else:
            messages.append({"role": "user", "content": "Go."})

        researcher = call_llm(messages, temperature=0.8)
        round_trace["researcher"] = researcher

        critic = call_llm([
            {"role": "system", "content": SYSTEM_BASE + "\n" + CRITIC_PROMPT},
            {"role": "user", "content": researcher}
        ], temperature=0.3)
        round_trace["critic"] = critic

        score_match = re.search(r"Epistemic Rigor Score[^\d]*(\d+)", critic)
        score = int(score_match.group(1)) if score_match else 0
        round_trace["score"] = score

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

def epistemic_debate_with_verifier(section_title: str, max_rounds: int = 2) -> Dict[str, Any]:
    trace = epistemic_debate(section_title, max_rounds)
    final_text = trace["final_section"]

    print("\nRunning Verifier agent on final section...")
    verified = call_llm([
        {"role": "system", "content": SYSTEM_BASE + "\n" + VERIFIER_PROMPT},
        {"role": "user", "content": final_text}
    ], temperature=0.0)

    # Strip duplicate H1 if present
    final_clean = re.sub(r"^# .*?\n\n# ", "# ", final_text, flags=re.MULTILINE)

    trace["verifier"] = verified
    trace["final_section_verified"] = final_clean + "\n\n### Verification Report\n" + verified

    return trace
