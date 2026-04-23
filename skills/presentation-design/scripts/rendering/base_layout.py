"""
BaseLayoutRenderer — Abstract base for all layout renderers.

Handles shared slide chrome: title, subtitle, divider, logos, footer, page number.
Subclasses implement :meth:`compute_card_slots` to define card placement for
their specific grid geometry.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from scripts.models.deck import SlideModel
from scripts.models.theme import ThemeTokens
from scripts.rendering.base_card import RenderBox

_LOGO_EXTENSIONS = (".svg", ".png", ".jpg", ".jpeg")


class SlideChrome:
    """Pre-computed slide chrome geometry.

    Attributes:
        body_x: Left edge of the card body area.
        body_y: Top edge of the card body area (below title/divider).
        body_w: Width of the card body area.
        body_h: Height of the card body area (above footer).
    """

    __slots__ = ("body_x", "body_y", "body_w", "body_h")

    def __init__(self, body_x: float, body_y: float, body_w: float, body_h: float):
        self.body_x = body_x
        self.body_y = body_y
        self.body_w = body_w
        self.body_h = body_h


class BaseLayoutRenderer(ABC):
    """Abstract base for all layout renderers.

    Args:
        theme: The loaded ``ThemeTokens`` for the current deck.
        project_root: Optional path to the presentation project folder
            (used to locate logo files in ``assets/logos/``).
    """

    def __init__(self, theme: ThemeTokens, project_root: Path | None = None) -> None:
        self.theme = theme
        self.project_root = project_root

    # ── public API ────────────────────────────────────────────────────────

    def render(
        self,
        slide: SlideModel,
        *,
        page_number: int = 1,
    ) -> RenderBox:
        """Render the slide chrome and compute card slots.

        Returns a :class:`RenderBox` for the full canvas, populated with chrome
        elements and containing the card slot bounding boxes via the
        :meth:`compute_card_slots` return value.
        """
        overrides = slide.slide_overrides

        canvas_w = float(self._resolve("canvas-width", overrides) or 1280)
        canvas_h = float(self._resolve("canvas-height", overrides) or 720)

        canvas = RenderBox(0, 0, canvas_w, canvas_h)

        # Background
        bg = self._resolve("canvas-background-color", overrides) or "#FFFFFF"
        canvas.add(
            {
                "type": "rect",
                "x": 0,
                "y": 0,
                "w": canvas_w,
                "h": canvas_h,
                "fill": bg,
                "rx": 0,
            }
        )

        # Margins
        ml = float(self._resolve("canvas-padding-left", overrides) or 48)
        mr = float(self._resolve("canvas-padding-right", overrides) or 48)
        mt = float(self._resolve("canvas-padding-top", overrides) or 48)
        mb = float(self._resolve("canvas-padding-bottom", overrides) or 48)

        y_cursor = mt

        # Title
        if slide.title:
            title_size = float(
                self._resolve("slide-title-font-size", overrides) or 28
            )
            canvas.add(
                {
                    "type": "text",
                    "x": ml,
                    "y": y_cursor,
                    "w": canvas_w - ml - mr,
                    "h": title_size * 1.2 + 8,
                    "text": slide.title,
                    "font_size": title_size,
                    "font_color": self._resolve("slide-title-font-color", overrides)
                    or "#1A1A1A",
                    "font_weight": self._resolve(
                        "slide-title-font-weight", overrides
                    )
                    or "bold",
                    "alignment": self._resolve(
                        "slide-title-alignment", overrides
                    )
                    or "left",
                }
            )
            y_cursor += title_size * 1.2 + 8

        # Subtitle
        if slide.subtitle:
            sub_size = float(
                self._resolve("slide-subtitle-font-size", overrides) or 18
            )
            # Allocate 2 lines of height so longer subtitles don't get clipped
            # (the divider follows after this block, so the full allocation is safe)
            sub_h = sub_size * 2 + 8
            canvas.add(
                {
                    "type": "text",
                    "x": ml,
                    "y": y_cursor,
                    "w": canvas_w - ml - mr,
                    "h": sub_h,
                    "text": slide.subtitle,
                    "font_size": sub_size,
                    "font_color": self._resolve(
                        "slide-subtitle-font-color", overrides
                    )
                    or "#555555",
                    "wrap": True,
                }
            )
            y_cursor += sub_h

        # Divider line
        div_width = float(
            self._resolve("slide-divider-border-width", overrides) or 1
        )
        if div_width > 0:
            canvas.add(
                {
                    "type": "line",
                    "x1": ml,
                    "y1": y_cursor,
                    "x2": canvas_w - mr,
                    "y2": y_cursor,
                    "stroke": self._resolve(
                        "slide-divider-border-color", overrides
                    )
                    or "#CCCCCC",
                    "stroke_width": div_width,
                }
            )
            y_cursor += div_width + 8

        # Footer region — always rendered at its fixed position
        hide_footer = (
            overrides.get("hide-footer") or overrides.get("hide_footer", False)
        ) if overrides else False
        if not hide_footer:
            footer_y = self._render_footer(
                canvas, ml, mr, canvas_w, canvas_h, mb, page_number, overrides
            )
        else:
            footer_size = float(self._resolve("slide-footer-font-size", overrides) or 10)
            footer_y = canvas_h - mb - (footer_size + 16)

        # Take-away box — always sits directly above the footer
        take_away_data = (
            overrides.get("take-away") or overrides.get("take_away") or overrides.get("takeaway")
        ) if overrides else None
        take_away_top = footer_y  # default: no take-away, body ends at footer
        if take_away_data and isinstance(take_away_data, dict):
            ta_h = float(
                take_away_data.get("height")
                or self._resolve("slide-take-away-height", overrides)
                or 48
            )
            ta_width = (
                take_away_data.get("width")
                or self._resolve("slide-take-away-width", overrides)
                or "100%"
            )
            if isinstance(ta_width, str) and ta_width.strip().endswith("%"):
                ta_w = canvas_w * float(ta_width.strip().rstrip("%")) / 100
            else:
                ta_w = float(ta_width)
            ta_box_alignment = str(
                take_away_data.get("box_alignment")
                or self._resolve("slide-take-away-box-alignment", overrides)
                or "center"
            )
            if ta_w < canvas_w:
                if ta_box_alignment == "left":
                    ta_x = 0
                elif ta_box_alignment == "right":
                    ta_x = canvas_w - ta_w
                else:
                    ta_x = (canvas_w - ta_w) / 2
            else:
                ta_x = 0
                ta_w = canvas_w
            ta_bg = str(
                take_away_data.get("background_color")
                or self._resolve("slide-take-away-background-color", overrides)
                or "#E2001A"
            )
            # Resolve any var(--token) reference so exporters receive a plain hex value
            ta_bg = str(self.theme._resolve_var_reference(ta_bg) or ta_bg)
            ta_fc = str(
                take_away_data.get("font_color")
                or self._resolve("slide-take-away-font-color", overrides)
                or "#FFFFFF"
            )
            ta_fc = str(self.theme._resolve_var_reference(ta_fc) or ta_fc)
            ta_fs = float(
                take_away_data.get("font_size")
                or self._resolve("slide-take-away-font-size", overrides)
                or 14
            )
            ta_fw = str(
                take_away_data.get("font_weight")
                or self._resolve("slide-take-away-font-weight", overrides)
                or "bold"
            )
            ta_fs_style = str(
                take_away_data.get("font_style")
                or self._resolve("slide-take-away-font-style", overrides)
                or "normal"
            )
            ta_align = str(
                take_away_data.get("text_alignment")
                or self._resolve("slide-take-away-text-alignment", overrides)
                or take_away_data.get("alignment")
                or self._resolve("slide-take-away-alignment", overrides)
                or "center"
            )
            ta_pad_x = float(
                take_away_data.get("padding_x")
                or self._resolve("slide-take-away-padding-x", overrides)
                or ml
            )
            ta_text = str(take_away_data.get("text", ""))
            ta_margin_b = take_away_data.get("margin_bottom")
            if ta_margin_b is None or str(ta_margin_b).strip() == "":
                ta_margin_b = None
            else:
                ta_margin_b = float(ta_margin_b)
            footer_line_width = float(
                self._resolve("slide-footer-line-border-width", overrides) or 0
            )
            footer_overlap = footer_line_width / 2 if footer_line_width > 0 else 0
            below_footer_gap = ta_margin_b if ta_margin_b is not None else 0
            take_away_top = footer_y - ta_h - below_footer_gap + footer_overlap

            # Background bar
            canvas.add(
                {
                    "type": "rect",
                    "x": ta_x,
                    "y": take_away_top,
                    "w": ta_w,
                    "h": ta_h,
                    "fill": ta_bg,
                    "rx": 0,
                }
            )
            # Text centered vertically in bar — use full bar height with
            # vertical_align=middle so renderers that clip at cell boundaries
            # (e.g. draw.io) don't cut off content.
            canvas.add(
                {
                    "type": "text",
                    "x": ta_x + ta_pad_x,
                    "y": take_away_top,
                    "w": ta_w - ta_pad_x * 2,
                    "h": ta_h,
                    "text": ta_text,
                    "font_size": ta_fs,
                    "font_color": ta_fc,
                    "font_weight": ta_fw,
                    "font_style": ta_fs_style,
                    "alignment": ta_align,
                    "vertical_align": "middle",
                    "wrap": True,
                }
            )

        # Compute body region — stops at take-away box (or footer if no take-away)
        chrome = SlideChrome(
            body_x=ml,
            body_y=y_cursor,
            body_w=canvas_w - ml - mr,
            body_h=take_away_top - y_cursor - 8,
        )

        # Store chrome and card slots on the canvas for downstream use
        canvas.chrome = chrome  # type: ignore[attr-defined]
        canvas.card_slots = self.compute_card_slots(chrome, overrides)  # type: ignore[attr-defined]

        # Logos — rendered last so they appear on top of all card content in z-order
        self._render_logos(canvas, ml, mr, mt, overrides)

        return canvas

    @abstractmethod
    def compute_card_slots(
        self,
        chrome: SlideChrome,
        overrides: dict[str, Any] | None,
    ) -> list[RenderBox]:
        """Return a list of bounding boxes for card placement.

        Must be implemented by every subclass.
        """

    # ── token resolution ─────────────────────────────────────────────────

    def _resolve(self, token: str, overrides: dict[str, Any] | None = None) -> Any:
        return self.theme.resolve(token, overrides=overrides)

    # ── chrome rendering helpers ─────────────────────────────────────────

    def _find_all_logo_srcs(self) -> list[str]:
        """Return sorted list of all logo file paths in assets/logos/."""
        if not self.project_root:
            return []
        logos_dir = self.project_root / "assets" / "logos"
        if not logos_dir.is_dir():
            return []
        found = [
            f"logos/{f.name}"
            for f in sorted(logos_dir.iterdir())
            if f.suffix.lower() in _LOGO_EXTENSIONS and f.stat().st_size > 0
        ]
        return found

    def _find_logo_src(self) -> str | None:
        """Return the primary logo src (first file in assets/logos/), or None."""
        srcs = self._find_all_logo_srcs()
        return srcs[0] if srcs else None

    @staticmethod
    def _logo_xy(
        pos: str,
        ml: float, mr: float,
        canvas_w: float, canvas_h: float, mb: float,
        y_cursor: float,
        logo_w: float, logo_h: float, logo_padding: float,
    ) -> tuple[float, float]:
        """Compute (x, y) for a logo given its position token."""
        if pos == "top-left":
            return ml, y_cursor + logo_padding
        if pos == "bottom-left":
            return ml, canvas_h - mb - logo_h - logo_padding
        if pos == "bottom-right":
            return canvas_w - mr - logo_w, canvas_h - mb - logo_h - logo_padding
        # default: top-right
        return canvas_w - mr - logo_w, y_cursor + logo_padding

    def _render_logos(
        self,
        canvas: RenderBox,
        ml: float,
        mr: float,
        y: float,
        overrides: dict[str, Any] | None,
    ) -> float:
        """Render primary and secondary logos at their configured positions.

        Logos positioned at the top advance the returned Y cursor.
        Logos positioned at the bottom are placed absolutely and do not.
        """
        mb = float(self._resolve("canvas-padding-bottom", overrides) or 48)
        all_srcs = self._find_all_logo_srcs()
        y_after = y

        for idx, which in enumerate(("primary", "secondary")):
            logo_src = all_srcs[idx] if idx < len(all_srcs) else None
            # Secondary logo is optional — skip if no file exists
            if logo_src is None and which == "secondary":
                continue

            logo_w = float(self._resolve(f"slide-logo-{which}-width", overrides) or 100)
            logo_h = float(self._resolve(f"slide-logo-{which}-height", overrides) or 36)
            logo_padding = float(self._resolve(f"slide-logo-{which}-padding", overrides) or 12)
            default_pos = "top-right" if which == "primary" else "top-left"
            logo_pos = str(
                self._resolve(f"slide-logo-{which}-position", overrides) or default_pos
            )

            logo_x, logo_y = self._logo_xy(
                logo_pos, ml, mr, canvas.w, canvas.h, mb,
                y, logo_w, logo_h, logo_padding,
            )

            if logo_src:
                canvas.add_post(
                    {
                        "type": "image",
                        "src": logo_src,
                        "x": logo_x,
                        "y": logo_y,
                        "w": logo_w,
                        "h": logo_h,
                    }
                )
            else:
                # Primary logo placeholder only
                canvas.add_post(
                    {
                        "type": "placeholder",
                        "role": "logo-primary",
                        "x": logo_x,
                        "y": logo_y,
                        "w": logo_w,
                        "h": logo_h,
                    }
                )

            # Only top-positioned logos advance the y cursor
            if logo_pos.startswith("top"):
                y_after = max(y_after, logo_y + logo_h + logo_padding)

        return y_after

    def _render_footer(
        self,
        canvas: RenderBox,
        ml: float,
        mr: float,
        canvas_w: float,
        canvas_h: float,
        mb: float,
        page_number: int,
        overrides: dict[str, Any] | None,
    ) -> float:
        """Render footer line, text, and page number. Return the top Y of footer region."""
        footer_size = float(
            self._resolve("slide-footer-font-size", overrides) or 10
        )
        footer_h = footer_size + 16  # line + text + padding
        footer_top = canvas_h - mb - footer_h

        # Footer line
        footer_line_width = float(
            self._resolve("slide-footer-line-border-width", overrides) or 0
        )
        if footer_line_width > 0:
            canvas.add(
                {
                    "type": "line",
                    "x1": ml,
                    "y1": footer_top,
                    "x2": canvas_w - mr,
                    "y2": footer_top,
                    "stroke": self._resolve(
                        "slide-footer-line-border-color", overrides
                    )
                    or "#CCCCCC",
                    "stroke_width": footer_line_width,
                }
            )

        # Footer text placeholder (left-aligned)
        canvas.add(
            {
                "type": "placeholder",
                "role": "footer-text",
                "x": ml,
                "y": footer_top + 4,
                "w": canvas_w * 0.6,
                "h": footer_size,
            }
        )

        # Page number (right-aligned)
        pn_size = float(
            self._resolve("slide-page-number-font-size", overrides) or 10
        )
        canvas.add(
            {
                "type": "text",
                "x": canvas_w - mr - 40,
                "y": footer_top + 4,
                "w": 40,
                "text": str(page_number),
                "font_size": pn_size,
                "font_color": self._resolve(
                    "slide-page-number-font-color", overrides
                )
                or "#888888",
                "alignment": "right",
            }
        )

        return footer_top
