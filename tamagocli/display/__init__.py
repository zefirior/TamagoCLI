"""Display and rendering system."""

from .sprites import get_sprite
from .curses_renderer import CursesGameRenderer

__all__ = ["get_sprite", "CursesGameRenderer"]

