"""
Outlines the various option attributes. Each option has both a single-character flag,
a verbose string (alias) flag, and a general description (description), but there are also
other attributes as well. See /src/core/Option.py for all available attributes.

Some examples of attributes and what they do are:

    - context: Determines what type a flag is. See /src/core/Option.py for all contexts.
    - handler: Determines which function in handlers.py will be used by the option.
    - params: Outlines what types of args should be used with the flag.
"""

from core.Option import Option
from core.OptionRegistrar import OptionRegistrar


option_registrar = OptionRegistrar()

option_registrar.register("core", [
    Option("-v",
        aliases=["-verbose"],
        description="show additional information for a command invocation",
        context="generic"
    ),
    Option("-h",
        aliases=["-help"],
        description="display help information for a command",
        context="generic",
        handler="help"
    )
])

option_registrar.register("TapipyController", [
    Option("-f",
        aliases=["-file, -contents"],
        description="converts the contents of a json file into position arguments",
        params={"filename": {type: str}},
        handler="fileContentsToPositionalArg"
    ),
    Option("-h",
        aliases=["-help"],
        description="displays help information for a command",
        context="generic",
        handler="help"
    ),
    Option("-j",
        aliases=["-json"],
        description="converts a json object from a file into keyword arguments",
        params={"filename": {type: str}},
        handler="jsonFileToKeywordArgs"
    ),
    Option("-q",
        aliases=["-quiet"],
        description="returns only an id if there is one",
        context="result",
        handler="quiet",
    ),
    Option("-r",
        aliases=["-raw"],
        description="prints a string representation of the result object",
        context="result",
        handler="tapisResultRawView"
    ),
    Option("-s",
        aliases=["-save"],
        description="saves results of a command invocation to a file",
        params={"filename": {type: str}},
        context="result",
        handler="resultToFile"
    ),
    Option("-t",
        aliases=["-table"],
        description="displays a table representation of the result if possible",
        context="result",
        handler="tapisResultTableView"
    ),
    Option("-v",
        aliases=["-verbose"],
        description="shows additional information for a command invocation",
        context="generic"
    )
])

option_registrar.uses("TapipyController", "core")
