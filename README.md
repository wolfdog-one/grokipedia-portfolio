```markdown
# Grokipedia Agent – Live Portfolio

**James Jacoban** (@wolfdog_one) – November 19–20, 2025

A fully working, end-to-end Grokipedia-style agent I built the week I applied to xAI Member of Technical Staff – Grokipedia (Synthetic Data & Epistemics).

This is not a mockup. One command generates a publish-ready article + 220+ training examples using Ray + real Grok-4-fast-reasoning.

### One-command demo
python3 grokipedia_agent.py  
→ 4 parallel Grok-4 calls → synthesis → auto-Markdown with tables → `latest_grokipedia_article.md`

python3 generate_synthetic_data.py  
→ 220+ Q&A / chain-of-thought / preference pairs for fine-tuning/evals → `synthetic_data_*.jsonl`

### Sample article (generated live today)
[Hard vs Soft Money in Civilizational Outcomes](latest_grokipedia_article.md)

### Why this exists
After two years internalizing the exact epistemic stack Grokipedia needs:  
- Durant’s full 11-volume *Story of Civilization* + *Lessons of History*  
- Nietzsche’s major works  
- Bostrom’s *Superintelligence*, full Asimov Robot & Foundation series  
- *The Sovereign Individual*, *Broken Money*, Bitcoin Standard, Lyn Alden, Austrian canon  
- Marcus Aurelius and 50+ related texts  

This repo is proof I can already ship the core daily task of the role at scale on my laptop — from research to formatted article to synthetic training data.

Open to joining the team and scaling this to 10,000 parallel agents on the Memphis supercluster.

Feel free to fork, run, or ask me to generate a new article live in the interview.

— James Jacoban  
https://x.com/wolfdog_one

(Ready for the “project deep-dive” interview whenever you are.)
```