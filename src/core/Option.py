"""Defines the structure and available attributes for an Option."""

from enum import Enum
from typing import Dict, Any


class HandlerContext(Enum):
    """Handlers deal with each enum type in their own regard."""
    GENERIC = "generic"
    ARGS = "args"
    RESULT = "result"


class Option:
    """
    All of the possible option attributes are listed below,
    but Options don't need to use every attribute.
    """
    def __init__(self,
        name: str,
        aliases: list = [],
        usage: str = None,
        description: str = None,
        params: Dict[str, Dict[str, Any]] = {},
        handler: str = None,
        context: HandlerContext = "args",
        required: bool = False,
        require: list = [],
        exclude: list = [],
        precedes: list = [],
        follows: list = []
    ):
        self.name = name
        self.aliases = aliases
        self.description = description
        self.usage = usage
        self.params = params
        self.handler = handler
        self.context = context
        self.required = required
        self.require = require
        self.exclude = exclude
        self.precedes = precedes
        self.follows = follows
