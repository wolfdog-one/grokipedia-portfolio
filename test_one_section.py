from grokipedia_epistemic_agent import epistemic_debate
import json
import os

section_title = "Napoleon’s Continental System as Proto-Central-Bank Warfare (1806–1814)"

os.makedirs("traces/v2_napoleon", exist_ok=True)
os.makedirs("articles/v2_napoleon", exist_ok=True)

trace = epistemic_debate(section_title, max_rounds=2)

with open(f"traces/v2_napoleon/01_continental_system_trace.json", "w") as f:
    json.dump(trace, f, indent=2)

with open(f"articles/v2_napoleon/01_continental_system.md", "w") as f:
    f.write(f"# {section_title}\n\n{trace['final_section']}")

print("\nFIRST EPISTEMIC SECTION GENERATED!")
print("Check:")
print("   articles/v2_napoleon/01_continental_system.md")
print("   traces/v2_napoleon/01_continental_system_trace.json")
