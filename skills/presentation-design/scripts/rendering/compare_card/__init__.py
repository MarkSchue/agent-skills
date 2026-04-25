"""Compare-card renderer package.

Public surface kept identical to the previous single-file module so existing
imports ``from scripts.rendering.compare_card import CompareCardRenderer``
continue to work after the package split.
"""

from scripts.rendering.compare_card._renderer import CompareCardRenderer

__all__ = ["CompareCardRenderer"]
