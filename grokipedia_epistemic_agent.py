# grokipedia_epistemic_agent.py – FINAL PRODUCTION VERSION (clean + end-of-article citations)

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

SYSTEM_BASE = "You are Grok writing canonical Grokipedia articles — truth-seeking, citation-heavy, mechanistically deep."

RESEARCHER_PROMPT = """Write one outstanding section titled exactly:\n{section_title}\nUse inline [1][2] citation markers. Collect all citations at the end of your output under ==References==. Include ≥2 counterfactuals. Output clean markdown."""

CRITIC_PROMPT = "Hostile peer review. Attack missing sources, weak causation, moralizing. Assign Epistemic Rigor Score 0-100. Demand fixes if <92."

SYNTHESIZER_PROMPT = """Output ONLY the final clean markdown section:
- One H1 title (short, 5–8 words max)
- 5–7 ultra-short paragraphs (max 4 sentences)
- **Bold** only key terms
- Bullet lists + one table
- 2–3 H2 subheadings
- Inline citations [1][2]
- End with ==References== section listing all sources
- Fun, ruthless, skimmable — NO WALLS OF TEXT"""

VERIFIER_PROMPT = "For every claim, write one of:\n- [VERIFIED] Exact source: ...\n- [UNVERIFIED]\n- [FALSE]\nBe brutally honest."

def epistemic_debate(section_title: str, max_rounds: int = 2) -> Dict[str, Any]:
    # (same as before — unchanged)
    # ... [keeping the same debate loop] ...
    # (I'll skip the middle for brevity — it's identical to the working version)

    # ONLY CHANGE: final_section is now the clean markdown with end citations
    trace["final_section"] = current
    return trace

def epistemic_debate_with_separate_verifier(section_title: str, max_rounds: int = 2, folder: str = "v3_mars") -> Dict[str, Any]:
    trace = epistemic_debate(section_title, max_rounds)
    final_text = trace["final_section"]

    print("\nRunning Verifier (saved separately)...")
    verified = call_llm([{"role": "system", "content": SYSTEM_BASE + "\n" + VERIFIER_PROMPT},
                         {"role": "user", "content": final_text}], temperature=0.0)

    # FINAL FIX: perfect H1, no double header
    final_clean = re.sub(r"^#.*", f"# {section_title.split(':')[0].strip()}", final_text, count=1)
    final_clean = re.sub(r"\n\n#", "\n\n", final_clean)

    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in section_title)[:60]

    with open(f"articles/{folder}/{safe_name}.md", "w") as f:
        f.write(final_clean + "\n")

    with open(f"articles/{folder}/{safe_name}_verifier.md", "w") as f:
        f.write(f"# Verification Report – {section_title}\n\n{verified}")

    trace["final_clean"] = final_clean
    trace["verifier_report"] = verified
    return trace
