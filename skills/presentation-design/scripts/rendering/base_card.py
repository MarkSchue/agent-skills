"""
BaseCardRenderer — Abstract base for all card renderers.

Every card renderer subclass must implement :meth:`render_body`. The base class
handles **all** chrome that is universal to every card type:

- card container geometry (background, border, radius, padding)
- card title rendering (full-width or narrowed when icon is present)
- **icon rendering** — optional icon glyph beside the title, left or right; drawn
  using the icon font family from ``.icon-set`` (``--icon-font-family``); controlled
  by the ``icon`` dict on the ``CardModel`` (keys: ``name``, ``visible``,
  ``position``, ``color``, ``size``) and/or ``--card-icon-*`` CSS tokens
- header line rendering (below title, gated on ``--card-title-line-visible: true``)
- **subtitle rendering** — optional muted caption below the header line;
  set via ``card.subtitle`` text (parser reads the top-level ``subtitle:`` YAML key);
  styled via ``--card-subtitle-*`` CSS tokens
- **footer area** — optional text and/or divider line at the bottom of every card,
  controlled entirely by CSS tokens on ``.card-base`` (and overridable per variant
  class or per card instance via ``style_overrides``):

    ``content.footer``            text string in card YAML   → supplies footer text
    ``--card-footer-line-visible``  CSS token / style_override → shows line even without text
    ``--card-footer-font-*``        typography tokens
    ``--card-footer-line-color/width`` line appearance tokens
    ``--card-footer-margin-top``    gap between body/line and footer

  The footer text and footer line are **independent**: the line renders whenever
  ``card-footer-line-visible`` is ``true``, regardless of whether any text is set.
  Vertical space is reserved from the body before ``render_body`` is called, so
  no subclass needs special-casing.

**Body ↔ Bullets design principle** — every card type that renders a ``body``
text field must also support a ``bullets`` list as a drop-in replacement.
When ``bullets`` is present and non-empty it takes precedence over ``body``.
Use the shared helpers :meth:`_bullet_list_height` and :meth:`_emit_bullet_list`
instead of duplicating the logic.  Both methods are implemented here in
``BaseCardRenderer`` so all subclasses automatically inherit them.

Subclasses should call ``self.resolve(token_name)`` to look up any token
value — this method transparently applies the override chain using the current
card's ``style_overrides`` and the renderer's variant name.

No renderer may short-circuit the priority chain by reading
``card.style_overrides`` or ``card.props`` directly for token lookups.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from scripts.models.deck import CardModel
from scripts.models.theme import ThemeTokens
from scripts.parsing.inline_markdown import text_and_runs


class RenderBox:
    """Axis-aligned bounding box for a rendered element.

    Attributes:
        x: Left edge in px.
        y: Top edge in px.
        w: Width in px.
        h: Height in px.
        elements: Child rendered elements (exporter-agnostic dicts).
    """

    __slots__ = ("x", "y", "w", "h", "elements", "post_elements", "chrome", "card_slots")

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.elements: list[dict[str, Any]] = []
        self.post_elements: list[dict[str, Any]] = []
        self.chrome: Any = None
        self.card_slots: Any = None

    def add(self, element: dict[str, Any]) -> None:
        self.elements.append(element)

    def add_post(self, element: dict[str, Any]) -> None:
        """Add an element that should be rendered on top of all card content."""
        self.post_elements.append(element)


class BaseCardRenderer(ABC):
    """Abstract base for all card renderers.

    Provides the full shared card chrome: container, title, header line, footer area
    (footer line and/or footer text), and body region geometry. Subclasses override
    only :meth:`render_body` to render card-type-specific content.

    The footer is fully operational for every card type without any subclass code:
    - Set ``content.footer`` text in the card YAML to show footer text.
    - Set ``--card-footer-line-visible: true`` via CSS or ``style_overrides`` to show
      the footer line separator even without text.
    - Both can be combined; they are styled independently through ``--card-footer-*``
      tokens on ``.card-base`` (overridable per variant class or per card instance).

    Args:
        theme: The loaded ``ThemeTokens`` for the current deck.
        variant: CSS variant class name (e.g. ``card--kpi``), or ``None``.
    """

    variant: str | None = None

    def __init__(self, theme: ThemeTokens) -> None:
        self.theme = theme
        self._card: CardModel | None = None
        self._slide_overrides: dict[str, Any] = {}

    # ── public API ────────────────────────────────────────────────────────

    def render(
        self,
        card: CardModel,
        box: RenderBox,
        *,
        slide_overrides: dict[str, Any] | None = None,
    ) -> RenderBox:
        """Render *card* into the given *box*.

        Args:
            card: The card model to render.
            box: The allocated bounding box for this card.
            slide_overrides: Per-slide overrides that should also feed into
                             token resolution (lower priority than card overrides).

        Returns:
            The *box* populated with render elements.
        """
        self._card = card
        self._slide_overrides = slide_overrides or {}

        # Optional card width reduction (as percent of allocated slot width).
        width_pct = self.resolve("card-width-pct")
        if width_pct is not None and width_pct != "":
            try:
                width_pct_f = float(width_pct)
            except (ValueError, TypeError):
                width_pct_f = None
            if width_pct_f is not None and 0 < width_pct_f < 100:
                new_w = box.w * width_pct_f / 100
                box.x += (box.w - new_w) / 2
                box.w = new_w

        # Container
        self._render_container(box)

        # Title + header line
        body_y = self._render_header(card, box)

        # ── Footer setup (must happen before body box so height is reserved) ──
        footer_text = ""
        if isinstance(card.content, dict):
            footer_text = card.content.get("footer", "") or ""

        # Resolve footer tokens once — used for sizing and later rendering
        footer_font_size   = float(self.resolve("card-footer-font-size")   or 10)
        footer_margin_top  = float(self.resolve("card-footer-margin-top")  or 8)
        footer_line_width  = float(self.resolve("card-footer-line-width")  or 1)
        footer_line_vis_raw = self.resolve("card-footer-line-visible")
        footer_line_visible = footer_line_vis_raw in (True, "true", "True")

        has_footer_text = bool(footer_text)
        has_footer      = has_footer_text or footer_line_visible

        # Reserve vertical space: text needs font-size + margin; line-only needs line-width + margin
        if has_footer_text:
            footer_height = footer_font_size + footer_margin_top
        elif footer_line_visible:
            footer_height = footer_line_width + footer_margin_top
        else:
            footer_height = 0

        # Body occupies the space between header and footer
        body_box = RenderBox(
            x=box.x + self._pad_left,
            y=body_y,
            w=box.w - self._pad_left - self._pad_right,
            h=box.y + box.h - body_y - self._pad_bottom - footer_height,
        )
        self.render_body(card, body_box)
        box.elements.extend(body_box.elements)

        # ── Render footer area ─────────────────────────────────────────────
        if has_footer:
            # Line y: sits margin_top above the text baseline (or above pad_bottom if no text)
            footer_line_y = (
                box.y + box.h
                - self._pad_bottom
                - (footer_font_size if has_footer_text else 0)
                - footer_margin_top
            )

            if footer_line_visible:
                box.add(
                    {
                        "type": "line",
                        "x1": box.x + self._pad_left,
                        "y1": footer_line_y,
                        "x2": box.x + box.w - self._pad_right,
                        "y2": footer_line_y,
                        "stroke": self.resolve("card-footer-line-color"),
                        "stroke_width": footer_line_width,
                    }
                )

            if has_footer_text:
                footer_text_y = box.y + box.h - self._pad_bottom - footer_font_size
                box.add(
                    {
                        "type": "text",
                        "x": box.x + self._pad_left,
                        "y": footer_text_y,
                        "w": box.w - self._pad_left - self._pad_right,
                        "h": footer_font_size,
                        **text_and_runs(footer_text),
                        "font_size": footer_font_size,
                        "font_color": (
                            self.resolve("card-footer-font-color")
                            or self.resolve("card-body-font-color")
                        ),
                        "font_weight": self.resolve("card-footer-font-weight") or "normal",
                        "font_style":  self.resolve("card-footer-font-style")  or "normal",
                        "alignment":   self.resolve("card-footer-alignment")   or "left",
                    }
                )

        self._card = None
        self._slide_overrides = {}
        return box

    @abstractmethod
    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render card-type-specific body content into *box*.

        Must be implemented by every subclass.
        """

    # ── token resolution ─────────────────────────────────────────────────

    def resolve(self, token_name: str) -> Any:
        """Resolve a token through the 4-level priority chain.

        Priority: card override → slide override → variant → base → fallback.
        """
        # Merge slide overrides (lower priority) with card overrides (higher)
        merged = {**self._slide_overrides}
        if self._card and self._card.style_overrides:
            merged.update(self._card.style_overrides)
        return self.theme.resolve(
            token_name,
            variant=self.variant,
            overrides=merged if merged else None,
        )

    def _resolve_tok(self, variant_prefix: str, name: str, default: Any = None) -> Any:
        """Resolve a token with automatic card-base fallback.

        Resolution order:

        0. ``card-{name}`` in instance/slide overrides — authors write
           ``card_heading_font_color`` (no card-type prefix) and it wins over
           any variant CSS token.
        1. ``card-{variant_prefix}-{name}`` in overrides, then variant CSS.
        2. ``card-{name}`` in base CSS.
        3. *default*.

        Using base token names in ``style_overrides`` (step 0) is the
        recommended approach: it keeps the presentation YAML free of
        card-type-specific token names.

        Usage in renderer::

            def _tok(self, name: str, default: Any = None) -> Any:
                return self._resolve_tok("my-card", name, default)

        Args:
            variant_prefix: The card-specific prefix without leading ``card-``
                (e.g. ``"timeline"`` → tries ``card-timeline-{name}``).
            name: Token suffix (e.g. ``"body-font-size"``).
            default: Fallback value when neither CSS layer defines the token.
        """
        # Step 0: base-name override wins over any variant CSS token.
        merged: dict = {**self._slide_overrides}
        if self._card and self._card.style_overrides:
            merged.update(self._card.style_overrides)
        if merged:
            base_key = f"card-{name}"
            candidate = merged.get(base_key)
            if candidate is None:
                candidate = merged.get(base_key.replace("-", "_"))
            if candidate is not None and candidate != "":
                return self.theme._resolve_var_reference(candidate, self.variant, merged)

        # Step 1 & 2: standard two-level CSS lookup.
        v = self.resolve(f"card-{variant_prefix}-{name}")
        if v is not None and v != "":
            return v
        v = self.resolve(f"card-{name}")
        return v if (v is not None and v != "") else default

    def _tok(self, name: str, default: Any = None) -> Any:
        """Resolve ``card-{prefix}-{name}`` → ``card-{name}`` priority chain.

        The *prefix* is derived from :attr:`variant` by stripping the
        ``card--`` class prefix (e.g. ``"card--timeline"`` → ``"timeline"``).
        Subclasses whose token prefix differs from their CSS variant name
        (e.g. ``gantt-chart`` uses ``gantt``) must override this method.
        """
        prefix = (self.variant or "").replace("card--", "")
        if not prefix:
            v = self.resolve(f"card-{name}")
            return v if (v is not None and v != "") else default
        return self._resolve_tok(prefix, name, default)

    def _f(self, name: str, default: float) -> float:
        """Resolve token as :class:`float` — shorthand for ``float(self._tok(…))``."""
        return float(self._tok(name, default))

    # ── private rendering helpers ────────────────────────────────────────

    def _pad_side(self, side: str) -> float:
        """Return padding for *side* (``top``, ``bottom``, ``left``, ``right``).

        Resolution order:
        1. ``card-padding-<side>`` — per-side override token
        2. ``card-padding``        — uniform padding token
        3. Hard-coded default 16
        """
        per_side = self.resolve(f"card-padding-{side}")
        if per_side is not None and per_side != "":
            return float(per_side)
        return float(self.resolve("card-padding") or 16)

    @property
    def _pad_left(self) -> float:
        return self._pad_side("left")

    @property
    def _pad_right(self) -> float:
        return self._pad_side("right")

    @property
    def _pad_top(self) -> float:
        return self._pad_side("top")

    @property
    def _pad_bottom(self) -> float:
        return self._pad_side("bottom")

    def _render_container(self, box: RenderBox) -> None:
        """Add a container rectangle element to *box*."""
        box.add(
            {
                "type": "rect",
                "x": box.x,
                "y": box.y,
                "w": box.w,
                "h": box.h,
                "fill": self.resolve("card-background"),
                "stroke": self.resolve("card-border-color"),
                "stroke_width": self.resolve("card-border-width"),
                "rx": self.resolve("card-border-radius"),
            }
        )

    def _render_header(self, card: CardModel, box: RenderBox) -> float:
        """Render title (+ optional icon), header line, and optional subtitle.

        Title line is controlled independently by ``--card-title-line-visible``
        (must be ``true``) *and* ``--card-title-line-width`` (must be > 0).
        Icon is drawn beside the title when ``card.icon.visible`` is truthy or
        ``--card-icon-visible`` CSS token is ``true``.
        Subtitle appears after the header line when ``card.subtitle`` text is set
        or ``--card-subtitle-visible`` is ``true``.

        Returns:
            The Y-coordinate at which body content should start.
        """
        # card-header-margin-top governs where the title sits vertically.
        # It defaults to card-padding but is a separate token so cards with
        # card-padding:0 (e.g. fullbleed image cards) still align with
        # neighbours that use the default padding.
        _hmt = self.resolve("card-header-margin-top")
        header_margin_top = float(_hmt) if (_hmt is not None and _hmt != "") else self._pad_top
        y = box.y + header_margin_top

        title_visible_raw = self.resolve("card-title-visible")
        title_visible = title_visible_raw not in (False, "false", "False")

        if card.title and title_visible:
            title_size = float(self.resolve("card-title-font-size") or 16)
            title_line_gap = float(self.resolve("card-title-line-gap") or 8)
            content_w = box.w - self._pad_left - self._pad_right

            # ── Icon resolution (card.icon dict takes priority over CSS tokens) ──
            icon_dict = card.icon if isinstance(card.icon, dict) else {}
            _icon_vis_raw = (
                icon_dict.get("visible")
                if icon_dict.get("visible") is not None
                else self.resolve("card-icon-visible")
            )
            icon_visible = _icon_vis_raw in (True, "true", "True")
            icon_name    = str(icon_dict.get("name") or self.resolve("card-icon-name") or "")
            icon_position = str(icon_dict.get("position") or self.resolve("card-icon-position") or "right")
            icon_size    = float(icon_dict.get("size") or self.resolve("card-icon-size") or 20)
            icon_color   = str(icon_dict.get("color") or self.resolve("card-icon-color") or "#000000")
            icon_gap     = float(self.resolve("card-icon-gap") or 8)
            icon_padding = float(self.resolve("card-icon-padding") or 0)
            icon_y_offset = float(icon_dict.get("offset") or self.resolve("card-icon-y-offset") or 0)
            icon_bg_color   = str(self.resolve("card-icon-background-color") or "transparent")
            icon_bg_radius  = float(self.resolve("card-icon-background-radius") or 0)
            icon_font_family = str(self.resolve("icon-font-family") or "Material Symbols Outlined")

            if icon_visible and icon_name:
                # Icon slot width: icon + padding on each side + gap to title
                icon_slot_w = icon_size + icon_padding * 2 + icon_gap
                text_w = max(content_w - icon_slot_w, 0)

                if icon_position == "left":
                    icon_x  = box.x + self._pad_left + icon_padding
                    title_x = box.x + self._pad_left + icon_slot_w
                else:  # right (default)
                    title_x = box.x + self._pad_left
                    icon_x  = box.x + self._pad_left + text_w + icon_gap + icon_padding

                # Optional icon background badge
                if icon_bg_color and icon_bg_color.lower() not in ("transparent", "none", ""):
                    box.add({
                        "type": "rect",
                        "x": icon_x - icon_padding,
                        "y": y + icon_y_offset - icon_padding,
                        "w": icon_size + icon_padding * 2,
                        "h": icon_size + icon_padding * 2,
                        "fill": icon_bg_color,
                        "stroke": "transparent",
                        "stroke_width": 0,
                        "rx": icon_bg_radius,
                    })

                # Icon glyph — emitted as a dedicated "icon" element so exporters
                # can render it as an actual SVG image rather than a ligature text.
                box.add({
                    "type": "icon",
                    "x": icon_x,
                    "y": y + icon_y_offset,
                    "w": icon_size,
                    "h": icon_size,
                    "name": icon_name,
                    "color": icon_color,
                    "font_family": icon_font_family,
                })

                # Title text — narrowed by the icon slot
                box.add({
                    "type": "text",
                    "x": title_x,
                    "y": y,
                    "w": text_w,
                    "h": title_size * 1.2 + title_line_gap,
                    **text_and_runs(card.title),
                    "font_size": title_size,
                    "font_color": self.resolve("card-title-font-color"),
                    "font_weight": self.resolve("card-title-font-weight"),
                })
            else:
                # No icon — full-width title
                box.add({
                    "type": "text",
                    "x": box.x + self._pad_left,
                    "y": y,
                    "w": content_w,
                    "h": title_size * 1.2 + title_line_gap,
                    **text_and_runs(card.title),
                    "font_size": title_size,
                    "font_color": self.resolve("card-title-font-color"),
                    "font_weight": self.resolve("card-title-font-weight"),
                })

            y += title_size * 1.2 + title_line_gap

            # ── Header line (gated on --card-title-line-visible AND line-width > 0) ──
            line_vis_raw = self.resolve("card-title-line-visible")
            line_visible = line_vis_raw in (True, "true", "True")
            line_width = self.resolve("card-title-line-width")
            try:
                line_width_f = float(line_width) if line_width else 0
            except (ValueError, TypeError):
                line_width_f = 0
            if line_visible and line_width_f > 0:
                box.add({
                    "type": "line",
                    "x1": box.x + self._pad_left,
                    "y1": y,
                    "x2": box.x + box.w - self._pad_right,
                    "y2": y,
                    "stroke": self.resolve("card-title-line-color"),
                    "stroke_width": line_width_f,
                })
                y += line_width_f

        # ── Subtitle (independent of title — renders even when title is absent) ──
        sub_text = str(getattr(card, "subtitle", "") or "").strip()
        sub_vis_raw = self.resolve("card-subtitle-visible")
        sub_visible = bool(sub_text) or (sub_vis_raw in (True, "true", "True"))
        if sub_visible and sub_text:
            sub_size = float(self.resolve("card-subtitle-font-size") or 12)
            sub_top = float(self.resolve("card-subtitle-margin-top") or 6)
            sub_bottom = float(self.resolve("card-subtitle-margin-bottom") or 8)
            y += sub_top
            box.add({
                "type": "text",
                "x": box.x + self._pad_left,
                "y": y,
                "w": box.w - self._pad_left - self._pad_right,
                "h": sub_size,
                **text_and_runs(sub_text),
                "font_size": sub_size,
                "font_color": str(self.resolve("card-subtitle-font-color") or "#888888"),
                "font_weight": str(self.resolve("card-subtitle-font-weight") or "400"),
                "font_style":  str(self.resolve("card-subtitle-font-style")  or "normal"),
                "alignment":   str(self.resolve("card-subtitle-alignment")   or "left"),
            })
            y += sub_size + sub_bottom
        elif card.title:
            body_gap_top = float(self.resolve("card-body-gap-top") or 8)
            y += body_gap_top

        return y

    # ── Shared bullet-list helpers ────────────────────────────────────────────

    def _bullet_list_height(
        self,
        bullets: list,
        b_size: float,
        line_height: float,
        w: float,
    ) -> float:
        """Return total pixel height needed to render *bullets* as a bullet list.

        Uses the same token-driven geometry as :meth:`_emit_bullet_list` so that
        height allocation and actual rendering are always in sync.  Any new tokens
        added to ``_emit_bullet_list`` should also be reflected here.

        Args:
            bullets: Raw bullet items (strings or dicts with inline-markdown).
            b_size: Body font size in px.
            line_height: Single line height in px (typically b_size * 1.3–1.5).
            w: Available width in px for the bullet column (marker + text).
        """
        from scripts.parsing.inline_markdown import strip_inline
        bullet_indent = float(self.resolve("card-body-bullet-indent") or 16)
        bullet_gap = float(self.resolve("card-bullet-gap") or 8)
        bullet_spacing = float(self.resolve("card-bullet-spacing") or 4)
        chars_per_line = max(1, int((w - bullet_indent - bullet_gap) / (b_size * 0.6)))
        total = 0.0
        for b in bullets:
            plain = strip_inline(str(b))
            lines = max(1, len(plain) // chars_per_line + 1)
            total += lines * line_height + bullet_spacing
        return total

    def _emit_bullet_list(
        self,
        box: "RenderBox",
        bullets: list,
        x: float,
        y: float,
        w: float,
        h: float,
        b_size: float,
        b_color: object,
        b_weight: str,
        b_align: str,
        line_height: float,
    ) -> None:
        """Emit a single ``bullet_list`` element into *box*."""
        from scripts.parsing.inline_markdown import text_and_runs, strip_inline
        _BULLET_CHAR = {
            "disc": "•", "circle": "○", "square": "■",
            "dash": "–", "arrow": "›", "none": "",
        }
        bullet_style_raw = self.resolve("card-bullet-style") or "square"
        bullet_char = _BULLET_CHAR.get(str(bullet_style_raw).strip().lower(), "■")
        bullet_color_raw = self.resolve("card-bullet-color")
        bullet_color = str(bullet_color_raw) if bullet_color_raw else str(b_color)
        try:
            bullet_size_raw = self.resolve("card-bullet-size")
            bullet_size = (
                float(bullet_size_raw)
                if bullet_size_raw and float(bullet_size_raw) > 0
                else b_size
            )
        except (ValueError, TypeError):
            bullet_size = b_size
        bullet_indent = float(self.resolve("card-body-bullet-indent") or 16)
        bullet_gap = float(self.resolve("card-bullet-gap") or 8)
        bullet_spacing = float(self.resolve("card-bullet-spacing") or 4)
        chars_per_line = max(1, int((w - bullet_indent - bullet_gap) / (b_size * 0.6)))
        items = []
        for b in bullets:
            plain = strip_inline(str(b))
            num_lines = max(1, len(plain) // chars_per_line + 1)
            item_h = num_lines * line_height + bullet_spacing
            items.append({**text_and_runs(str(b)), "h": item_h})
        box.add(
            {
                "type": "bullet_list",
                "x": x, "y": y, "w": w, "h": h,
                "items": items,
                "font_size": b_size,
                "font_color": b_color,
                "font_weight": b_weight,
                "alignment": b_align,
                "bullet_char": bullet_char,
                "bullet_color": bullet_color,
                "bullet_size": bullet_size,
                "bullet_indent": bullet_indent,
                "bullet_gap": bullet_gap,
                "bullet_spacing": bullet_spacing,
                "line_height": line_height,
                "wrap": True,
            }
        )
