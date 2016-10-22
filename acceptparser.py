def parse_accept(header):
    types = header.split(',')
    result = []
    for accept_type in types:
        values = accept_type.split(';')
        accepted_type = values[0]
        quality_value = values[1].split('=')[1] if len(values) > 1 else 1.0

        result.append(dict(accept=accepted_type,
                           quality=quality_value))
    sorted(result, key=lambda x: x["quality"], reverse=True)
    return result
