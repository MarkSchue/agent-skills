"""Data normalization & parsing helpers for compare-card content."""

from __future__ import annotations

from typing import Any


def is_false(value: Any) -> bool:
    """Falsy CSS/YAML boolean equivalent."""
    return value in (False, "false", "False", "0", 0)


def is_true(value: Any) -> bool:
    """Truthy CSS/YAML boolean equivalent."""
    return value in (True, "true", "True", "1", 1)


def normalize_cell(raw: object) -> dict[str, Any]:
    """Normalise a raw cell value (string or dict) to a uniform dict."""
    if isinstance(raw, dict):
        return {
            "value": str(raw.get("value", raw.get("text", "")) or ""),
            "icon": str(raw.get("icon", "") or ""),
            "color": str(raw.get("color", "") or ""),
            "alignment": str(raw.get("alignment", "") or ""),
            "highlighted": bool(raw.get("highlighted", False)),
            "bg_color": str(raw.get("bg_color", "") or ""),
        }
    return {
        "value": str(raw) if raw is not None else "",
        "icon": "", "color": "", "alignment": "",
        "highlighted": False, "bg_color": "",
    }


def normalize_topic(raw: object) -> dict[str, Any]:
    """Normalise a raw topic value (string or dict) to a uniform dict."""
    if isinstance(raw, dict):
        return {
            "text": str(raw.get("text", "") or ""),
            "icon": str(raw.get("icon", "") or ""),
            "number": raw.get("number"),
        }
    return {"text": str(raw) if raw is not None else "", "icon": "", "number": None}


def parse_columns(content: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse ``content.columns`` to a list of ``{label, highlight}`` dicts (max 5)."""
    raw_cols = content.get("columns") or []
    columns: list[dict[str, Any]] = []
    for c in raw_cols[:5]:
        if isinstance(c, dict):
            columns.append({
                "label": str(c.get("label", "") or ""),
                "highlight": bool(c.get("highlight", False)),
            })
        else:
            columns.append({"label": str(c) if c is not None else "", "highlight": False})
    return columns


def parse_topic_cfg(content: dict[str, Any]) -> tuple[str, Any, Any]:
    """Return ``(label, visible_raw, width_pct_raw)`` from ``content.topic_col``."""
    cfg = content.get("topic_col") or {}
    if isinstance(cfg, dict):
        return str(cfg.get("label", "") or ""), cfg.get("visible"), cfg.get("width_pct")
    return "", None, None


def parse_rows(content: dict[str, Any], n_cols: int) -> list[dict[str, Any]]:
    """Parse ``content.rows`` ensuring every row has exactly ``n_cols`` cells."""
    rows: list[dict[str, Any]] = []
    for r in (content.get("rows") or []):
        if isinstance(r, dict):
            topic = normalize_topic(r.get("topic"))
            cells = [normalize_cell(c) for c in (r.get("cells") or [])]
        else:
            topic = normalize_topic(None)
            cells = []
        while len(cells) < n_cols:
            cells.append(normalize_cell(None))
        rows.append({"topic": topic, "cells": cells[:n_cols]})
    return rows


def parse_summary(content: dict[str, Any], n_cols: int) -> dict[str, Any] | None:
    """Parse ``content.summary`` → ``{topic_text, cells}`` or ``None``."""
    raw = content.get("summary")
    if not isinstance(raw, dict):
        return None
    cells = [normalize_cell(c) for c in (raw.get("cells") or [])]
    while len(cells) < n_cols:
        cells.append(normalize_cell(None))
    return {
        "topic_text": str(raw.get("topic", "") or ""),
        "cells": cells[:n_cols],
    }
