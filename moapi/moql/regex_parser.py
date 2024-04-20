import re


def parse_regex(regex: str) -> str:
    """Convert regex to pattern to mongo db regex query

    Args:
        regex (str): Regex pattern in string format.

     Returns:
        Optional[string]: Regex as mongo db query
    """

    # flake8: noqa
    REGEX_VALUE_REGEX = r"\/(.+)\/(([a-z]))?"

    match: str = re.match(REGEX_VALUE_REGEX, regex)
    result = re.search(REGEX_VALUE_REGEX, regex)

    if match:
        regex = match.group(1)  # pattern
        options = (
            match.group(3) if match.group(3) else None
        )  # options, if included
        result = {"$regex": regex}
        if options:
            result["$options"] = options

        return result
