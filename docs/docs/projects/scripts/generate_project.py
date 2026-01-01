import os
import re
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# OpenAI client (API key is injected via GitHub Actions secret)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Repo paths
ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "docs" / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

# Date for frontmatter and filename
today = datetime.utcnow().strftime("%Y-%m-%d")

prompt = f"""
Choose a new topic. It must be non-dangerous, legal, and practical.
Create something impressive, demonstrable, and useful that a person can actually use or show.

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

# Generate content (allow web search for citations)
response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt,
    tools=[{"type": "web_search"}],
)

md = response.output_text.strip() + "\n"

# Extract title for filename
m = re.search(r"^title:\s*(.+)$", md, flags=re.MULTILINE)
title = m.group(1).strip() if m else "project"

slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
path = PROJECTS_DIR / f"{today}-{slug}.md"

# Write file
path.write_text(md, encoding="utf-8")
print(f"Wrote {path}")
