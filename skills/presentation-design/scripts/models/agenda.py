"""
Agenda model for tracking section entries and current-section highlighting.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgendaEntry:
    """One agenda item corresponding to a ``# Section`` heading.

    Attributes:
        index: 0-based position in the section list.
        title: Section title text.
        is_active: Whether this entry is the current/active section.
    """

    index: int = 0
    title: str = ""
    is_active: bool = False


@dataclass
class AgendaModel:
    """Complete agenda derived from the deck section list.

    Attributes:
        entries: Ordered list of agenda entries.
        column_count: Number of display columns (auto-computed or overridden).
    """

    entries: list[AgendaEntry] = field(default_factory=list)
    column_count: int | None = None  # None = auto

    @property
    def auto_columns(self) -> int:
        """Compute column count based on section count thresholds.

        1–4 sections → 1 column
        5–8 sections → 2 columns
        9+  sections → 3 columns
        """
        if self.column_count is not None:
            return self.column_count
        n = len(self.entries)
        if n <= 4:
            return 1
        if n <= 8:
            return 2
        return 3

    def with_active(self, active_index: int) -> AgendaModel:
        """Return a copy with ``is_active`` set for the given section index."""
        new_entries = []
        for entry in self.entries:
            new_entries.append(
                AgendaEntry(
                    index=entry.index,
                    title=entry.title,
                    is_active=(entry.index == active_index),
                )
            )
        return AgendaModel(entries=new_entries, column_count=self.column_count)

    @classmethod
    def from_section_titles(cls, titles: list[str]) -> AgendaModel:
        """Build an AgendaModel from a list of section title strings."""
        entries = [
            AgendaEntry(index=i, title=t)
            for i, t in enumerate(titles)
        ]
        return cls(entries=entries)
