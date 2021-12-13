TRANSFORMS = {
    "primitives": {
        "string": str,
        "integer": int,
        "float": float,
        "boolean": bool,
    },
    "non-primitives": {
        "array": list,
        "object": dict,
    }
}

def transform(oapi_schema_type, value):
    transforms = { **TRANSFORMS["primitives"], **TRANSFORMS["non-primitives"] }
    return transforms[oapi_schema_type](value)