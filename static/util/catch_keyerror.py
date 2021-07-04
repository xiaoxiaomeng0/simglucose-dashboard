def catch_keyerror(form, key):
    try:
        result = form[key]
    except KeyError:
        result = None
    return result
