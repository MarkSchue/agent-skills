"""
AgendaInjector — Automatically inject agenda slides at section boundaries.

After the parser produces a ``DeckModel``, the AgendaInjector:
1. Extracts the section title list.
2. Builds an ``AgendaModel``.
3. Injects an agenda slide at the beginning of each section with the current
   section highlighted.
4. Tags injected slides with ``is_generated = True``.
"""

from __future__ import annotations

from scripts.models.agenda import AgendaModel
from scripts.models.deck import CardModel, DeckModel, SlideModel


class AgendaInjector:
    """Inject agenda slides into a ``DeckModel`` at section boundaries."""

    def inject(self, deck: DeckModel) -> DeckModel:
        """Insert an agenda slide at the start of every section.

        The agenda card on each injected slide highlights the current section
        via the ``highlight`` field.

        Args:
            deck: The parsed deck model.

        Returns:
            The same ``DeckModel`` instance, mutated with injected agenda slides.
        """
        if len(deck.sections) < 2:
            # Don't inject agenda for single-section decks
            return deck

        section_titles = deck.section_titles
        agenda = AgendaModel.from_section_titles(section_titles)

        for idx, section in enumerate(deck.sections):
            agenda_slide = self._build_agenda_slide(agenda, idx)
            section.slides.insert(0, agenda_slide)

        return deck

    @staticmethod
    def _build_agenda_slide(agenda: AgendaModel, active_index: int) -> SlideModel:
        """Create an agenda ``SlideModel`` for a specific section.

        Args:
            agenda: The full agenda model.
            active_index: 0-based index of the currently active section.

        Returns:
            A ``SlideModel`` tagged ``is_generated=True`` containing one
            ``agenda-card``.
        """
        active_agenda = agenda.with_active(active_index)

        # Left spacer — empty area giving the agenda card a right-aligned feel
        spacer = CardModel(
            title="",
            card_type="text-card",
            content={},
        )

        # Agenda card on the right; always single vertical column
        card = CardModel(
            title="Agenda",
            card_type="agenda-card",
            content={
                "sections": [e.title for e in active_agenda.entries],
                "highlight": active_index,
                "columns": 1,
            },
        )

        slide = SlideModel(
            title="Agenda",
            cards=[spacer, card],
            layout="grid-1x2",
            is_generated=True,
        )

        return slide
