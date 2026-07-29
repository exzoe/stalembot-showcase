from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache"}
EXCLUDED_FILES = {Path(__file__).resolve()}
TEXT_SUFFIXES = {
    ".py", ".md", ".txt", ".toml", ".yml", ".yaml", ".json", ".ini", ".env",
}

PATTERNS = {
    "Telegram-style token": re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
    "Private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Credential assignment": re.compile(
        r"(?i)\b(?:token|secret|password|api[_-]?key)\b\s*=\s*"
        r"(?!replace_|your_|example|placeholder)[^\s#]{12,}"
    ),
}


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.resolve() in EXCLUDED_FILES:
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.name == ".env.example" or path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return files


def main() -> int:
    findings: list[str] = []
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                findings.append(f"{path.relative_to(ROOT)}:{line_number}: {label}")

    if findings:
        print("Potential secrets found:")
        print("\n".join(findings))
        return 1

    print("Secret scan passed: no high-confidence credentials found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
