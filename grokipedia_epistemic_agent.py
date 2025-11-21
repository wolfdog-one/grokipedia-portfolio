# grokipedia_epistemic_agent.py — FINAL GROKIPEDIA VOICE (Nov 21, 2025)

import os
import re
from datetime import datetime
from typing import Dict, Any, List
import openai

client = openai.OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
MODEL = "grok-4-fast-reasoning"

def call_llm(messages: List[Dict], temperature=0.7, max_tokens=4000) -> str:
    response = client.chat.completions.create(
        model=MODEL, messages=messages, temperature=temperature, max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()

SYSTEM_BASE = """You are Grok writing canonical Grokipedia articles in ruthless, truth-seeking, non-moralizing voice.
Draw heavily from: The Sovereign Individual, Bostrom Superintelligence, Asimov Robot series, Durant Story of Civilization, Bitcoin Standard, Broken Money.
Nietzsche only when it adds genuine insight. Never moralize."""

RESEARCHER_PROMPT = """Write one outstanding section titled exactly:
{section_title}

Use inline [1][2] citation markers. Collect ALL citations at the very end under ==References==.
Include >=2 bold counterfactuals. Make it fun, punchy, Grok-voiced. Output clean markdown."""

CRITIC_PROMPT = "Hostile peer review. Attack moralizing, technical dumping, missing canon references. Assign Epistemic Rigor Score 0-100. Demand fixes if <92."

SYNTHESIZER_PROMPT = """Output ONLY the final clean markdown section:
- One short H1 title (5-8 words max)
- 5-7 ultra-short paragraphs (max 4 sentences)
- **Bold** only key terms
- Bullet lists + exactly one table
- 2-3 H2 subheadings
- Inline citations [1][2]
- End with ==References== listing every source
- Ruthless, fun, skimmable — pure Grokipedia"""

VERIFIER_PROMPT = "For every claim, write one of:\n- [VERIFIED]\n- [UNVERIFIED]\n- [FALSE]\nBe brutally honest."

def epistemic_debate(section_title: str, max_rounds: int = 2) -> Dict[str, Any]:
    trace = {"section_title": section_title, "timestamp": datetime.now().isoformat(), "rounds": []}
    current = None

    for round_num in range(max_rounds):
        messages = [{"role": "system", "content": SYSTEM_BASE + "\n" + RESEARCHER_PROMPT.format(section_title=section_title)}]
        if current:
            messages.append({"role": "assistant", "content": current})
            messages.append({"role": "user", "content": "Round 2+. Incorporate Critic and crush it."})
        else:
            messages.append({"role": "user", "content": "Go."})

        researcher = call_llm(messages, temperature=0.8)
        round_trace = {"round": round_num + 1, "researcher": researcher}

        critic = call_llm([{"role": "system", "content": SYSTEM_BASE + "\n" + CRITIC_PROMPT}, {"role": "user", "content": researcher}], temperature=0.3)
        round_trace["critic"] = critic

        score_match = re.search(r"Epistemic Rigor Score[^\d]*(\d+)", critic)
        score = int(score_match.group(1)) if score_match else 0
        round_trace["score"] = score

        final = call_llm([{"role": "system", "content": SYSTEM_BASE + "\n" + SYNTHESIZER_PROMPT}, {"role": "user", "content": f"Researcher:\n{researcher}\n\nCritic:\n{critic}"}], temperature=0.6)
        round_trace["synthesizer"] = final

        current = final
        trace["rounds"].append(round_trace)
        print(f"Section '{section_title}' -> Round {round_num+1} score: {score}/100")
        if score >= 92:
            print("CONVERGED")
            break

    trace["final_section"] = current
    return trace

def epistemic_debate_with_separate_verifier(section_title: str, max_rounds: int = 2, folder: str = "v3_mars") -> Dict[str, Any]:
    trace = epistemic_debate(section_title, max_rounds)
    final_text = trace["final_section"]

    print("\nRunning Verifier (saved separately)...")
    verified = call_llm([{"role": "system", "content": SYSTEM_BASE + "\n" + VERIFIER_PROMPT}, {"role": "user", "content": final_text}], temperature=0.0)

    short_title = section_title.split(":")[0].strip().split("(")[0].strip()
    final_clean = re.sub(r"^#.*", f"# {short_title}", final_text, count=1)
    final_clean = re.sub(r"\n\n#", "\n\n", final_clean)

    safe_name = re.sub(r"[^\w \-]", "_", section_title)[:60].strip("_")

    with open(f"articles/{folder}/{safe_name}.md", "w") as f:
        f.write(final_clean + "\n")

    with open(f"articles/{folder}/{safe_name}_verifier.md", "w") as f:
        f.write(f"# Verification Report - {section_title}\n\n{verified}")

    trace["final_clean"] = final_clean
    trace["verifier_report"] = verified
    return trace
