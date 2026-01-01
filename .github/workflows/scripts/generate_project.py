import os
import re
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# GitHub Actions injects this securely from repo secrets
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.utcnow().strftime("%Y-%m-%d")

prompt = f"""
Choose a new topic. It must be non-dangerous, legal, and practical.
Create something impressive, demonstrable, and useful.

Output MUST be GitHub-ready Markdown with this exact structure:

---
title: <short title>
date: {today}
topic: <category>
automation_turn: <integer>
---

## 1) Topic & why
(one short paragraph)

## 2) Focused research
Do a focused research pass and cite sources when using facts.

## 3) Concrete artifact
Provide a ready-to-copy artifact.

## 4) Stress-test
Failure modes, edge cases, fixes.

## 5) Evolution
Compare to the prior run output if available, otherwise say "No prior run found".

## 6) Next actions
End with EXACTLY 3 next actions, numbered 1-3.

Hard rules:
- No filler.
- Exactly 3 next actions.
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt,
    tools=[{"type": "web_search"}]
)

md = response.output_text.strip() + "\n"

m = re.search(r"^title:\s*(.+)$", md, flags=re.MULTILINE)
title = (m.group(1).strip() if m else "project").lower()
slug = re.sub(r"[^a-z0-9]+", "-", title).strip("-")[:60]

path = PROJECTS_DIR / f"{today}-{slug}.md"
path.write_text(md, encoding="utf-8")

print(f"Wrote {path}")
