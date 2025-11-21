#!/usr/bin/env python3
import json
import glob
import random

traces = glob.glob("traces/v2_napoleon/*.json")
print(f"Found {len(traces)} debate traces — generating v2 synthetic data...")

examples = []
for trace_file in traces:
    with open(trace_file) as f:
        t = json.load(f)
    
    final = t["final_section_verified"]
    debate = "\n\n".join([f"Round {r['round']} — Researcher:\n{r['researcher']}\n\nCritic (score {r['score']}):\n{r['critic']}\n\nSynthesizer:\n{r['synthesizer']}" 
                         for r in t["rounds"]])
    
    examples.append({
        "messages": [
            {"role": "user", "content": f"Write about: {t['section_title']}"},
            {"role": "assistant", "content": debate + "\n\nFinal verified output:\n" + final}
        ],
        "preference": "good" if any(r["score"] >= 85 for r in t["rounds"]) else "bad"
    })

# Save
with open("synthetic/v2_napoleon/synthetic_v2_napoleon_250.jsonl", "w") as f:
    for ex in examples:
        f.write(json.dumps(ex) + "\n")

print(f"Generated {len(examples)} high-quality v2 examples → synthetic/v2_napoleon/")
