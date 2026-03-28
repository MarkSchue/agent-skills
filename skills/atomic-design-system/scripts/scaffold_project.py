#!/usr/bin/env python3
"""scaffold_project.py — create a new presentation project from scratch.

Usage
─────
    python scaffold_project.py <project-name> <theme>
                               [--primary <hex>]
                               [--secondary <hex>]
                               [--font <css-font-stack>]
                               [--brand <brand-label>]
                               [--out <workspace-root>]

Arguments
─────────
    project-name   Folder name for the new project (e.g. "myproject-carbon")
    theme          Base design system: materialdesign3 | carbon | liquidglass

Options
───────
    --primary   Override --color-primary hex value        (e.g. "#0f62fe")
    --secondary Override --color-secondary hex value      (e.g. "#6f6f6f")
    --font      Override --font-family CSS value          (e.g. '"Inter", sans-serif')
    --brand     Human-readable brand label for header comment (e.g. "Acme Corp")
    --out       Workspace root dir (default: current working directory)

What is created
───────────────
    <out>/<project-name>/
        theme.css     Full standalone copy of the base theme with brand overrides
                      applied directly in :root — no @import, one file.
        deck.md       Starter slide deck wired to the chosen theme
        output/       Build target (draw.io / pptx files go here)
        qa/           QA render target
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import textwrap
from datetime import date


# ─── Locate the designthemes directory relative to this script ───────────────

SCRIPT_DIR   = pathlib.Path(__file__).resolve().parent
THEMES_DIR   = SCRIPT_DIR.parent / "designthemes"
VALID_THEMES = {"materialdesign3", "carbon", "liquidglass"}

THEME_META = {
    "materialdesign3": {
        "label":       "Material Design 3 (Material You)",
        "reference":   "https://m3.material.io",
        "note":        "radii, spacing, elevation unchanged",
        "deck_title":  "New Presentation",
        "deck_ds":     "Google Material Design 3 (Material You) · Preset: material · Font: Roboto",
    },
    "carbon": {
        "label":       "IBM Carbon Design System v11 (White theme)",
        "reference":   "https://carbondesignsystem.com",
        "note":        "radii, spacing, elevation unchanged",
        "deck_title":  "New Presentation",
        "deck_ds":     "IBM Carbon Design System v11 · Preset: carbon · Font: IBM Plex Sans",
    },
    "liquidglass": {
        "label":       "Apple Human Interface Guidelines — Liquid Glass (WWDC 2025)",
        "reference":   "https://developer.apple.com/design/human-interface-guidelines",
        "note":        "radii, spacing, elevation unchanged",
        "deck_title":  "New Presentation",
        "deck_ds":     "Apple Liquid Glass (WWDC 2025) · Preset: liquidglass · Font: SF Pro Display",
    },
}


# ─── CSS helper: replace a single :root token value ─────────────────────────

def _replace_root_token(css: str, token: str, value: str) -> str:
    """Replace the value of a CSS custom property inside the :root block."""
    pattern = rf"({re.escape(token)}\s*:\s*)[^;]+;"
    return re.sub(pattern, rf"\g<1>{value};", css)


# ─── Build the project's theme.css from the base theme ──────────────────────

def build_theme_css(
    theme: str,
    project_name: str,
    brand_label: str | None,
    primary: str | None,
    secondary: str | None,
    font: str | None,
) -> str:
    base_path = THEMES_DIR / theme / "theme.css"
    if not base_path.exists():
        sys.exit(f"Error: base theme not found at {base_path}")

    css = base_path.read_text()
    meta = THEME_META[theme]
    today = date.today().strftime("%B %Y")

    # ── Build the project header ─────────────────────────────────────────────
    brand_line = f"   Brand:   {brand_label}" if brand_label else ""
    header = textwrap.dedent(f"""\
        /* ═══════════════════════════════════════════════════════════════════════════
           {project_name} — {brand_label + " × " if brand_label else ""}{meta["label"]}
           ═══════════════════════════════════════════════════════════════════════════
           Design System: {meta["label"]}
           Reference:     {meta["reference"]}
           Created:       {today}
        {'   Brand:   ' + brand_label if brand_label else ''}
           Base:    {meta["label"]} ({meta["note"]})

           BRAND CUSTOMIZATION CONTRACT
           ✔ CUSTOMIZE: --color-* tokens — replace with brand palette
           ✔ CUSTOMIZE: --font-family   — replace with brand typeface
           ✘ DO NOT CHANGE: --radius-*, --spacing-*, --elevation-* — design-system owned

           To apply brand overrides: edit --color-* and --font-family directly
           in the :root block below. No @import needed — this is a standalone file.
           ═══════════════════════════════════════════════════════════════════════════ */""").rstrip()

    # Remove empty lines from header (brand_line empty when no brand given)
    header = "\n".join(line for line in header.splitlines() if line.strip() or line == "")

    # Strip the existing file header (everything before the first :root {)
    root_pos = css.index(":root {")
    css = header + "\n\n\n" + css[root_pos:]

    # ── Apply brand token overrides inside :root ─────────────────────────────
    if primary:
        css = _replace_root_token(css, "--color-primary", primary)
    if secondary:
        css = _replace_root_token(css, "--color-secondary", secondary)
    if font:
        css = _replace_root_token(css, "--font-family", font)

    # ── Add brand-override comment block at end of :root ────────────────────
    # Only if at least one override was supplied — otherwise stays vanilla.
    overrides: list[str] = []
    if primary:
        overrides.append(f"  /* primary overridden: {primary} */")
    if secondary:
        overrides.append(f"  /* secondary overridden: {secondary} */")
    if font:
        overrides.append(f"  /* font-family overridden: {font} */")

    if overrides:
        override_block = (
            "\n  /* ── Brand Overrides Applied by Scaffold ─────────────────────────────── */\n"
            + "\n".join(overrides)
            + "\n"
        )
        # Insert just before the closing } of :root
        root_close = css.index("}", css.index(":root {"))
        css = css[:root_close] + override_block + css[root_close:]

    return css


# ─── Starter deck.md ─────────────────────────────────────────────────────────

def build_deck_md(theme: str, project_name: str, brand_label: str | None) -> str:
    meta  = THEME_META[theme]
    title = brand_label or project_name
    return textwrap.dedent(f"""\
        # {title}
        <!-- layout: hero-title -->

        {meta["deck_ds"]}

        # Slide Two
        <!-- layout: grid-3 -->

        ## KPI One
        <!-- card: kpi-card -->
        label: Metric A
        value: "—"
        trend: neutral

        ## KPI Two
        <!-- card: kpi-card -->
        label: Metric B
        value: "—"
        trend: neutral

        ## KPI Three
        <!-- card: kpi-card -->
        label: Metric C
        value: "—"
        trend: neutral

        # Slide Three
        <!-- layout: hero-title -->

        Add your content here.
    """)


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new Atomic Design System presentation project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("project_name", help="Folder name for the new project")
    parser.add_argument(
        "theme",
        choices=sorted(VALID_THEMES),
        help="Base design system theme",
    )
    parser.add_argument("--primary",   metavar="HEX",  help="Override --color-primary")
    parser.add_argument("--secondary", metavar="HEX",  help="Override --color-secondary")
    parser.add_argument("--font",      metavar="STACK", help="Override --font-family")
    parser.add_argument("--brand",     metavar="LABEL", help="Human-readable brand name")
    parser.add_argument(
        "--out",
        metavar="DIR",
        default=".",
        help="Workspace root (default: current directory)",
    )
    args = parser.parse_args()

    workspace = pathlib.Path(args.out).resolve()
    project   = workspace / args.project_name

    # ── Safety check ─────────────────────────────────────────────────────────
    if project.exists():
        sys.exit(f"Error: '{project}' already exists. Choose a different name or remove it first.")

    # ── Create folder structure ───────────────────────────────────────────────
    (project / "output").mkdir(parents=True)
    (project / "qa").mkdir(parents=True)

    # ── Write theme.css ───────────────────────────────────────────────────────
    theme_css = build_theme_css(
        theme=args.theme,
        project_name=args.project_name,
        brand_label=args.brand,
        primary=args.primary,
        secondary=args.secondary,
        font=args.font,
    )
    (project / "theme.css").write_text(theme_css)

    # ── Write deck.md ─────────────────────────────────────────────────────────
    deck_md = build_deck_md(
        theme=args.theme,
        project_name=args.project_name,
        brand_label=args.brand,
    )
    (project / "deck.md").write_text(deck_md)

    # ── Done ──────────────────────────────────────────────────────────────────
    print(f"Scaffolded project: {project}")
    print(f"  theme.css  — {len(theme_css.splitlines())} lines  (base: {args.theme})")
    print(f"  deck.md    — starter deck with 3 slides")
    print(f"  output/    — build target")
    print(f"  qa/        — QA render target")
    print()
    print("Next step:")
    print(f"  python scripts/drawio_builder.py {args.project_name}/deck.md")


if __name__ == "__main__":
    main()
