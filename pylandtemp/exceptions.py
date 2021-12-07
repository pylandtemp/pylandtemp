import numpy as np


class InvalidMaskError(Exception):
    pass


class KeywordArgumentError(Exception):
    pass


class InputShapesNotEqual(Exception):
    pass


class InvalidMethodRequested(Exception):
    pass


def verify_keyword_arguments(keywords, **kwargs):
    """
    This method does three things:

    1.  Checks if all the required keyword arguments to complete a computation
        are provided in **kwargs

    2.  Checks to ensure all numpy arrays provided to all methods are of the same shape

    3.  Checks the mask variable provided to ensure it's indeed a mask with bool values


    Args:
        keywords ([list[str]], optional): Required keywords.
    """

    ensure_required_all_keywords_are_provided(keywords=keywords, **kwargs)
    ensure_images_are_same_shape(**kwargs)
    ensure_mask_is_bool(**kwargs)


def ensure_required_all_keywords_are_provided(keywords, **kwargs):
    """
    This method checks if all the required keyword arguments to complete a computation
        are provided in **kwargs

    Args:
        keywords ([list[str]], optional): Required keywords.

    Raises:
        KeywordArgumentError: custom exception
    """
    for keyword in keywords:
        if keyword not in kwargs:
            message = (
                f"Keyword argument {keyword} must be provided for this computation "
            )
            raise KeywordArgumentError(message)


def ensure_mask_is_bool(**kwargs):
    """
    This method checks the mask variable provided to ensure it's indeed a mask with bool values

    Raises:
        InvalidMaskError: custom exception
    """
    mask = kwargs[mask]
    if mask.dtype != "bool":
        message = (
            "Image passed in a 'mask' must be a numpy array with bool dtype values"
        )
        raise InvalidMaskError(message)


def ensure_images_are_same_shape(**kwargs):
    """Checks to ensure all numpy arrays provided to all methods are of the same shape

    Raises:
        InputShapesNotEqual: custom exception
    """

    base_shape = None
    for kwarg in kwargs:
        if isinstance(kwargs[kwarg], np.ndarray):
            variable_shape = kwargs[kwarg].shape
            if not base_shape:
                base_shape = variable_shape
            else:
                if base_shape != variable_shape:
                    message = f"Input images should be of same shape. {base_shape}, {variable_shape}"
                    raise InputShapesNotEqual(message)


def ensure_requested_method_valid(algo, algorithms):
    """
    This function checks that the requested algorithm in available in the package

    Args:
        algo (str): requested algorithm
        algorithms (dict): available algorithms with "key: implementation class" map

    Raises:
        InvalidMethodRequested: custom exception
    """

    if algo not in algorithms:
        message = "You can only request the following methods: {algorithms.keys()}"
        raise InvalidMethodRequested(message)
