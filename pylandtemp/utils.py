import numpy as np


def generate_mask(image: np.ndarray) -> np.ndarray:
    """
    Return a bool array masking 0 and NaN values as False and others as True

    Args:
        image (np.ndarray): Single-band image which is True where we do not want to mask and False where we want to mask.
    """
    zero_mask = image != 0
    nan_mask = image != np.nan
    mask_true = np.logical_and(zero_mask, nan_mask)
    return mask_true


def compute_ndvi(
    nir: np.ndarray, red: np.ndarray, eps: float = 1e-15, mask=None
) -> np.ndarray:
    """Takes the near infrared and red bands of an optical satellite image as input and returns the ndvi: normalized difference vegetation index

    Args:
        nir (np.ndarray): Near-infrared band image
        red (np.ndarray): Red-band image
        eps (float): Epsilon to avoid ZeroDivisionError in numpy
        use_mask (bool): If True, mask NaN and 0 values in input images.

    Returns:
        np.ndarray: Normalized difference vegetation index
    """
    ndvi = (nir - red) / (nir + red + eps)
    ndvi[abs(ndvi) > 1] = np.nan
    if mask is not None:
        ndvi[mask] = np.nan
    return ndvi


def fractional_vegetation_cover(ndvi: np.ndarray) -> np.ndarray:
    """Computes the fractinal vegetation cover matrix

    Args:
        ndvi (np.ndarray):  Normalized difference vegetation index (m x n)
    Returns:
        np.ndarray: Fractional vegetation cover
    """
    if len(ndvi.shape) != 2:
        raise ValueError("NDVI image should be 2-dimensional")
    return ((ndvi - 0.2) / (0.5 - 0.2)) ** 2


def cavity_effect(
    emissivity_veg: float,
    emissivity_soil: float,
    fractional_vegetation_cover: np.ndarray,
    geometrical_factor: float = 0.55,
) -> np.ndarray:
    """Compute the cavity effect matrix

    Args:
        emissivity_veg (float): value of vegetation emissivity
        emissivity_soil (float): value of soil emissivity
        fractional_vegetation_cover (np.ndarray): Fractional vegetation cover image
        geometrical_factor (float, optional): Geometric factor. Defaults to 0.55.

    Returns:
        np.ndarray: Cavity effect numpy array
    """
    to_return = (
        (1 - emissivity_soil)
        * emissivity_veg
        * geometrical_factor
        * (1 - fractional_vegetation_cover)
    )
    return to_return


def rescale_band(
    image: np.ndarray, mult: float = 2e-05, add: float = 0.1
) -> np.ndarray:
    """rescales the image band

    Args:
        image (np.ndarray): Band 1 - 9, or non Thermal IR bands of the satellite image.
        mult (float, optional): Multiplicative factor. Defaults to 2e-05.
        add (float, optional): Additive factor. Defaults to 0.1.

    Returns:
        np.ndarray: rescaled image of same size as input
    """
    return (mult * image) + 0.1
