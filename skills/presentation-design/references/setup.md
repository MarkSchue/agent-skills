# Environment Setup Guide

## Prerequisites

- Python 3.10+
- `pip` package manager

## Virtual Environment

This skill uses a single canonical virtual environment at
`skills/presentation-design/.venv`. All scripts must run through this venv.

### Create the venv

```bash
cd skills/presentation-design
python3 -m venv .venv
```

### Activate it

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Verify

```bash
python -c "import python_pptx; print('OK')"
```

## Running Scripts

Always use the venv Python:

```bash
# Build a presentation
.venv/bin/python scripts/build_presentation.py \
  /path/to/presentation-definition.md \
  --stylesheet /path/to/theme.css \
  --output /path/to/output/presentation.pptx

# Scaffold a new presentation
.venv/bin/python scripts/scaffold_presentation.py \
  "My Presentation" \
  --path /path/to/target/directory
```

## Updating Dependencies

```bash
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```
