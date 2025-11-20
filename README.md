# Grokipedia Agent – Live Portfolio

**James Jacoban** (@wolfdog_one) – November 19–20, 2025

A **fully working, end-to-end Grokipedia-style agent** I built the week I applied to xAI Member of Technical Staff – Grokipedia (Synthetic Data & Epistemics).

This is not a mockup. Run one command and it generates a publish-ready Grokipedia article + 220+ training examples using **Ray + real Grok-4-fast-reasoning**.

### One-command demo

```bash
python3 grokipedia_agent.py
→ 4 parallel Grok-4 calls → synthesis → auto-Markdown with tables → latest_grokipedia_article.md
Bashpython3 generate_synthetic_data.py
→ 220+ Q&A / chain-of-thought / preference pairs → synthetic_data_*.jsonl
Sample article (generated live today)
Hard vs Soft Money in Civilizational Outcomes
Why this exists
After two years internalizing the exact epistemic stack Grokipedia needs:

Durant’s full 11-volume Story of Civilization + Lessons of History
Nietzsche’s major works
Bostrom’s Superintelligence, full Asimov Robot & Foundation series
The Sovereign Individual, Broken Money, Bitcoin Standard, Lyn Alden, Austrian canon
Marcus Aurelius and 50+ related texts

I can already ship the core daily task of the role at scale on my laptop.
This repo is proof.
Open to joining the team and scaling this to 10,000 parallel agents on the Memphis supercluster.
Run it yourself
Bashpip install "ray[default]" openai python-dotenv
cp .env.example .env   # add your xAI API key
python3 grokipedia_agent.py
Feel free to fork, run, or ask me to generate a new article live in the interview.
— James Jacoban
https://x.com/wolfdog_one | jim@wolfdog.group