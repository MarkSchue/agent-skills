"""
rendering/atoms — visualization atom renderers
==============================================
Each class exposes a single ``render(ctx, ...)`` method that uses
the unified RenderContext API, so it works identically for both
draw.io and PPTX output.
"""
from .chart.waveform          import WaveformAtom
from .chart.dot_line          import DotLineAtom
from .data.stat_display       import StatDisplayAtom
from .data.metric_footer      import MetricFooterAtom
from .data.icon_title_header  import IconTitleHeaderAtom
from .ui.agenda_entry         import AgendaEntryAtom

__all__ = [
    "WaveformAtom",
    "DotLineAtom",
    "StatDisplayAtom",
    "MetricFooterAtom",
    "IconTitleHeaderAtom",
    "AgendaEntryAtom",
]
