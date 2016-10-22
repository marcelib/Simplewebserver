def parse(accept_language):
    languages = accept_language.split(',')
    _return = []
    for language in languages:
        bits = language.split(';')
        ietf = bits[0].split('-')
        _return.append(dict(lang=ietf[0].strip(),
                            quality=float(bits[1].strip().split('=')[1]) if 1 < len(bits) else 1.0,
                            region=ietf[1].strip() if 1 < len(ietf) else None))
    sorted(_return, key=lambda x: x["quality"], reverse=True)
    return _return
