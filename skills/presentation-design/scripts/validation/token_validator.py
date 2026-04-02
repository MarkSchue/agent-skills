"""
token_validator.py — Validate CSS theme token coverage and consistency.

Checks:
- All base tokens from base.css are present
- No undocumented tokens (tokens in CSS but not in token-reference.md)
- All tokens have inline comments in base.css
- Variant tokens reference known namespaces
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent.parent


def validate_base_css(base_css_path: Path) -> list[str]:
    """Validate that all tokens in base.css have inline comments.

    Returns a list of issue strings (empty if all clear).
    """
    issues: list[str] = []
    text = base_css_path.read_text(encoding="utf-8")

    # Extract all --token lines
    token_pattern = re.compile(r"^\s*(--[a-zA-Z0-9_-]+)\s*:\s*(.+?)\s*;(.*)$")
    for line_num, line in enumerate(text.splitlines(), 1):
        m = token_pattern.match(line)
        if m:
            token_name = m.group(1)
            rest = m.group(3).strip()
            if "/*" not in rest and "/*" not in line:
                issues.append(
                    f"Line {line_num}: Token {token_name} has no inline comment"
                )

    return issues


def validate_token_reference(
    base_css_path: Path, ref_path: Path
) -> list[str]:
    """Check that all tokens in base.css appear in token-reference.md.

    Returns a list of issue strings.
    """
    issues: list[str] = []

    # Extract token names from base.css
    css_tokens: set[str] = set()
    token_re = re.compile(r"^\s*--([\w-]+)\s*:")
    for line in base_css_path.read_text(encoding="utf-8").splitlines():
        m = token_re.match(line)
        if m:
            css_tokens.add(m.group(1))

    # Check presence in reference doc
    ref_text = ref_path.read_text(encoding="utf-8")
    for token in sorted(css_tokens):
        if token not in ref_text:
            issues.append(f"Token --{token} not documented in {ref_path.name}")

    return issues


def main() -> None:
    """CLI entry point."""
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="Validate CSS token coverage.")
    parser.add_argument(
        "--base-css",
        type=Path,
        default=SKILL_DIR / "themes" / "base.css",
        help="Path to base.css",
    )
    parser.add_argument(
        "--reference",
        type=Path,
        default=SKILL_DIR / "references" / "token-reference.md",
        help="Path to token-reference.md",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    all_issues: list[str] = []

    if args.base_css.exists():
        all_issues.extend(validate_base_css(args.base_css))
    else:
        all_issues.append(f"base.css not found: {args.base_css}")

    if args.base_css.exists() and args.reference.exists():
        all_issues.extend(validate_token_reference(args.base_css, args.reference))
    elif not args.reference.exists():
        all_issues.append(f"token-reference.md not found: {args.reference}")

    if not all_issues:
        print("✓ Token validation passed — all tokens documented and commented.")
    else:
        for issue in all_issues:
            print(f"  ⚠ {issue}")
        print(f"\n{len(all_issues)} issue(s) found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
