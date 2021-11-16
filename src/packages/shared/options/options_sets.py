"""
Outlines the various option attributes. Each option has both a single-character flag,
a verbose string (alias) flag, and a general description (usage), but there are also
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
        usage="show additional information for a command invocation",
        context="generic"
    ),
    Option("-h",
        aliases=["-help"],
        usage="display help information for a command",
        context="generic",
        handler="help"
    )
])

option_registrar.register("TapipyController", [
    Option("-f",
        aliases=["-file, -contents"],
        usage="a filename",
        params={"filename": {type: str}},
        handler="fileContentsToPositionalArg"
    ),
    Option("-h",
        aliases=["-help"],
        usage="display help information for a command",
        context="generic",
        handler="help"
    ),
    Option("-j",
        aliases=["-json"],
        usage="a json filename",
        params={"filename": {type: str}},
        handler="jsonFileToKeywordArgs"
    ),
    Option("-r",
        aliases=["-tapis-raw"],
        usage="",
        context="result",
        handler="tapisResultRawView"
    ),
    Option("-s",
        aliases=["-save"],
        usage="save results of a controller invocation to a file",
        params={"filename": {type: str}},
        context="result",
        handler="resultToFile"
    ),
    Option("-t",
        aliases=["-tapis-table"],
        usage="",
        context="result",
        handler="tapisResultTableView"
    ),
    Option("-v",
        aliases=["-verbose"],
        usage="show additional information for a command invocation",
        context="generic"
    )
])

option_registrar.uses("TapipyController", "core")
