from django import template

register = template.Library()

@register.filter
def split(value, delimiter=" "):
    """
    Splits the string into a list using the given delimiter.
    :param value: The string to split
    :param delimiter: The delimiter to use for splitting (default is space)
    :return: List of split values
    """
    if not isinstance(value, str):
        return value  # Return unchanged if not a string
    return value.split(delimiter)
