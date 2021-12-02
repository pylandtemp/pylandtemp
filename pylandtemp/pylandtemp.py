from pylandtemp.emissivity import Emissivity, EMISSIVITY_METHODS

from pylandtemp.temperature import BrightnessTemperatureLandsat
from pylandtemp.temperature import LST
from pylandtemp.temperature import  SINGLE_WINDOW_METHODS, SPLIT_WINDOW_METHODS

from pylandtemp.general_utils import compute_ndvi




def split_window(
        landsat_band_10, 
        landsat_band_11, 
        landsat_band_4, 
        landsat_band_5, 
        lst_method, 
        emissivity_method,
        unit='kelvin'
    ):
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

    mask = landsat_band_10 == 0

    ndvi_image = ndvi(landsat_band_5, landsat_band_4, mask)

    brightness_temp_10, brightness_temp_11 = brightness_temperature(landsat_band_10, band_11=landsat_band_11, mask=mask)
    emissivity_10, emissivity_11 = Emissivity(ndvi_image, landsat_band_4)(emissivity_method)

    lst_fn = LST(method=lst_method)
    
    lst_image = lst_fn(
        emissivity_10, 
        brightness_temp_10, 
        emissivity_11=emissivity_11, 
        brightness_temperature_11 =brightness_temp_11, 
        mask = mask, 
        ndvi=ndvi_image,
        unit=unit
    )

    return lst_image

def single_window(
        landsat_band_10, 
        landsat_band_4, 
        landsat_band_5, 
        lst_method='mono-window', 
        emissivity_method='avdan',
        unit='kelvin'
    ):
    """Provides an interface to compute land surface temperature 
        from landsat 8 imagery using single window method

    Args:
        landsat_band_10 (np.ndarray): Band 10 of the Landsat 8 image
        landsat_band_4 (np.ndarray): Band 4 of the Landsat 8 image (Red band)
        landsat_band_5 (np.ndarray): Band 4 of the Landsat 8 image (Near-Infrared band)
        lst_method (str, optional): [description]. Defaults to 'mono-window'.
                                    Valid methods to add include:
                                    'mono-window': Avdan Ugur et al, 2016
        emissivity_method (str, optional): provide one of the valid split window method for computing land surface emissivity. 
                                            Defaults to 'avdan'.
                                         Valid methods to add include:
                                        'advan': Avdan Ugur et al, 2016
                                        'xiaolei':  Xiaolei Yu et al, 2014 
                                        'gopinadh': Gopinadh Rongali et al 2018
        unit (str, optional): 'celcius' or 'kelvin'. Defaults to 'kelvin'.

    Returns:
        np.ndarray: Land surface temperature (numpy array)
    """

    mask = landsat_band_10 == 0

    ndvi_image = ndvi(landsat_band_5, landsat_band_4, mask)

    brightness_temp_10, _ = brightness_temperature(landsat_band_10, mask=mask)
    emissivity_10, _ = Emissivity(ndvi_image, landsat_band_4)(emissivity_method)

    lst_fn = LST(method=lst_method)
    
    lst_image = lst_fn(
        emissivity_10, 
        brightness_temp_10, 
        mask = mask, 
        ndvi=ndvi_image,
        unit=unit
    )

    return lst_image 

def emissivity(ndvi_image, emissivity_method='avdan', landsat_band_4=None):
    """Provides an interface to compute land surface emissivity 
        from landsat 8 imagery 

    Args:
        ndvi_image (np.ndarray): Normalized difference vegetation index image
        emissivity_method (str, optional): provide one of the valid split window method for computing land surface emissivity. 
                                            Defaults to 'avdan'.
                                         Valid methods to add include:
                                        'advan': Avdan Ugur et al, 2016
                                        'xiaolei':  Xiaolei Yu et al, 2014 
        landsat_band_4 (None or np.ndarray, optional): red band image. Defaults to None.
                                                        Can be None except when emissivity_method = 'xiaolei'

    Returns:
        np.ndarray: Emissivity numpy array
    """

    if emissivity_method == 'xiaolei':
        assert landsat_band_4 is not None, ValueError(f'The red band has to be provided if {emissivity_method} is to be used')

    emissivity_10, emissivity_11 = Emissivity(ndvi_image, landsat_band_4)(emissivity_method)
    return emissivity_10, emissivity_11

def ndvi(landsat_band_5, landsat_band_4, mask):
    """[summary]

    Args:
        landsat_band_5 (np.ndarray): Band 5 of landsat 8 image
        landsat_band_4 (np.ndarray): Band 4 of landsat 8 image
        mask (np.ndarray[bool]): output is NaN where Mask == True

    Returns:
        np.ndarray: NVDI numpy array
    """
    return compute_ndvi(landsat_band_5, landsat_band_4, mask=mask)

def brightness_temperature(landsat_band_10, landsat_band_11=None, mask=None):
    """[summary]

    Args:
        landsat_band_10 (np.ndarray): Band 10 of landsat 8 image
        landsat_band_11 (np.ndarray): Band 11 of landsat 8 image. Defaults to None.
        mask (np.ndarray[bool]): output is NaN where Mask == True. Defaults to None.

    Returns:
        np.ndarray: Brightness temperature numpy array
    """
    brightness_temp_10, brightness_temp_11 = BrightnessTemperatureLandsat()(landsat_band_10, landsat_band_11,mask=mask)
    return brightness_temp_10, brightness_temp_11