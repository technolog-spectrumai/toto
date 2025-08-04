from django import template

register = template.Library()

@register.filter
def theme_class(theme, token_key_mode):
    """
    Looks up Tailwind class from Theme object.
    Usage: {{ theme|theme_class:'header:dark' }}
    """
    if not theme:
        return ""
    try:
        element, mode = token_key_mode.split(":")
        for token in theme:
            if token["element"] == element and token["mode"] == mode:
                return token["class"] + " " + element
    except Exception:
        pass

    return ""
