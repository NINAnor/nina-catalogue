def safe_get(element, attribute):
    if element:
        if (v := element.__getattribute__(attribute)) is not None:
            return v
    return ""
