import numpy as np

from .temperature import default_algorithms as temperature_algorithms
from .emissivity import default_algorithms as emissivity_algorithms
from .temperature import BrightnessTemperatureLandsat
from .runner import Runner
from .utils import compute_ndvi
from .exceptions import *


def split_window(
    landsat_band_10: np.ndarray,
    landsat_band_11: np.ndarray,
    landsat_band_4: np.ndarray,
    landsat_band_5: np.ndarray,
    lst_method: str,
    emissivity_method: str,
    unit: str = "kelvin",
) -> np.ndarray:
    """Provides an interface to compute land surface temperature
        from landsat 8 imagery using split window method

    Args:
        landsat_band_10 (np.ndarray): Band 10 of the Landsat 8 image
        landsat_band_11 (np.ndarray): Band 11 of the landsat 8 image
        landsat_band_4 (np.ndarray): Band 4 of the landsat 8 image (Red band)
        landsat_band_5 (np.ndarray): Band 5 of the landsat 8 image (Near-Infrared band)

        lst_method (str): provide one of the valid split window method for computing land surface temperature
                        Valid methods to add include:
                        'jiminez-munoz': Jiminez-Munoz et al, 2008
                        'kerr': Kerr Y et al, 2004
                        'mc-millin': McMillin L. M. , 1975
                        'price': Price J. C., 1984
                        'sobrino-1993': Sobrino J. A. et al, 1993
                        'coll-caselles': Coll C. et al, 1997

        emissivity_method (str): provide one of the valid split window method for computing land surface emissivity.
                                         Valid methods to add include:
                                        'advan': Avdan Ugur et al, 2016
                                        'xiaolei':  Xiaolei Yu et al, 2014
                                        'gopinadh': Gopinadh Rongali et al 2018

        unit (str, optional): 'kelvin' or 'celcius'. Defaults to 'kelvin'.

    Returns:
        np.ndarray: Land surface temperature (numpy array)
    """

    if not (
        landsat_band_10.shape
        == landsat_band_11.shape
        == landsat_band_5.shape
        == landsat_band_4.shape
    ):
        raise InputShapesNotEqual(
            f"Shapes of input images should be equal: {landsat_band_10.shape}, {landsat_band_5.shape}, {landsat_band_4.shape}"
        )

    mask = landsat_band_10 == 0
    ndvi_image = ndvi(landsat_band_5, landsat_band_4, mask)

    brightness_temp_10, brightness_temp_11 = brightness_temperature(
        landsat_band_10, landsat_band_11=landsat_band_11, mask=mask
    )

    emissivity_10, emissivity_11 = Runner(algorithms=emissivity_algorithms)(
        emissivity_method, ndvi=ndvi_image, red_band=landsat_band_4
    )

    lst_image = Runner(algorithms=temperature_algorithms.split_window)(
        lst_method,
        emissivity_10=emissivity_10,
        emissivity_11=emissivity_11,
        brightness_temperature_10=brightness_temp_10,
        brightness_temperature_11=brightness_temp_11,
        mask=mask,
        ndvi=ndvi_image,
    )
    return lst_image


def single_window(
    landsat_band_10: np.ndarray,
    landsat_band_4: np.ndarray,
    landsat_band_5: np.ndarray,
    lst_method: str = "mono-window",
    emissivity_method: str = "avdan",
    unit: str = "kelvin",
) -> np.ndarray:
    """Provides an interface to compute land surface temperature
        from landsat 8 imagery using single window method

    Args:
        landsat_band_10 (np.ndarray): Band 10 of the Landsat 8 image
        landsat_band_4 (np.ndarray): Band 4 of the Landsat 8 image (Red band)
        landsat_band_5 (np.ndarray): Band 4 of the Landsat 8 image (Near-Infrared band)

        lst_method (str, optional): Defaults to 'mono-window'.
                                    Valid methods to add include:
                                    'mono-window': Avdan Ugur et al, 2016

        emissivity_method (str, optional): provide one of the valid split window method for computing
                                        land surface emissivity.

                                        Defaults to 'avdan'.
                                         Valid methods to add include:
                                        'advan': Avdan Ugur et al, 2016
                                        'xiaolei':  Xiaolei Yu et al, 2014
                                        'gopinadh': Gopinadh Rongali et al 2018

        unit (str, optional): 'celcius' or 'kelvin'. Defaults to 'kelvin'.

    Returns:
        np.ndarray: Land surface temperature (numpy array)
    """

    if not landsat_band_10.shape == landsat_band_5.shape == landsat_band_4.shape:
        raise InputShapesNotEqual(
            f"Shapes of input images should be equal: {landsat_band_10.shape}, {landsat_band_5.shape}, {landsat_band_4.shape}"
        )

    mask = landsat_band_10 == 0
    ndvi_image = ndvi(landsat_band_5, landsat_band_4, mask)
    brightness_temp_10, _ = brightness_temperature(landsat_band_10, mask=mask)

    emissivity_10, _ = Runner(algorithms=emissivity_algorithms)(
        emissivity_method, ndvi=ndvi_image, red_band=landsat_band_4
    )

    lst_image = Runner(algorithms=temperature_algorithms.single_window)(
        lst_method,
        emissivity_10=emissivity_10,
        brightness_temperature_10=brightness_temp_10,
        mask=mask,
        ndvi=ndvi_image,
    )
    return lst_image


def emissivity(
    ndvi_image: np.ndarray,
    landsat_band_4: np.ndarray = None,
    emissivity_method: str = "avdan",
):
    """Provides an interface to compute land surface emissivity
        from landsat 8 imagery

    Args:
        ndvi_image (np.ndarray): Normalized difference vegetation index image

        landsat_band_4 (None or np.ndarray, optional): red band image. Defaults to None.
                                                        Can be None except when emissivity_method = 'xiaolei'

        emissivity_method (str, optional): provide one of the valid split window method for computing land surface emissivity.
                                            Defaults to 'avdan'.
                                         Valid methods to add include:
                                        'advan': Avdan Ugur et al, 2016
                                        'xiaolei':  Xiaolei Yu et al, 2014

    Returns:
        np.ndarray: Emissivity numpy array
    """
    if not ndvi_image.shape == landsat_band_4.shape:
        raise InputShapesNotEqual(
            f"Shapes of input images should be equal: {ndvi_image.shape}, {landsat_band_4.shape}"
        )
    if emissivity_method == "xiaolei" and landsat_band_4 is None:
        raise ValueError(
            f"The red band (landsat_band_4) has to be provided if {emissivity_method} is to be used"
        )

    emissivity_10, emissivity_11 = Runner(algorithms=emissivity_algorithms)(
        emissivity_method, ndvi=ndvi_image, red_band=landsat_band_4
    )
    return emissivity_10, emissivity_11


def ndvi(landsat_band_5: np.ndarray, landsat_band_4: np.ndarray, mask: np.ndarray):
    """Computes the NDVI given bands 4 and 5 of Landsat 8 image

    Args:
        landsat_band_5 (np.ndarray): Band 5 of landsat 8 image
        landsat_band_4 (np.ndarray): Band 4 of landsat 8 image
        mask (np.ndarray[bool]): output is NaN where Mask == True

    Returns:
        np.ndarray: NVDI numpy array
    """
    if not landsat_band_5.shape == landsat_band_4.shape:
        raise InputShapesNotEqual(
            f"Shapes of input images should be equal: {landsat_band_5.shape}, {landsat_band_4.shape}"
        )

    if mask.dtype != "bool":
        raise InvalidMaskError(
            f"image passed in as 'mask' must be a numpy array with bool dtype values"
        )
    return compute_ndvi(landsat_band_5, landsat_band_4, mask=mask)


def brightness_temperature(
    landsat_band_10: np.ndarray,
    landsat_band_11: np.ndarray = None,
    mask: np.ndarray = None,
):
    """Compute brightness temperature

    Args:
        landsat_band_10 (np.ndarray): Band 10 of landsat 8 image
        landsat_band_11 (np.ndarray): Band 11 of landsat 8 image. Defaults to None.
        mask (np.ndarray[bool]): output is NaN where Mask == True. Defaults to None.

    Returns:
        np.ndarray: Brightness temperature numpy array
    """
    if (
        landsat_band_11 is not None
        and not landsat_band_10.shape == landsat_band_11.shape
    ):
        raise InputShapesNotEqual(
            f"Shapes of input images should be equal: {landsat_band_10.shape}, {landsat_band_11.shape}"
        )

    if mask.dtype != "bool":
        raise InvalidMaskError(
            f"image passed in as 'mask' must be a numpy array with bool dtype values"
        )

    brightness_temp_10, brightness_temp_11 = BrightnessTemperatureLandsat()(
        landsat_band_10, landsat_band_11, mask=mask
    )
    return brightness_temp_10, brightness_temp_11
