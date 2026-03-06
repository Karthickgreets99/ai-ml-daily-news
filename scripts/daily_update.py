from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from random import choice

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
NOTES_DIR = ROOT / "notes"
DATA_DIR = ROOT / "data"
LOG_FILE = DATA_DIR / "activity-log.jsonl"

TOPICS = [
    "LLM evaluation",
    "RAG quality",
    "agent reliability",
    "fraud detection ML",
    "identity verification AI",
    "feature engineering",
    "MLOps observability",
    "AI governance",
    "distributed inference",
    "payment risk modeling",
]

PROMPTS = [
    "Summarized one practical takeaway from an AI/ML paper and linked it to production systems.",
    "Captured one experiment idea for improving reliability, latency, or model quality.",
    "Added a short note on applying AI/ML patterns to fintech, identity, or platform engineering.",
    "Documented a lesson learned about evaluation, monitoring, or deployment tradeoffs.",
    "Recorded one production-minded architecture insight for scalable AI systems.",
]


def ensure_dirs() -> None:
    NOTES_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)


def today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def make_entry() -> dict:
    day = today_utc()
    topic = choice(TOPICS)
    summary = choice(PROMPTS)
    return {
        "date": day,
        "topic": topic,
        "summary": summary,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def already_logged(day: str) -> bool:
    if not LOG_FILE.exists():
        return False
    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("date") == day:
            return True
    return False


def append_log(entry: dict) -> None:
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def write_note(entry: dict) -> None:
    note = NOTES_DIR / f"{entry['date']}.md"
    content = f"""# AI/ML Activity — {entry['date']}\n\n## Topic\n{entry['topic']}\n\n## Note\n{entry['summary']}\n\n## Why it matters\nA small but real knowledge update that keeps this repository active and documents ongoing AI/ML learning.\n"""
    note.write_text(content, encoding="utf-8")


def build_readme() -> None:
    rows = []
    if LOG_FILE.exists():
        for line in reversed(LOG_FILE.read_text(encoding="utf-8").splitlines()[-14:]):
            if not line.strip():
                continue
            entry = json.loads(line)
            rows.append(f"- **{entry['date']}** — {entry['topic']}: {entry['summary']}")

    body = "\n".join(rows) if rows else "- No activity yet"
    content = f"""# Daily AI/ML Activity Bot\n\nThis repository is updated automatically once a day with a small, genuine AI/ML learning note.\n\n## Latest activity\n{body}\n\n## How it works\n- A GitHub Actions workflow runs on a daily schedule.\n- The workflow generates one dated note in `notes/`.\n- The README and JSONL log are updated and committed to the default branch.\n\n## Good practice\nUse this repo for authentic micro-updates: paper takeaways, experiment notes, benchmark observations, architecture insights, or links to code you actually worked on.\n"""
    README.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    day = today_utc()
    if already_logged(day):
        print(f"Entry already exists for {day}; nothing to do.")
        return
    entry = make_entry()
    append_log(entry)
    write_note(entry)
    build_readme()
    print(f"Logged AI/ML activity for {day}")


if __name__ == "__main__":
    main()
