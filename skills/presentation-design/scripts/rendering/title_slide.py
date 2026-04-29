"""
TitleSlideLayoutRenderer — Full-canvas title slide with no card slots.

Supports two visual modes controlled by ``--title-slide-layout`` token:
- ``split`` (default): left colour panel + right photo, MHP-template style.
- ``centered``: legacy full-slide centred title layout.
"""

from __future__ import annotations

from typing import Any

from scripts.rendering.base_layout import BaseLayoutRenderer, RenderBox, SlideChrome


class TitleSlideLayoutRenderer(BaseLayoutRenderer):
    """Layout renderer for ``title-slide`` — no card grid."""

    def __init__(self, theme, project_root=None) -> None:
        super().__init__(theme, project_root=project_root)

    def compute_card_slots(
        self,
        chrome: SlideChrome,
        overrides: dict[str, Any] | None,
    ) -> list[RenderBox]:
        """Title slide has zero card slots."""
        return []

    def render(self, slide, *, page_number: int = 1) -> RenderBox:
        """Render the title slide.

        In ``split`` layout mode (default) the slide is divided into a coloured
        left panel and an optional right-side image — matching the MHP speaker
        template.  In ``centered`` mode the legacy full-canvas centred layout
        is used.
        """
        overrides = slide.slide_overrides
        layout_mode = str(
            self._resolve("title-slide-layout", overrides) or "split"
        ).strip().lower()

        if layout_mode == "centered":
            return self._render_centered(slide, page_number=page_number)
        return self._render_split(slide, page_number=page_number)

    # ── split layout ──────────────────────────────────────────────────────

    def _render_split(self, slide, *, page_number: int = 1) -> RenderBox:
        """MHP-style split layout: left colour panel + right image."""
        overrides = slide.slide_overrides

        canvas_w = float(self._resolve("canvas-width", overrides) or 1280)
        canvas_h = float(self._resolve("canvas-height", overrides) or 720)

        # ── Canvas ────────────────────────────────────────────────────────
        canvas = RenderBox(0, 0, canvas_w, canvas_h)

        # ── Left-panel dimensions ─────────────────────────────────────────
        split_pct = float(
            self._resolve("title-slide-split-pct", overrides) or 40.5
        ) / 100
        split_x = round(canvas_w * split_pct)

        left_bg = str(
            self._resolve("title-slide-left-bg", overrides) or "#1612FF"
        )

        # Full-canvas white base (right side background)
        canvas.add({"type": "rect", "x": 0, "y": 0, "w": canvas_w, "h": canvas_h,
                    "fill": "#FFFFFF", "rx": 0})

        # Right-side image (covers right portion, rendered under the left panel)
        right_image = str(
            self._resolve("title-slide-image", overrides) or ""
        ).strip()
        if right_image:
            canvas.add({
                "type": "image",
                "src": right_image,
                "x": split_x,
                "y": 0,
                "w": canvas_w - split_x,
                "h": canvas_h,
                "fit": "cover",
            })

        # Left colour panel
        canvas.add({"type": "rect", "x": 0, "y": 0, "w": split_x, "h": canvas_h,
                    "fill": left_bg, "rx": 0})

        # ── Margin / padding ──────────────────────────────────────────────
        ml = float(self._resolve("canvas-padding-left", overrides) or 43)
        mt = float(self._resolve("canvas-padding-top", overrides) or 43)
        mb = float(self._resolve("canvas-padding-bottom", overrides) or 43)

        content_w = split_x - ml - 20  # 20px right gutter before the split

        # ── Event label pill ──────────────────────────────────────────────
        event_label = str(
            overrides.get("event-label") or overrides.get("event_label")
            or self._resolve("title-slide-event-label", overrides) or ""
        ).strip()

        label_y = mt
        if event_label:
            pill_bg = str(
                self._resolve("title-slide-event-label-color", overrides) or "#DDEF03"
            )
            pill_fc = str(
                self._resolve("title-slide-event-label-text-color", overrides) or "#262626"
            )
            pill_fs = float(
                self._resolve("title-slide-event-label-font-size", overrides) or 13
            )
            pill_h = pill_fs + 14
            pill_w = min(content_w, 260)
            pill_rx = pill_h / 2  # fully rounded pill

            canvas.add({
                "type": "rect",
                "x": ml,
                "y": label_y,
                "w": pill_w,
                "h": pill_h,
                "fill": pill_bg,
                "rx": pill_rx,
            })
            canvas.add({
                "type": "text",
                "x": ml,
                "y": label_y,
                "w": pill_w,
                "h": pill_h,
                "text": event_label,
                "font_size": pill_fs,
                "font_color": pill_fc,
                "font_weight": "600",
                "alignment": "center",
                "vertical_align": "middle",
                "wrap": False,
            })
            label_y += pill_h + 12

        # ── Hero title ────────────────────────────────────────────────────
        slide_title = slide.title or ""
        slide_subtitle = slide.subtitle or ""

        title_size = float(
            self._resolve("title-slide-title-font-size", overrides) or 40
        )
        title_color = str(
            self._resolve("title-slide-title-font-color", overrides) or "#FFFFFF"
        )
        title_weight = str(
            self._resolve("title-slide-title-font-weight", overrides) or "700"
        )

        # Position title in the lower-middle of the left panel
        title_h = title_size * 3.0  # allow 3 lines
        title_y = canvas_h * 0.40

        canvas.add({
            "type": "text",
            "x": ml,
            "y": title_y,
            "w": content_w,
            "h": title_h,
            "text": slide_title,
            "font_size": title_size,
            "font_color": title_color,
            "font_weight": title_weight,
            "alignment": "left",
            "wrap": True,
        })

        # ── Subtitle ──────────────────────────────────────────────────────
        if slide_subtitle:
            sub_size = float(
                self._resolve("title-slide-subtitle-font-size", overrides) or 16
            )
            sub_color = str(
                self._resolve("title-slide-subtitle-font-color", overrides) or "#E0E0FF"
            )
            sub_h = sub_size * 3.5
            sub_y = title_y + title_h + 8

            canvas.add({
                "type": "text",
                "x": ml,
                "y": sub_y,
                "w": content_w,
                "h": sub_h,
                "text": slide_subtitle,
                "font_size": sub_size,
                "font_color": sub_color,
                "alignment": "left",
                "wrap": True,
            })

        # ── Logos (post-elements, rendered on top) ────────────────────────
        self._render_logos(canvas, ml, 43, mt, overrides)

        # Minimal chrome stub (no cards)
        canvas.chrome = SlideChrome(  # type: ignore[attr-defined]
            body_x=ml, body_y=mt, body_w=content_w, body_h=canvas_h - mt - mb
        )
        canvas.card_slots = []  # type: ignore[attr-defined]

        return canvas

    # ── centered layout (legacy) ──────────────────────────────────────────

    def _render_centered(self, slide, *, page_number: int = 1) -> RenderBox:
        """Original full-canvas centred title layout."""
        saved_title = slide.title
        saved_subtitle = slide.subtitle
        slide.title = ""
        slide.subtitle = ""
        try:
            canvas = super().render(slide, page_number=page_number)
        finally:
            slide.title = saved_title
            slide.subtitle = saved_subtitle
        overrides = slide.slide_overrides

        chrome = canvas.chrome  # type: ignore[attr-defined]
        body_x = chrome.body_x
        body_y = chrome.body_y
        body_w = chrome.body_w
        body_h = chrome.body_h

        slide_title = saved_title or ""
        slide_subtitle = saved_subtitle or ""

        title_size = float(
            self._resolve("title-slide-title-font-size", overrides) or 40
        )
        title_color = (
            self._resolve("title-slide-title-font-color", overrides)
            or self._resolve("slide-title-font-color", overrides)
            or "#1A1A1A"
        )
        title_weight = str(self._resolve("title-slide-title-font-weight", overrides) or "700")

        title_h = title_size * 1.4
        title_y = body_y + body_h * 0.30

        canvas.add({
            "type": "text",
            "x": body_x,
            "y": title_y,
            "w": body_w,
            "h": title_h,
            "text": slide_title,
            "font_size": title_size,
            "font_color": title_color,
            "font_weight": title_weight,
            "alignment": "center",
            "wrap": True,
        })

        if slide_subtitle:
            sub_size = float(self._resolve("title-slide-subtitle-font-size", overrides) or 20)
            sub_color = (
                self._resolve("title-slide-subtitle-font-color", overrides)
                or self._resolve("slide-subtitle-font-color", overrides)
                or "#555555"
            )
            sub_h = sub_size * 2.5
            sub_y = title_y + title_h + 16

            canvas.add({
                "type": "text",
                "x": body_x,
                "y": sub_y,
                "w": body_w,
                "h": sub_h,
                "text": slide_subtitle,
                "font_size": sub_size,
                "font_color": sub_color,
                "alignment": "center",
                "wrap": True,
            })

        return canvas
