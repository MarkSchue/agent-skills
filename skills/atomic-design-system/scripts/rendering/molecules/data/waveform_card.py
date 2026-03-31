"""WaveformCard — waveform chart with big-number stat"""
from __future__ import annotations
from rendering.atoms.chart.waveform    import WaveformAtom
from rendering.atoms.data.stat_display  import StatDisplayAtom
from rendering.atoms.data.metric_footer import MetricFooterAtom

_waveform = WaveformAtom()
_stat     = StatDisplayAtom()
_footer   = MetricFooterAtom()


class WaveformCard:
    """Render a dark card with a waveform on the left and a large stat on the right."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.PAD
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        footer_h = ctx.card_footer_h(h, props)
        main_h   = h - footer_h - PAD
        left_w   = int(w * 0.42)
        right_x  = x + left_w + PAD
        right_w  = w - left_w - PAD * 2

        wdata = props.get("waveform-data") or []
        if isinstance(wdata, str):
            wdata = [float(v.strip()) for v in wdata.split(",") if v.strip()]

        _waveform.render(ctx, x + PAD, y + PAD, left_w - PAD, main_h - PAD,
                         wdata, fill=ctx.color("primary-container"))

        _stat.render(ctx, right_x, y + PAD, right_w, main_h - PAD,
                     value=str(props.get("value", "—")),
                     unit=str(props.get("unit", "")),
                     sublabel="",
                     val_color=ctx.color("surface"),
                     unit_color=ctx.color("surface"),
                     sub_color=ctx.color("on-surface-variant"),
                     align="right")

        _footer.render(ctx, x + PAD, y + h - footer_h, w - PAD * 2, footer_h,
                       left_label=str(props.get("left-label",  "")),
                       left_value="",
                       right_label=str(props.get("right-label", "")),
                       right_value=str(props.get("right-value", "")),
                       text_color=ctx.card_footer_color(props, default_token="text-secondary"),
                       sep_color=ctx.color("border-subtle"),
                       props=props)
