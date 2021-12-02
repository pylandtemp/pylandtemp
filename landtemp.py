from emissivity import Emissivity, EMISSIVITY_METHODS

from temperature import BrightnessTemperatureLandsat
from temperature import LST
from temperature import  SINGLE_WINDOW_METHODS, SPLIT_WINDOW_METHODS

from general_utils import compute_ndvi




def split_window(
        landsat_band_10, 
        landsat_band_11, 
        landsat_band_4, 
        landsat_band_5, 
        lst_method, 
        emissivity_method,
        unit='kelvin'
    ):

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

def emissivity(ndvi_image, emissivity_method='avdan'):
    emissivity_10, emissivity_11 = Emissivity(ndvi_image, None)(emissivity_method)
    return emissivity_10, emissivity_11

def ndvi(nir, red, mask):
    return compute_ndvi(nir, red, mask=mask)

def brightness_temperature(band_10, band_11=None, mask=None):
    brightness_temp_10, brightness_temp_11 = BrightnessTemperatureLandsat()(band_10, band_11,mask=mask)
    return brightness_temp_10, brightness_temp_11