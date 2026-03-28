"""
IconTitleHeaderAtom — section header with icon tile, title, subtitle, pill
===========================================================================
Renders a horizontal header row containing:
  • A square coloured icon tile (left-aligned)
  • A bold title + optional subtitle beside it
  • An optional right-aligned pill badge
"""
from __future__ import annotations


class IconTitleHeaderAtom:
    """Render an icon-tile header row with title, subtitle, and pill badge."""

    def render(self, ctx, x: int, y: int, w: int, row_h: int,
               icon_bg: str, title: str, subtitle: str,
               pill: str, pill_bg: str, pill_color: str,
               title_color: str, sub_color: str,
               icon_name: str = "") -> None:
        """
        Parameters
        ----------
        ctx         : RenderContext
        x, y        : top-left of the header zone (pixels)
        w           : total width of the header zone (pixels)
        row_h       : height of the header zone (pixels)
        icon_bg     : hex fill color for the icon tile
        title       : main title string
        subtitle    : optional subtitle (use "" to omit)
        pill        : text for the right-side pill badge (use "" to omit)
        pill_bg     : hex fill color for the pill
        pill_color  : hex text color for the pill
        title_color : hex color for the title text
        sub_color   : hex color for the subtitle text
        icon_name   : optional Material Icons concept name (e.g. "analytics")
        """
        LP     = 10
        tile_s = max(24, row_h - LP * 2)
        tile_y = y + (row_h - tile_s) // 2

        ctx.rect(x + LP, tile_y, tile_s, tile_s, fill=icon_bg,
                 stroke=ctx.icon_stroke(), radius=ctx.icon_radius(tile_s))
        if icon_name:
            ctx.draw_icon(x + LP, tile_y, tile_s, tile_s, icon_name,
                          color=ctx.icon_fg())

        pill_w  = max(60, len(pill) * 8 + 20) if pill else 0
        pill_h  = max(22, int(row_h * 0.40))
        tx      = x + LP + tile_s + LP
        tw      = w - (tx - x) - (pill_w + LP if pill else LP)
        t_sz    = max(14, int(row_h * 0.35))
        s_sz    = max(11, int(row_h * 0.24))

        if subtitle:
            t_y = y + LP
            ctx.text(tx, t_y, tw, t_sz + 4, title,
                     size=t_sz, bold=True, color=title_color,
                     align="left", valign="top")
            ctx.text(tx, t_y + t_sz + 2, tw, s_sz + 4, subtitle,
                     size=s_sz, color=sub_color,
                     align="left", valign="top")
        else:
            ctx.text(tx, y, tw, row_h, title,
                     size=t_sz, bold=True, color=title_color,
                     align="left", valign="middle")

        if pill:
            px = x + w - pill_w - LP
            py = y + (row_h - pill_h) // 2
            ctx.badge(px, py, pill_w, pill_h, pill,
                      fill=pill_bg, text_color=pill_color,
                      size=ctx.font_size("annotation"), radius=pill_h // 2)
