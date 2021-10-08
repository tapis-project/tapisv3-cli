from core.Option import Option
from core.OptionRegistrar import OptionRegistrar

option_registrar = OptionRegistrar()

option_registrar.register("core", [
    Option("-a",
        aliases=["-verbose"],
        usage="show additional information for a command invocation",
        context="generic"
    ),
    Option("-b",
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