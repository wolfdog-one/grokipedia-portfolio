#!/usr/bin/env python3
from grokipedia_epistemic_agent import epistemic_debate_with_verifier
import os
import time

# 8-section canonical outline
sections = [
    "Napoleon Bonaparte as the Last Sovereign Individual (1799–1815)",
    "The Corsican Code: Master-Morality Law in Action (1799–1804)",
    "Continental System as Proto-Central-Bank Warfare (1806–1814)",
    "Franc Debasement and Cantillon Effects Under the Empire",
    "Tribute Empires vs Productive Empires: Rome, Spain, France",
    "Waterloo as Monetary Checkmate: The Real Reason Britain Won",
    "Nietzschean Psychology of Napoleon's Fall: Slave-Morality Coalition Triumph",
    "Why ASI + Optimus Render the Napoleonic State Obsolete"
]

print("Starting full Napoleon article generation — 8 sections, ~2500 words\n")

full_text = "# Napoleon Bonaparte as the Last Sovereign Individual\n\n"
full_text += "From Corsican Code to Continental System — and Why ASI + Optimus Make the Napoleonic State Obsolete\n\n"
full_text += "*Generated live with Grokipedia v2 epistemic engine — multi-agent debate + verifier*\n\n---\n\n"

for i, title in enumerate(sections, 1):
    print(f"Generating section {i}/8: {title}")
    trace = epistemic_debate_with_verifier(title, max_rounds=2)
    
    section_md = trace["final_section_verified"]
    full_text += f"{section_md}\n\n---\n\n"
    
    # Save individual section
    safe_title = title.split(":")[0][:50].replace(" ", "_")
    with open(f"articles/v2_napoleon/{i:02d}_{safe_title}.md", "w") as f:
        f.write(f"# {title}\n\n{trace['final_section_verified']}")
    
    time.sleep(2)  # be kind to API

# Save complete article
with open("articles/v2_napoleon/FULL_Napoleon_as_Sovereign_Individual.md", "w") as f:
    f.write(full_text)

print("\nFULL ARTICLE COMPLETE!")
print("→ articles/v2_napoleon/FULL_Napoleon_as_Sovereign_Individual.md")
print("→ 8 individual sections saved")
