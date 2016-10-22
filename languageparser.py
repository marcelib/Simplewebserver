def parse_lang(accept_language):
    languages = accept_language.split(',')
    result = []
    for language in languages:
        values = language.split(';')
        lang_and_region = values[0].split('-')
        lang = lang_and_region[0]
        region = lang_and_region[1] if 1 < len(lang_and_region) else None
        quality_value = values[1].split('=')[1] if len(values) > 1 else 1.0

        result.append(dict(lang=lang,
                           quality=quality_value,
                           region=region))
    sorted(result, key=lambda x: x["quality"], reverse=True)
    return result
