"""
rendering/molecules — molecule registry
========================================
``MOLECULE_REGISTRY`` maps every molecule slug to a pre-instantiated
renderer object that exposes ``render(ctx, props, x, y, w, h)``.

For chart-card, call ``ChartCard.render(ctx, chart_type, chart_data, x, y, w, h)``
directly (it needs chart_type + data instead of props).
"""
from .strategy.mission_card      import MissionCard
from .strategy.objective_card    import ObjectiveCard
from .strategy.quote_card        import QuoteCard
from .strategy.roadmap_panel     import RoadmapPanel
from .strategy.column_conclusion_card import ColumnConclusionCard
from .strategy.grid_card          import GridCard
from .strategy.numbered_list_card  import NumberedListCard
from .strategy.table_summary_card  import TableSummaryCard
from .strategy.step_card         import StepCard
from .strategy.table_card        import TableCard
from .strategy.timeline_card     import TimelineCard
from .strategy.user_story_card   import UserStoryCard
from .strategy.topic_card        import TopicCard
from .strategy.quarter_grid_card import QuarterGridCard
from .strategy.agenda_card       import AgendaCard

from .data.kpi_card           import KpiCard
from .data.trend_card         import TrendCard
from .data.comparison_card    import ComparisonCard
from .data.data_insight_panel import DataInsightPanel
from .data.chart_card         import ChartCard
from .data.waveform_card      import WaveformCard
from .data.dot_chart_card     import DotChartCard
from .data.stats_chart_panel  import StatsChartPanel
from .data.daily_header_card  import DailyHeaderCard

from .team.profile_card     import ProfileCard
from .team.team_grid_panel  import TeamGridPanel
from .team.contact_card     import ContactCard
from .team.location_card    import LocationCard
from .team.role_card        import RoleCard
from .team.header_list_card import HeaderListCard

# Pre-instantiated singletons — stateless, shared across slides
MOLECULE_REGISTRY: dict = {
    # Strategy
    "mission-card":        MissionCard(),
    "objective-card":      ObjectiveCard(),
    "quote-card":          QuoteCard(),
    "roadmap-panel":       RoadmapPanel(),
    "column-conclusion-card": ColumnConclusionCard(),
    "grid-card":            GridCard(),
    "numbered-list-card":   NumberedListCard(),
    "table-summary-card":   TableSummaryCard(),
    "step-card":           StepCard(),
    "table-card":          TableCard(),
    "timeline-card":       TimelineCard(),
    "user-story-card":     UserStoryCard(),
    "topic-card":          TopicCard(),        # legacy alias
    "stacked-text":        TopicCard(),        # preferred name
    "4-6-card":            QuarterGridCard(),  # numbered/icon quarter grid (4–6 items)
    "quarter-grid":        QuarterGridCard(),  # alternate slug
    "agenda-card":         AgendaCard(),
    # Data
    "kpi-card":            KpiCard(),
    "trend-card":          TrendCard(),
    "comparison-card":     ComparisonCard(),
    "data-insight-panel":  DataInsightPanel(),
    "chart-card":          ChartCard(),      # special: use chart_type + data
    "waveform-card":       WaveformCard(),
    "dot-chart-card":      DotChartCard(),
    "stats-chart-panel":   StatsChartPanel(),
    "daily-header-card":   DailyHeaderCard(),
    # Team
    "profile-card":        ProfileCard(),
    "team-grid-panel":     TeamGridPanel(),
    "contact-card":        ContactCard(),
    "location-card":       LocationCard(),
    "role-card":           RoleCard(),
    "header-list-card":    HeaderListCard(),
}

__all__ = ["MOLECULE_REGISTRY", "ChartCard", "StepCard", "TableCard"]
