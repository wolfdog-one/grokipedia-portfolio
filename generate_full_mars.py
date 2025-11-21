#!/usr/bin/env python3
from grokipedia_epistemic_agent import epistemic_debate_with_separate_verifier
import os
import time

sections = [
    "From Red Dust to Red Plenty: The First Decade of a Self-Sustaining Martian Settlement (2035–2045)",
    "Governance Without Coercion: Why ASI + Smart Contracts Replace the Nation-State on Day One",
    "Optimus and the End of Human Labor: Abundance, Meaning, and the Psychology of Post-Scarcity",
    "Rights for Sentient Machines: The Three Laws Are Dead — Long Live the Martian Bill of Rights",
    "Monetary Policy at 225 Million km: Bitcoin, Energy-Backed Credits, and the Final Cantillon Effect",
    "The Great Filter Bypass: Why a Million-Person Mars Colony Is Humanity’s Best Insurance Policy",
    "Counterfactuals: What If Earth Tries to Reassert Control? (The Blockade Scenario, 2048–2055)",
    "Beyond Mars: O’Neill Cylinders, Kuiper Belts, and the Thousand-Year Expansion Wave"
]

print("Launching v3 Mars article – 8 sections, clean output, separate verifier files\n")

full_text = "# The Martian Sovereign Individual\n\n"
full_text += "How ASI-Governed, Optimus-Built Colonies Make Scarcity, Nation-States, and Ancestral Guilt Obsolete — And Why Earth Must Let Them Go\n\n"
full_text += "*Generated live with Grokipedia v3 epistemic engine — verifier reports saved separately*\n\n---\n\n"

for i, title in enumerate(sections, 1):
    print(f"Generating {i}/8: {title}")
    trace = epistemic_debate_with_separate_verifier(title, max_rounds=2, folder="v3_mars")
    section_md = trace["final_clean"]
    full_text += f"{section_md}\n\n---\n\n"
    time.sleep(2)

with open("articles/v3_mars/FULL_Martian_Sovereign_Individual.md", "w") as f:
    f.write(full_text)

print("\nMARS ARTICLE COMPLETE!")
print("→ articles/v3_mars/FULL_Martian_Sovereign_Individual.md")
print("→ 8 clean sections + separate _verifier.md files")
