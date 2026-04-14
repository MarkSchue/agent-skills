"""
AgendaInjector — Automatically inject agenda slides at section boundaries.

After the parser produces a ``DeckModel``, the AgendaInjector:
1. Extracts the section title list.
2. Builds an ``AgendaModel`` (enriched with per-entry metadata from
   ``deck.agenda_config`` if the ``<!-- agenda ... -->`` block is present).
3. Injects an agenda slide at the beginning of each section with the current
   section highlighted.
4. Tags injected slides with ``is_generated = True``.

The ``<!-- agenda ... -->`` block in the MD file can supply:
- ``icon`` dict  (name, visible, position, color, size) — shown beside card title
- ``sections`` list  — per-entry ``number`` and ``info`` overrides (matched by index)
"""

from __future__ import annotations

from scripts.models.agenda import AgendaModel
from scripts.models.deck import CardModel, DeckModel, SlideModel


class AgendaInjector:
    """Inject agenda slides into a ``DeckModel`` at section boundaries."""

    def inject(self, deck: DeckModel) -> DeckModel:
        """Insert an agenda slide at the start of every section.

        The agenda card on each injected slide highlights the current section
        via the ``highlight`` field.  When ``deck.agenda_config`` is set the
        injector uses its ``icon`` and per-entry ``info``/``number`` values.

        Args:
            deck: The parsed deck model.

        Returns:
            The same ``DeckModel`` instance, mutated with injected agenda slides.
        """
        if len(deck.sections) < 2:
            # Don't inject agenda for single-section decks
            return deck

        config = deck.agenda_config or {}

        # Honour the auto_agenda: false flag in the <!-- agenda --> block.
        # Defaults to True so existing decks without the key are unaffected.
        if not config.get("auto_agenda", True):
            return deck

        # Skip anonymous (empty-title) sections such as the title slide wrapper
        content_pairs = [
            (orig_idx, sec)
            for orig_idx, sec in enumerate(deck.sections)
            if sec.title.strip()
        ]

        if len(content_pairs) < 2:
            return deck

        section_titles = [sec.title for _, sec in content_pairs]

        if config:
            agenda = AgendaModel.from_agenda_config(section_titles, config)
        else:
            agenda = AgendaModel.from_section_titles(section_titles)

        for agenda_idx, (_, section) in enumerate(content_pairs):
            agenda_slide = self._build_agenda_slide(agenda, agenda_idx, config)
            section.slides.insert(0, agenda_slide)

        return deck

    @staticmethod
    def _build_agenda_slide(
        agenda: AgendaModel,
        active_index: int,
        config: dict,
    ) -> SlideModel:
        """Create an agenda ``SlideModel`` for a specific section.

        Args:
            agenda: The full agenda model.
            active_index: 0-based index of the currently active section.
            config: The parsed ``agenda_config`` dict (may be empty).

        Returns:
            A ``SlideModel`` tagged ``is_generated=True`` containing one
            ``agenda-card``.
        """
        active_agenda = agenda.with_active(active_index)

        # Build section entries — use rich-dict format when any entry has
        # number or info so col1/col3 render the custom values.
        has_extra = any(e.number or e.info for e in active_agenda.entries)
        if has_extra:
            sections_payload = [
                {
                    "title": e.title,
                    "number": e.number or f"{e.index + 1:02d}",
                    "info": e.info,
                }
                for e in active_agenda.entries
            ]
        else:
            sections_payload = [e.title for e in active_agenda.entries]

        # Left spacer — empty area giving the agenda card a right-aligned feel
        spacer = CardModel(
            title="",
            card_type="text-card",
            content={},
        )

        # Build icon dict from config (if present and visible)
        icon_cfg = config.get("icon") or {}
        icon: dict = {}
        if isinstance(icon_cfg, dict) and icon_cfg.get("visible"):
            icon = icon_cfg

        # Agenda card on the right; always single vertical column
        card = CardModel(
            title="Agenda",
            card_type="agenda-card",
            content={
                "sections": sections_payload,
                "highlight": active_index,
                "columns": 1,
            },
            icon=icon,
        )

        slide = SlideModel(
            title="Agenda",
            cards=[spacer, card],
            layout="grid-1x2",
            is_generated=True,
        )

        return slide
