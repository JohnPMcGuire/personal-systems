from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
DOCS_PROJECTS = ROOT / "docs" / "projects"

DOCS_PROJECTS.mkdir(parents=True, exist_ok=True)

def title_from_frontmatter(md: str) -> str | None:
    m = re.search(r"^title:\s*(.+)$", md, flags=re.MULTILINE)
    return m.group(1).strip() if m else None

# Copy project markdown into docs/projects for MkDocs to serve
for p in PROJECTS.glob("*.md"):
    (DOCS_PROJECTS / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")

items = []
for p in sorted(DOCS_PROJECTS.glob("*.md"), reverse=True):
    text = p.read_text(encoding="utf-8", errors="ignore")
    title = title_from_frontmatter(text) or p.stem
    items.append((p.name, title))

out = ["# Projects", "", "Auto-generated list of published projects.", ""]
for fname, title in items:
    out.append(f"- [{title}]({fname})")

(DOCS_PROJECTS / "index.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Wrote docs/projects/index.md with {len(items)} entries.")
