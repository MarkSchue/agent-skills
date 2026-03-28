"""input_utils.py — Smart user-input interpretation for molecule/atom renderers.

This module is the bridge between what a *user* writes in deck.md and what the
renderers expect. Users are not expected to know token names, hex codes, or
icon codepoints. These helpers accept whatever natural language form the user
provided and convert it to the canonical internal representation.

Public API
----------
resolve_color(raw, ctx, fallback)   – any color expression → hex string
resolve_icon(description)           – natural language icon name → unicode char
parse_numeric(raw, fallback=0.0)    – "35 (#color primary)" → 35.0
resolve_trend(raw)                  – "rising", "↑", "positive" → "up"
resolve_legend_position(raw)        – "bottom", "below", "under" → "below"
"""
from __future__ import annotations
import json
import pathlib
import re
import urllib.request


# ─────────────────────────────────────────────────────────────────────────────
# Numeric parsing
# ─────────────────────────────────────────────────────────────────────────────

_NUM_RE = re.compile(r'^\s*([+-]?[0-9]*\.?[0-9]+)')


def parse_numeric(raw, fallback: float = 0.0) -> float:
    """Extract a number from any user-supplied value string.

    Handles:
    - Plain numbers: ``35``, ``35.5``, ``-3``
    - Percentage strings: ``"35%"``
    - Annotated forms: ``"35 (#color primary)"``, ``"45 (color orange)"``
    - Strings with units: ``"12.1M"``, ``"84,500"``
    """
    if raw is None:
        return fallback
    s = str(raw).replace(",", "")
    m = _NUM_RE.match(s)
    return float(m.group(1)) if m else fallback


# ─────────────────────────────────────────────────────────────────────────────
# CSS named colors  (subset covering the most common ~50)
# ─────────────────────────────────────────────────────────────────────────────

_CSS_NAMES: dict[str, str] = {
    "aliceblue": "#F0F8FF", "antiquewhite": "#FAEBD7", "aqua": "#00FFFF",
    "aquamarine": "#7FFFD4", "azure": "#F0FFFF", "beige": "#F5F5DC",
    "bisque": "#FFE4C4", "black": "#000000", "blanchedalmond": "#FFEBCD",
    "blue": "#0000FF", "blueviolet": "#8A2BE2", "brown": "#A52A2A",
    "burlywood": "#DEB887", "cadetblue": "#5F9EA0", "chartreuse": "#7FFF00",
    "chocolate": "#D2691E", "coral": "#FF7F50", "cornflowerblue": "#6495ED",
    "cornsilk": "#FFF8DC", "crimson": "#DC143C", "cyan": "#00FFFF",
    "darkblue": "#00008B", "darkcyan": "#008B8B", "darkgoldenrod": "#B8860B",
    "darkgray": "#A9A9A9", "darkgreen": "#006400", "darkgrey": "#A9A9A9",
    "darkkhaki": "#BDB76B", "darkmagenta": "#8B008B", "darkolivegreen": "#556B2F",
    "darkorange": "#FF8C00", "darkorchid": "#9932CC", "darkred": "#8B0000",
    "darksalmon": "#E9967A", "darkseagreen": "#8FBC8F", "darkslateblue": "#483D8B",
    "darkslategray": "#2F4F4F", "darkturquoise": "#00CED1", "darkviolet": "#9400D3",
    "deeppink": "#FF1493", "deepskyblue": "#00BFFF", "dimgray": "#696969",
    "dimgrey": "#696969", "dodgerblue": "#1E90FF", "firebrick": "#B22222",
    "floralwhite": "#FFFAF0", "forestgreen": "#228B22", "fuchsia": "#FF00FF",
    "gainsboro": "#DCDCDC", "ghostwhite": "#F8F8FF", "gold": "#FFD700",
    "goldenrod": "#DAA520", "gray": "#808080", "green": "#008000",
    "greenyellow": "#ADFF2F", "grey": "#808080", "honeydew": "#F0FFF0",
    "hotpink": "#FF69B4", "indianred": "#CD5C5C", "indigo": "#4B0082",
    "ivory": "#FFFFF0", "khaki": "#F0E68C", "lavender": "#E6E6FA",
    "lavenderblush": "#FFF0F5", "lawngreen": "#7CFC00", "lemonchiffon": "#FFFACD",
    "lightblue": "#ADD8E6", "lightcoral": "#F08080", "lightcyan": "#E0FFFF",
    "lightgoldenrodyellow": "#FAFAD2", "lightgray": "#D3D3D3",
    "lightgreen": "#90EE90", "lightgrey": "#D3D3D3", "lightpink": "#FFB6C1",
    "lightsalmon": "#FFA07A", "lightseagreen": "#20B2AA", "lightskyblue": "#87CEFA",
    "lightslategray": "#778899", "lightslategrey": "#778899",
    "lightsteelblue": "#B0C4DE", "lightyellow": "#FFFFE0", "lime": "#00FF00",
    "limegreen": "#32CD32", "linen": "#FAF0E6", "magenta": "#FF00FF",
    "maroon": "#800000", "mediumaquamarine": "#66CDAA", "mediumblue": "#0000CD",
    "mediumorchid": "#BA55D3", "mediumpurple": "#9370DB",
    "mediumseagreen": "#3CB371", "mediumslateblue": "#7B68EE",
    "mediumspringgreen": "#00FA9A", "mediumturquoise": "#48D1CC",
    "mediumvioletred": "#C71585", "midnightblue": "#191970",
    "mintcream": "#F5FFFA", "mistyrose": "#FFE4E1", "moccasin": "#FFE4B5",
    "navajowhite": "#FFDEAD", "navy": "#000080", "oldlace": "#FDF5E6",
    "olive": "#808000", "olivedrab": "#6B8E23", "orange": "#FFA500",
    "orangered": "#FF4500", "orchid": "#DA70D6", "palegoldenrod": "#EEE8AA",
    "palegreen": "#98FB98", "paleturquoise": "#AFEEEE",
    "palevioletred": "#D87093", "papayawhip": "#FFEFD5",
    "peachpuff": "#FFDAB9", "peru": "#CD853F", "pink": "#FFC0CB",
    "plum": "#DDA0DD", "powderblue": "#B0E0E6", "purple": "#800080",
    "red": "#FF0000", "rosybrown": "#BC8F8F", "royalblue": "#4169E1",
    "saddlebrown": "#8B4513", "salmon": "#FA8072", "sandybrown": "#F4A460",
    "seagreen": "#2E8B57", "seashell": "#FFF5EE", "sienna": "#A0522D",
    "silver": "#C0C0C0", "skyblue": "#87CEEB", "slateblue": "#6A5ACD",
    "slategray": "#708090", "slategrey": "#708090", "snow": "#FFFAFA",
    "springgreen": "#00FF7F", "steelblue": "#4682B4", "tan": "#D2B48C",
    "teal": "#008080", "thistle": "#D8BFD8", "tomato": "#FF6347",
    "turquoise": "#40E0D0", "violet": "#EE82EE", "wheat": "#F5DEB3",
    "white": "#FFFFFF", "whitesmoke": "#F5F5F5", "yellow": "#FFFF00",
    "yellowgreen": "#9ACD32",
}

# Common natural-language color aliases that map to CSS names or design tokens
_COLOR_ALIASES: dict[str, str] = {
    # English adjective shortcuts
    "transparent": "transparent",
    "none": "transparent",
    # Warm/cool shorthands people write
    "light gray": "lightgray", "light grey": "lightgrey",
    "dark gray": "darkgray",   "dark grey": "darkgrey",
    "dark blue": "darkblue",   "light blue": "lightblue",
    "dark green": "darkgreen", "light green": "lightgreen",
    "dark red": "darkred",
    # Token-like English phrases → design-system token names
    "brand": "primary",
    "brand color": "primary",
    "brand blue": "primary",
    "brand red":   "primary",    # theme-dependent, but primary is the brand color
    "primary color": "primary",
    "accent": "accent",
    "accent color": "accent",
    "secondary": "secondary",
    "highlight": "primary",
    "emphasis": "primary",
    "warning color": "warning",
    "success color": "success",
    "error color":   "error",
    "danger":   "error",
    "muted": "on-surface-variant",
    "subtle": "surface-variant",
    "background": "surface",
    "card background": "bg-card",
    "white background": "surface",
    "neutral": "surface-variant",
}

_HEX_RE = re.compile(r'^#?[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3})?$')
_INLINE_COLOR_RE = re.compile(
    r'\((?:#color|color)\s+([^)]+)\)',  # (#color primary) or (color orange)
    re.IGNORECASE
)


def resolve_color(raw, ctx, fallback: str = "#000000") -> str:
    """Resolve any color expression the user might write to a hex string.

    Accepts:
    - Design-system token names:        ``"primary"``, ``"surface-variant"``
    - CSS named colors:                 ``"orange"``, ``"steelblue"``
    - Hex values:                       ``"#FF6600"``, ``"FF6600"``, ``"#F60"``
    - English phrases:                  ``"brand blue"``, ``"dark green"``
    - Annotated value strings:          ``"35 (#color primary)"``
    - Inline override in value fields:  ``"45 (color orange)"``
    Falls back to *fallback* when nothing matches.
    """
    if raw is None:
        return fallback

    raw_s = str(raw).strip()

    # 1. Extract inline annotation if this is a slice-value string like "35 (#color primary)"
    m = _INLINE_COLOR_RE.search(raw_s)
    if m:
        raw_s = m.group(1).strip()

    # Normalise: lower-case, collapse internal whitespace
    key = re.sub(r'\s+', ' ', raw_s.lower()).strip()

    # 2. Direct hex — return immediately
    candidate = raw_s.lstrip("#") if raw_s.startswith("#") else raw_s
    if _HEX_RE.match(raw_s):
        h = raw_s.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return f"#{h.upper()}"

    # 3. English alias → normalised token or CSS name
    if key in _COLOR_ALIASES:
        key = _COLOR_ALIASES[key]

    # 4. Try as a design-system token (--color-<key>)
    resolved = ctx.color(key.replace(" ", "-"))
    if _HEX_RE.match(resolved):
        h = resolved.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return f"#{h.upper()}"

    # 4b. Also try dot → hyphen normalisation (e.g. "on primary" → "on-primary")
    resolved = ctx.color(key.replace(" ", "-"))
    if _HEX_RE.match(resolved):
        h = resolved.lstrip("#")
        return f"#{h.upper()}"

    # 5. CSS named color lookup
    if key in _CSS_NAMES:
        return _CSS_NAMES[key]
    # Try without spaces (e.g. "dark blue" → "darkblue")
    no_space = key.replace(" ", "")
    if no_space in _CSS_NAMES:
        return _CSS_NAMES[no_space]

    return fallback


def slice_color(raw_value, ctx, palette_fallback: str) -> str:
    """Convenience wrapper: extract per-slice color from an annotated value string.

    If the value field contains an inline ``(#color token)`` or ``(color name)``
    annotation, resolve that color. Otherwise return *palette_fallback*.

    Examples::
        slice_color("35 (#color primary)", ctx, "#888")  → resolved primary hex
        slice_color("45 (color orange)",   ctx, "#888")  → "#FFA500"
        slice_color("20",                  ctx, "#888")  → "#888"
    """
    s = str(raw_value)
    m = _INLINE_COLOR_RE.search(s)
    if not m:
        return palette_fallback
    return resolve_color(m.group(1).strip(), ctx, palette_fallback)


# ─────────────────────────────────────────────────────────────────────────────
# Icon interpretation
# ─────────────────────────────────────────────────────────────────────────────

# Maps natural-language descriptions → a single representative Unicode character.
# These are used when a renderer draws an icon glyph inside a badge/tile.
# The character is rendered with the font set in font-family; in most cases a
# generic letter or emoji is acceptable for PPTX/draw.io text boxes.
#
# When a proper icon font (Material Icons, IBM Plex Icons) is embedded in the
# future, replace these single-char values with the corresponding ligature name
# e.g. { "person": "person" } (Material Icons ligature rendering).
_ICON_MAP: dict[str, str] = {
    # People / org
    "person": "👤", "user": "👤", "people": "👥",
    "business user": "👤", "employee": "👤", "worker": "👤",
    "team": "👥", "group": "👥", "users": "👥",
    "manager": "👤", "ceo": "👤", "vp": "👤", "director": "👤",
    "executive": "👤", "leader": "👤", "contact": "👤",
    # Business / finance
    "revenue": "💶", "money": "💶", "finance": "💶", "sales": "💶",
    "profit": "💶", "growth": "📈", "trend": "📈", "chart": "📊",
    "kpi": "📊", "metric": "📊", "data": "📊", "analytics": "📊",
    "performance": "📊", "dashboard": "📊",
    # Strategy / planning
    "strategy": "♟", "plan": "♟", "mission": "🎯", "goal": "🎯",
    "target": "🎯", "objective": "🎯", "vision": "🔭",
    "roadmap": "🗺", "timeline": "📅", "calendar": "📅",
    # Communication
    "email": "✉", "mail": "✉", "message": "✉", "chat": "💬",
    "phone": "📞", "call": "📞", "video": "📹", "meeting": "📹",
    "notification": "🔔", "alert": "🔔",
    # Location / global
    "location": "📍", "place": "📍", "address": "📍",
    "country": "🌍", "globe": "🌍", "world": "🌍", "global": "🌍",
    "building": "🏢", "office": "🏢", "headquarters": "🏢",
    # Technology
    "technology": "💻", "tech": "💻", "software": "💻", "code": "💻",
    "cloud": "☁", "server": "🖥", "database": "🗄",
    "security": "🔒", "lock": "🔒", "shield": "🛡",
    "api": "🔌", "integration": "🔌",
    # Operations / process
    "process": "⚙", "gear": "⚙", "settings": "⚙", "configuration": "⚙",
    "automation": "⚙", "workflow": "⚙", "pipeline": "⚙",
    "delivery": "📦", "package": "📦", "product": "📦",
    "service": "🛠", "support": "🛠", "maintenance": "🛠",
    "quality": "✅", "check": "✅", "done": "✅", "complete": "✅",
    "warning": "⚠", "issue": "⚠", "problem": "⚠",
    "star": "⭐", "award": "⭐", "favourite": "⭐",
    # Misc
    "idea": "💡", "light": "💡", "innovation": "💡",
    "document": "📄", "file": "📄", "report": "📄",
    "search": "🔍", "find": "🔍",
    "up": "↑", "down": "↓", "increase": "↑", "decrease": "↓",
    "plus": "+", "minus": "−", "add": "+",
    "info": "ℹ", "help": "❔", "question": "❔",
    "home": "🏠", "elevator": "🛗", "lift": "🛗",
    # Trend / direction indicators
    "trend-up":      "▲", "trend-down":    "▼", "trend-neutral": "●",
    # Time
    "time": "🕐", "timezone": "🕐", "clock": "🕐",
    # Web / URL
    "url": "🌐", "web": "🌐", "website": "🌐", "link": "🔗",
}

# Material Icons ligatures — rendered by passing the ligature name as text in
# the "Material Icons" / "Material Icons Outlined" / "Material Icons Round" font.
# Activate via CSS:  --icon-set: material;  --icon-font-family: "Material Icons Outlined";
_ICON_MAP_MATERIAL: dict[str, str] = {
    # People / org
    "person": "person", "user": "person", "people": "group",
    "business user": "manage_accounts", "employee": "badge", "worker": "engineering",
    "team": "group", "group": "group", "users": "people",
    "manager": "supervisor_account", "ceo": "person", "vp": "person",
    "director": "person", "executive": "person", "leader": "star",
    "contact": "contact_mail",
    # Business / finance
    "revenue": "euro_symbol", "money": "payments", "finance": "account_balance",
    "sales": "trending_up", "profit": "bar_chart", "growth": "trending_up",
    "trend": "trending_up", "chart": "bar_chart", "kpi": "speed",
    "metric": "analytics", "data": "analytics", "analytics": "analytics",
    "performance": "speed", "dashboard": "dashboard",
    # Strategy / planning
    "strategy": "psychology", "plan": "event_note", "mission": "flag",
    "goal": "flag", "target": "gps_fixed", "objective": "gps_fixed",
    "vision": "visibility", "roadmap": "map", "timeline": "timeline",
    "calendar": "calendar_today",
    # Communication
    "email": "email", "mail": "mail", "message": "message", "chat": "chat",
    "phone": "phone", "call": "call", "video": "videocam",
    "meeting": "video_call", "notification": "notifications",
    "alert": "notification_important",
    # Location / global
    "location": "location_on", "place": "place", "address": "home",
    "country": "public", "globe": "public", "world": "public", "global": "language",
    "building": "business", "office": "business", "headquarters": "corporate_fare",
    # Technology
    "technology": "computer", "tech": "devices", "software": "code",
    "code": "code", "cloud": "cloud", "server": "dns", "database": "storage",
    "security": "security", "lock": "lock", "shield": "shield",
    "api": "api", "integration": "hub",
    # Operations / process
    "process": "settings", "gear": "settings", "settings": "settings",
    "configuration": "tune", "automation": "auto_fix_high",
    "workflow": "account_tree", "pipeline": "account_tree",
    "delivery": "local_shipping", "package": "inventory_2", "product": "inventory",
    "service": "build", "support": "support_agent", "maintenance": "build_circle",
    "quality": "verified", "check": "check_circle", "done": "done",
    "complete": "task_alt", "success": "check_circle", "warning": "warning",
    "issue": "error_outline",
    "problem": "error", "star": "star", "award": "emoji_events",
    "favourite": "favorite",
    # Misc
    "idea": "lightbulb", "light": "lightbulb", "innovation": "auto_awesome",
    "document": "description", "file": "insert_drive_file", "report": "assessment",
    "search": "search", "find": "search",
    "up": "arrow_upward", "down": "arrow_downward",
    "increase": "trending_up", "decrease": "trending_down",
    "plus": "add", "minus": "remove", "add": "add",
    "info": "info", "help": "help_outline", "question": "help",
    "home": "home", "elevator": "elevator", "lift": "elevator",
    "wrench": "build", "tool": "build", "repair": "build",
    # Trend / direction indicators
    "trend-up":      "trending_up",   "trend-down":    "trending_down",
    "trend-neutral": "remove",
    # Time
    "time": "schedule", "timezone": "schedule", "clock": "access_time",
    # Web / URL
    "url": "language", "web": "language", "website": "language", "link": "link",
}

# Noto Emoji — standard codepoint emoji, same as default but kept as named set
# for explicit CSS --icon-set: noto; --icon-font-family: "Noto Color Emoji";
_ICON_MAP_NOTO: dict[str, str] = _ICON_MAP  # Noto renders the same Unicode chars

# Registry of known icon sets → (map_dict, prefer_letter_default)
_ICON_SET_MAPS: dict[str, dict] = {
    "emoji":            _ICON_MAP,
    "noto":             _ICON_MAP_NOTO,
    "material":         _ICON_MAP_MATERIAL,
    "material-outlined": _ICON_MAP_MATERIAL,
    "material-rounded": _ICON_MAP_MATERIAL,
    "material-sharp":   _ICON_MAP_MATERIAL,
    "material-two-tone": _ICON_MAP_MATERIAL,
}

# Letter-based fallbacks when no emoji matches — used for single-char icon badges
_ICON_LETTER_MAP: dict[str, str] = {
    "person": "P", "user": "U", "team": "T", "group": "G",
    "revenue": "R", "sales": "S", "finance": "F",
    "strategy": "S", "mission": "M", "goal": "G", "objective": "O",
    "technology": "T", "tech": "T", "cloud": "C",
    "location": "L", "building": "B", "office": "O",
    "process": "P", "service": "S", "quality": "Q",
    "email": "E", "phone": "P",
}

# ──────────────────────────────────────────────────────────────────────────────
# Icon path disk-cache  (persists across builds so network is only hit once per
# new icon name; completely optional — degrades gracefully if offline)
# ──────────────────────────────────────────────────────────────────────────────

_ICON_CACHE_PATH: pathlib.Path = pathlib.Path(__file__).parent / "icon_cache.json"
# In-memory mirror of the cache file; populated at module-load and on each fetch
_RUNTIME_ICON_CACHE: dict[str, str] = {}


def _load_icon_cache() -> None:
    """Populate _RUNTIME_ICON_CACHE from the JSON file on disk (if present)."""
    global _RUNTIME_ICON_CACHE
    if _ICON_CACHE_PATH.exists():
        try:
            _RUNTIME_ICON_CACHE = json.loads(_ICON_CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            _RUNTIME_ICON_CACHE = {}


_load_icon_cache()


def _save_icon_cache() -> None:
    """Persist _RUNTIME_ICON_CACHE to disk (best-effort, never raises)."""
    try:
        _ICON_CACHE_PATH.write_text(
            json.dumps(_RUNTIME_ICON_CACHE, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    except Exception:
        pass


def _extract_paths_from_svg(svg_text: str) -> str | None:
    """Extract all <path d="…"> values from an SVG string.

    Joins multiple paths with a space and strips Material Icons' bounding-box
    placeholder ``M0 0h24v24H0V0z`` so only the visible geometry remains.
    Returns ``None`` if no usable path data is found.
    """
    paths = re.findall(r'<path[^>]*\sd="([^"]+)"', svg_text)
    # Also catch d='…' (single-quoted)
    paths += re.findall(r"<path[^>]*\sd='([^']+)'", svg_text)
    _BB = {"M0 0h24v24H0V0z", "M0,0h24v24H0V0z"}
    clean = [p for p in paths if p.strip() not in _BB]
    result = " ".join(clean).strip()
    return result if result else None


# CDN sources for Material Icons SVGs (Apache 2.0 license).
# Tried in order; first successful response wins.
_ICON_CDN_URLS = [
    # marella/material-icons npm mirror – filled/baseline variant
    "https://raw.githubusercontent.com/marella/material-icons/main/svg/{name}/baseline.svg",
    # jsDelivr npm CDN (same package, different host)
    "https://cdn.jsdelivr.net/npm/@material-icons/svg@1.0.33/svg/{name}/baseline.svg",
    # Google Fonts static CDN
    "https://fonts.gstatic.com/s/i/materialicons/{name}/v6/24px.svg",
]


def _fetch_icon_svg_path(lig_name: str) -> str | None:
    """Download the SVG for *lig_name* from a CDN, cache, and return the path d-string.

    Returns ``None`` if all CDN attempts fail (e.g. network unavailable or
    unknown icon name).  On success the result is stored in
    ``_RUNTIME_ICON_CACHE`` and persisted to ``icon_cache.json``.
    """
    for url_template in _ICON_CDN_URLS:
        url = url_template.format(name=lig_name)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "atomic-slides/1.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                svg_text = resp.read().decode("utf-8", errors="replace")
            d = _extract_paths_from_svg(svg_text)
            if d:
                _RUNTIME_ICON_CACHE[lig_name] = d
                _save_icon_cache()
                return d
        except Exception:
            continue
    return None


# ──────────────────────────────────────────────────────────────────────────────
# SVG path data for icon rendering (Material Icons style, 24×24 viewBox)
# ──────────────────────────────────────────────────────────────────────────────
# Keys are Material Icons ligature names (values of _ICON_MAP_MATERIAL).
# Paths may include "M0 0h24v24H0V0z" as a bounding-box placeholder — stripped
# automatically by _icon_d() before rendering.
# Paths sourced from: https://github.com/google/material-design-icons (Apache 2.0)
_ICON_SVG_PATHS: dict[str, str] = {
    # Trend / direction
    "trending_up":     "M0 0h24v24H0V0z M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6h-6z",
    "trending_down":   "M0 0h24v24H0V0z M16 18l2.29-2.29-4.88-4.88-4 4L2 7.41 3.41 6l6 6 4-4 6.3 6.29L22 12v6h-6z",
    "remove":          "M0 0h24v24H0V0z M19 13H5v-2h14v2z",
    "arrow_upward":    "M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z",
    "arrow_downward":  "M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z",
    # Ratings / highlights
    "star":            "M0 0h24v24H0V0z M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27z",
    "emoji_events":    "M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z",
    # People / org
    "person":          "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
    "group":           "M0 0h24v24H0V0z M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z",
    "manage_accounts": "M10.67,13.02C10.45,13.01,10.23,13,10,13c-2.42,0-4.68,0.67-6.61,1.82C2.51,15.34,2,16.32,2,17.35V20h9.26C10.47,18.87,10,17.49,10,16C10,14.93,10.25,13.93,10.67,13.02z M20.75,16c0-0.22-0.03-0.42-0.06-0.63l1.14-1.01l-1-1.73l-1.45,0.49c-0.32-0.27-0.68-0.48-1.08-0.63L18,11h-2l-0.3,1.49c-0.4,0.15-0.76,0.36-1.08,0.63l-1.45-0.49l-1,1.73l1.14,1.01c-0.03,0.21-0.06,0.41-0.06,0.63s0.03,0.42,0.06,0.63l-1.14,1.01l1,1.73l1.45-0.49c0.32,0.27,0.68,0.48,1.08,0.63L16,21h2l0.3-1.49c0.4-0.15,0.76-0.36,1.08-0.63l1.45,0.49l1-1.73l-1.14-1.01C20.72,16.42,20.75,16.22,20.75,16z M17,18c-1.1,0-2-0.9-2-2s0.9-2,2-2s2,0.9,2,2S18.1,18,17,18z",
    # Business / finance
    "euro_symbol":     "M0 0h24v24H0V0z M15 18.5c-2.51 0-4.68-1.42-5.76-3.5H15v-2H8.58c-.05-.33-.08-.66-.08-1s.03-.67.08-1H15V9H9.24C10.32 6.92 12.5 5.5 15 5.5c1.61 0 3.09.59 4.23 1.57L21 5.3C19.41 3.87 17.3 3 15 3c-3.92 0-7.24 2.51-8.48 6H3v2h3.06c-.04.33-.06.66-.06 1s.02.67.06 1H3v2h3.52c1.24 3.49 4.56 6 8.48 6 2.31 0 4.41-.87 6-2.3l-1.78-1.77c-1.13.98-2.6 1.57-4.22 1.57z",
    "bar_chart":       "M0 0h24v24H0V0z M5 9.2h3V19H5zM10.6 5h2.8v14h-2.8zm5.6 8H19v6h-2.8z",
    "analytics":       "M3 3v18h18V3H3z M9 17H7v-5h2V17z M13 17h-2v-3h2V17z M13 12h-2v-2h2V12z M17 17h-2V7h2V17z",
    "speed":           "M20.38 8.57l-1.23 1.85c.38 1.15.58 2.37.58 3.58 0 4.42-3.58 8-8 8s-8-3.58-8-8S7.58 4 12 4c1.9 0 3.63.66 5 1.75l1.77-1.77C17.09 2.73 14.65 2 12 2 6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10c0-1.52-.34-2.96-.95-4.25l-.67.82zM12 8l-4 7h8l-4-7z",
    "dashboard":       "M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z",
    # Strategy / planning
    "flag":            "M14.4 6L14 4H5v17h2v-7h5.6l.4 2h7V6z",
    "gps_fixed":       "M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z",
    "map":             "M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM15 19l-6-2.11V5l6 2.11V19z",
    "timeline":        "M23 8c0 1.1-.9 2-2 2-.18 0-.35-.02-.51-.07l-3.56 3.55c.05.16.07.34.07.52 0 1.1-.9 2-2 2s-2-.9-2-2c0-.18.02-.36.07-.52l-2.55-2.55c-.16.05-.34.07-.52.07s-.36-.02-.52-.07l-4.55 4.56c.05.16.07.33.07.51 0 1.1-.9 2-2 2s-2-.9-2-2 .9-2 2-2c.18 0 .35.02.51.07l4.56-4.55C8.02 9.36 8 9.18 8 9c0-1.1.9-2 2-2s2 .9 2 2c0 .18-.02.36-.07.52l2.55 2.55c.16-.05.34-.07.52-.07s.36.02.52.07l3.55-3.56C19.02 8.35 19 8.18 19 8c0-1.1.9-2 2-2s2 .9 2 2z",
    "event_note":      "M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z",
    # Location / global
    "location_on":     "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z",
    "home":            "M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z",
    "language":        "M0 0h24v24H0V0z M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95c-.32-1.25-.78-2.45-1.38-3.56 1.84.63 3.37 1.91 4.33 3.56zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.32-.14 2s.06 1.34.14 2H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56-1.84-.63-3.37-1.9-4.33-3.56zm2.95-8H5.08c.96-1.66 2.49-2.93 4.33-3.56C8.81 5.55 8.35 6.75 8.03 8zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96zM14.34 14H9.66c-.09-.66-.16-1.32-.16-2s.07-1.35.16-2h4.68c.09.65.16 1.32.16 2s-.07 1.34-.16 2zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95c-.96 1.65-2.49 2.93-4.33 3.56zM16.36 14c.08-.66.14-1.32.14-2s-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2h-3.38z",
    "business":        "M0 0h24v24H0V0z M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10zm-2-8h-2v2h2v-2zm0 4h-2v2h2v-2z",
    "corporate_fare":  "M12 2C10.07 2 8.5 3.57 8.5 5.5c0 1.54.99 2.85 2.36 3.34L9.93 11H6.5C5.12 11 4 12.12 4 13.5V20H2v2h20v-2h-2v-6.5C20 12.12 18.88 11 17.5 11h-3.43l-.93-2.16C14.51 8.35 15.5 7.04 15.5 5.5 15.5 3.57 13.93 2 12 2zm0 2c.83 0 1.5.67 1.5 1.5S12.83 7 12 7s-1.5-.67-1.5-1.5S11.17 4 12 4zm-5.5 9H11v7H6v-6.5c0-.28.22-.5.5-.5zM13 13h4.5c.28 0 .5.22.5.5V20h-5v-7z",
    # Technology
    "code":            "M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z",
    "cloud":           "M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z",
    "security":        "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z",
    "shield":          "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z",
    "lock":            "M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z",
    # Operations / process
    "settings":        "M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z",
    "build":           "M0 0h24v24H0V0z M12.09 2.91C10.08.9 7.07.49 4.65 1.67l4.34 4.34-3 3-4.34-4.34C.48 7.1.89 10.09 2.9 12.1c1.86 1.86 4.58 2.35 6.89 1.48l9.82 9.82 3.71-3.71-9.78-9.79c.92-2.34.44-5.1-1.45-6.99z",
    "build_circle":    "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.49-10.71l-1.06 1.06c.28.45.44.98.44 1.54 0 1.65-1.35 3-3 3s-3-1.35-3-3 1.35-3 3-3c.56 0 1.08.16 1.53.44l1.06-1.06C13.68 7.72 12.88 7.5 12 7.5c-2.49 0-4.5 2.01-4.5 4.5s2.01 4.5 4.5 4.5 4.5-2.01 4.5-4.5c0-.88-.22-1.68-.61-2.37l-1.05.66z",
    "support_agent":   "M21 12.22C21 6.73 16.74 3 12 3c-4.69 0-9 3.65-9 9.28-.6.34-1 .98-1 1.72v2c0 1.1.9 2 2 2h1v-6.1c0-3.87 3.13-7 7-7s7 3.13 7 7V19h-8v2h8c1.1 0 2-.9 2-2v-1.22c.59-.31 1-.92 1-1.64v-2.3c0-.7-.41-1.31-1-1.62z M9 14c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm6 0c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1z",
    # Status / feedback
    "check_circle":    "M0 0h24v24H0V0z M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z",
    "warning":         "M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z",
    "info":            "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z",
    # Communication
    "email":           "M0 0h24v24H0V0z M22 4H2v16h20V4zm-2 4l-8 5-8-5V6l8 5 8-5v2z",
    "phone":           "M0 0h24v24H0V0z M21 15.46l-5.27-.61-2.52 2.52c-2.83-1.44-5.15-3.75-6.59-6.59l2.53-2.53L8.54 3H3.03C2.45 13.18 10.82 21.55 21 20.97v-5.51z",
    "schedule":        "M0 0h24v24H0V0z M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z",
    # Elevator / infrastructure
    "elevator":        "M21,3H3v18h18V3z M8.5,6c0.69,0,1.25,0.56,1.25,1.25c0,0.69-0.56,1.25-1.25,1.25S7.25,7.94,7.25,7.25C7.25,6.56,7.81,6,8.5,6z M11,14h-1v4H7v-4H6V9.5h5V14z M15.5,17L13,13h5L15.5,17z M13,11l2.5-4l2.5,4H13z",
    # Misc / ideas
    "lightbulb":       "M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26C17.81 13.47 19 11.38 19 9c0-3.86-3.14-7-7-7z",
    "auto_awesome":    "M19 9l1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25L19 9zm-7.5.5L9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23l1.25-2.75L23 19l-2.75-1.25L19 15z",
    "search":          "M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z",
    "description":     "M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z",
    "visibility":      "M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z",
    # Charts / data
    "bar_chart":       "M0 0h24v24H0V0z M5 9.2h3V19H5zM10.6 5h2.8v14h-2.8zm5.6 8H19v6h-2.8z",
}


def _icon_d(lig_name: str) -> str | None:
    """Return the clean SVG path d-string for a Material Icons ligature name.

    Resolution order (fastest to slowest):
    1. ``_ICON_SVG_PATHS`` – static dict bundled with the module (no I/O)
    2. ``_RUNTIME_ICON_CACHE`` – icons downloaded in previous builds and
       persisted to ``icon_cache.json`` next to this file
    3. Network fetch from Material Icons CDN – result is cached on disk so the
       next build is instant; never raises, returns ``None`` if offline/unknown.
    """
    _BB = {"M0 0h24v24H0V0z", "M0,0h24v24H0V0z"}

    def _strip(raw: str) -> str | None:
        d = raw
        for bb in _BB:
            d = d.replace(bb, "")
        d = d.strip()
        return d if d else None

    # 1. Static dict (no I/O, instant)
    raw = _ICON_SVG_PATHS.get(lig_name)
    if raw:
        return _strip(raw)

    # 2. Disk cache loaded at import time
    cached = _RUNTIME_ICON_CACHE.get(lig_name)
    if cached:
        return _strip(cached)

    # 3. Network fetch (updates disk cache for future builds)
    return _fetch_icon_svg_path(lig_name)


def icon_to_png_bytes(lig_name: str, size_px: int, color_hex: str) -> bytes | None:
    """Render a Material Icons ligature as a PNG and return raw bytes.

    Uses ``cairosvg`` for SVG→PNG conversion. returns ``None`` if the icon
    has no path data or if cairosvg is unavailable.
    """
    d = _icon_d(lig_name)
    if not d:
        return None
    try:
        import cairosvg  # type: ignore
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
            f'width="{size_px}" height="{size_px}">'
            f'<path d="{d}" fill="{color_hex}"/>'
            f'</svg>'
        )
        return cairosvg.svg2png(bytestring=svg.encode())
    except Exception:
        return None


def resolve_icon(description: str, prefer_letter: bool = False,
                 icon_set: str = "emoji") -> str:
    """Map a natural-language icon description to a renderable character.

    Parameters
    ----------
    description  : any string the user wrote in deck.md, e.g.
                   ``"business user"``, ``"chart"``, ``"M"``, ``"👤"``
    prefer_letter: if True return a compact single letter instead of emoji
                   (useful for small icon badges in cards).
    icon_set     : which icon set to use — matches ``--icon-set`` CSS token.
                   ``"emoji"`` (default) | ``"material"`` | ``"material-outlined"``
                   | ``"material-rounded"`` | ``"material-sharp"`` | ``"noto"``
                   When a ligature-based set is chosen (material*) the returned
                   string is the ligature name (e.g. ``"euro_symbol"``), which
                   must be rendered in the corresponding icon font.

    Returns
    -------
    A character or ligature name suitable for ctx.text() rendering.
    Falls back to the first upper-case letter of the description.
    """
    if not description:
        return "?"

    raw = description.strip()

    # Already a single char / emoji — return as-is
    if len(raw) == 1:
        return raw

    # Already an emoji (multi-byte but single grapheme cluster) — return as-is
    # Rough heuristic: code point > 127 and len <= 4 bytes
    if len(raw) <= 4 and any(ord(c) > 127 for c in raw):
        return raw

    key = raw.lower().strip()

    # Pick lookup dict based on icon set
    iset = icon_set.lower().strip() if icon_set else "emoji"
    lookup = _ICON_SET_MAPS.get(iset, _ICON_MAP)
    # For letter preference with emoji sets, use letter map; for ligature sets keep lookup
    if prefer_letter and iset in ("emoji", "noto", ""):
        lookup = _ICON_LETTER_MAP

    # Exact match
    if key in lookup:
        return lookup[key]

    # Partial-word match — scan for any keyword contained in the description
    for kw, char in lookup.items():
        if kw in key:
            return char

    # For ligature-based sets fall back to the raw description (it may itself be a valid ligature)
    if iset not in ("emoji", "noto", ""):
        # Return snake_case version of the description as a best-effort ligature
        return raw.lower().replace(" ", "_").replace("-", "_")

    # Token fallback (emoji sets)
    fallback_alpha = _ICON_LETTER_MAP.get(key) or _ICON_LETTER_MAP.get(
        next((k for k in _ICON_LETTER_MAP if k in key), ""), ""
    )
    if fallback_alpha:
        return fallback_alpha

    # Last resort: first upper-case letter of the description
    for c in raw:
        if c.isalpha():
            return c.upper()
    return "?"


# ─────────────────────────────────────────────────────────────────────────────
# Trend / direction interpretation
# ─────────────────────────────────────────────────────────────────────────────

_UP_WORDS  = {"up", "rise", "rising", "increase", "increasing", "positive",
              "good", "green", "higher", "growing", "growth", "↑", "⬆",
              "+", "gain", "improve", "improving"}
_DOWN_WORDS = {"down", "fall", "falling", "decrease", "decreasing", "negative",
               "bad", "red", "lower", "decline", "declining", "↓", "⬇",
               "-", "loss", "drop", "dropping", "worse"}


def resolve_trend(raw) -> str:
    """Normalise any trend expression to ``"up"``, ``"down"``, or ``"neutral"``.

    Accepts: ``"up"``, ``"rising"``, ``"+"``, ``"↑"``, ``"positive"``,
    ``"green"``, the equivalents for down, or anything else → ``"neutral"``.
    """
    if not raw:
        return "neutral"
    key = str(raw).strip().lower()
    if key in _UP_WORDS or key.startswith("+") or key.startswith("↑"):
        return "up"
    if key in _DOWN_WORDS or key.startswith("-") or key.startswith("↓"):
        return "down"
    return "neutral"


# ─────────────────────────────────────────────────────────────────────────────
# Legend position
# ─────────────────────────────────────────────────────────────────────────────

_LEGEND_POS_MAP: dict[str, str] = {
    # Canonical
    "below": "below", "above": "above", "right": "right", "left": "left",
    # Synonyms
    "bottom": "below", "under": "below", "beneath": "below", "down": "below",
    "top": "above", "over": "above",
    "side": "right", "sidebar": "right",
}


def resolve_legend_position(raw, default: str = "right") -> str:
    """Normalise any legend position description to ``right | left | above | below``."""
    if not raw:
        return default
    key = str(raw).strip().lower()
    return _LEGEND_POS_MAP.get(key, default)
