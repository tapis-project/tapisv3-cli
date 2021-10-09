"""Handles abstract class method inheritance in the CLI."""

from abc import ABC, abstractclassmethod


class AbstractView(ABC):
    """All abstract class methods will go here."""
    @abstractclassmethod
    def __init__(self, data):
        pass

    @abstractclassmethod
    def render(self):
        """Rendering code to go here."""
        pass
