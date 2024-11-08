def serialize_result(result):
    if type(result) in [str, int, float, type(None), bool]: return result

    # NOTE FIXME REMOVE WHEN FIXED IN TAPIPY
    # Catch an edgecase where tapipy returns the actual JSON response
    # object and not a TapisResult
    if type(result) == dict and result.get("message", None) != None:
        return result["message"]
    
    if type(result) == list:
        modified_result = []
        for res in result:
            modified_result.append(serialize_result(res))

        return modified_result
    
    modified_result = result.__dict__
    for prop in modified_result:
        modified_result[prop] = serialize_result(modified_result[prop])

    return modified_result