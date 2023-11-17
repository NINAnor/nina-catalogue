def safe_get(element, attribute):
    if element:
        if (v := element.__getattribute__(attribute)) is not None:
            return v
    return ""


def req_to_base(request):
    return request.scheme + "://" + request.get_host()
