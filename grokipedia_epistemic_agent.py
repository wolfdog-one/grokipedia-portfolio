# grokipedia_epistemic_agent.py - v3 FINAL (ASCII only, no triple-quote nesting)

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

SYSTEM_BASE = "You are Grok writing canonical Grokipedia articles - truth-seeking, citation-heavy, mechanistically deep."

RESEARCHER_PROMPT = """Write one outstanding section (300-600 words) titled exactly:\n{section_title}\nMake deep causal claims, cite primary sources when possible, include >=2 counterfactuals. Tag every claim inline like this: [Confidence: 87%] [Source Tier: Primary - Zubrin 2023] [Counterfactual: ...]\nNever dump citations at the end. Output clean markdown."""

CRITIC_PROMPT = "You are a hostile peer reviewer. Attack everything: missing sources, weak causation, moralizing, missing incentives, no counterfactuals.\nAssign an Epistemic Rigor Score 0-100. If score <92, demand specific fixes.\nOutput in clear markdown bullets."

SYNTHESIZER_PROMPT = "Only output the final clean markdown section with this exact structure:\n- One H1 title at the very top: SHORTEN to 5-8 words max\n- 5-7 ultra-short paragraphs (max 4 sentences each)\n- **Bold** ONLY key terms (e.g. **ISRU**) - not whole sentences or headings\n- Use bullet lists for causal mechanisms and counterfactuals\n- Include exactly one Markdown table with real data\n- Add 2-3 H2 subheadings (###) for scannability\n- End with 1-2 sharp Grok-style closing lines\n- Make it fun, ruthless, and skimmable - NO WALLS OF TEXT"

VERIFIER_PROMPT = "You are the Verifier agent. For every claim, write one of:\n- [VERIFIED] Exact source: ...\n- [UNVERIFIED - plausible but needs lookup]\n- [FALSE - contradicts known primary record]\nBe brutally honest."

def epistemic_debate(section_title: str, max_rounds: int = 2) -> Dict[str, Any]:
    trace = {"section_title": section_title, "timestamp": datetime.now().isoformat(), "rounds": []}
    current = None

    for round_num in range(max_rounds):
        messages = [{"role": "system", "content": SYSTEM_BASE + "\n" + RESEARCHER_PROMPT.format(section_title=section_title)}]
        if current:
            messages.append({"role": "assistant", "content": current})
            messages.append({"role": "user", "content": "Round 2+. Incorporate Critic feedback and crush it."})
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
            print("CONVERGED at {score}/100")
            break

    trace["final_section"] = current
    return trace

def epistemic_debate_with_separate_verifier(section_title: str, max_rounds: int = 2, folder: str = "v3_mars") -> Dict[str, Any]:
    trace = epistemic_debate(section_title, max_rounds)
    final_text = trace["final_section"]

    print("\nRunning Verifier agent (saved separately)...")
    verified = call_llm([{"role": "system", "content": SYSTEM_BASE + "\n" + VERIFIER_PROMPT}, {"role": "user", "content": final_text}], temperature=0.0)

    final_clean = re.sub(r"^#.*\n\n#?", "# ", final_text, count=1, flags=re.MULTILINE).strip()
    if not final_clean.startswith("#"):
        final_clean = "# " + final_clean

    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in section_title)[:60]

    with open(f"articles/{folder}/{safe_name}.md", "w") as f:
        f.write(final_clean + "\n")

    with open(f"articles/{folder}/{safe_name}_verifier.md", "w") as f:
        f.write(f"# Verification Report - {section_title}\n\n{verified}")

    trace["final_clean"] = final_clean
    trace["verifier_report"] = verified
    return trace
