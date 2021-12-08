import numpy as np


__all__ = [
    "InvalidMaskError",
    "InputShapesNotEqual",
    "InvalidMethodRequested",
]


class InvalidMaskError(Exception):
    """Invalid mask error"""

    pass


class KeywordArgumentError(Exception):
    """Required keyword argument missing"""

    pass


class InputShapesNotEqual(Exception):
    """Input images don't have the same shape"""

    pass


class InvalidMethodRequested(Exception):
    """Invalid method/algorithm requested"""

    pass


def assert_required_keywords_provided(keywords, **kwargs):
    """
    This method checks if all the required keyword arguments to complete a computation
        are provided in **kwargs
    Args:
        keywords ([list[str]], optional): Required keywords.
    Raises:
        KeywordArgumentError: custom exception
    """
    for keyword in keywords:
        if keyword not in kwargs or kwargs[keyword] is None:
            message = (
                f"Keyword argument {keyword} must be provided for this computation "
            )
            raise KeywordArgumentError(message)
