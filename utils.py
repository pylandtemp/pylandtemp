import numpy as np
from typing import Optional, List






def compute_brightness_temp(image: np.ndarray, M: float, A: float , k1: float, k2: float, unit: str='kelvin', mask: bool =True)-> np.ndarray:

    """Converts image raw digital numbers to brightness temperature
        Reference :  https://landsat.usgs.gov/using-usgs-landsat-8-product

    Args:
        image ([np.ndarray]): [Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data (e.g Band 10 landsat 8 data)]
        M (float): [Band-specific multiplicative rescaling factor from the image folder metadata (RADIANCE_MULT_BAND_x, where x is the band number).]
        A (float): [Band-specific additive rescaling factor from the image folder metadata (RADIANCE_ADD_BAND_x, where x is the band number).]
        k1 (float): [Band-specific thermal conversion constant from the image folder metadata (K1_CONSTANT_BAND_x, where x is the thermal band number)]
        k2 (float): [Band-specific thermal conversion constant from the image folder metadata (K2_CONSTANT_BAND_x, where x is the thermal band number]
        unit (str):  ['kelvin' or 'celcius']
        mask (bool): [A bitmap to mask out zero, NaN or cloudy pixels.  Must be same shape with image]

    Returns:
        [np.ndarray]: [Brightness temperature corrected image]
    """

    # if image.shape != mask.shape:
    #     raise ValueError("Image and mask should be of the same size")

    if unit not in ['kelvin', 'celcius']:
        raise ValueError("unit argument should be set to either 'kelvin' or 'celcius'")


    toa_radiance = np.empty(image.shape)
    brightness_temp = np.empty(image.shape)

    
    if mask:  #If mask is used
        mask_true = generate_mask(image)
        i,j = np.where(mask_true)
        toa_radiance[i,j] = (M * image[i,j]) + A
        brightness_temp[i,j] = k2 / (np.log((k1/toa_radiance[i,j]) + 1))

    else:
        toa_radiance = (M * image) + A
        brightness_temp = (k2 / (np.log((k1 / toa_radiance) + 1))) 
    
    if unit == 'celcius':
        brightness_temp = brightness_temp - 273.15
    return brightness_temp


def generate_mask(image)-> np.ndarray:
    """
    Return a bool array masking 0 and NaN values as False and others as True

    Args:
        image (np.ndarray): Single-band image
    """

    zero_mask = image != 0 #or image != np.nan
    nan_mask = image != np.nan
    mask_true = np.logical_and(zero_mask, nan_mask)

    return mask_true


def compute_ndvi(nir: np.ndarray, red: np.ndarray, eps=1e-15)-> np.ndarray:
    """Takes the near infrared and red bands of an optical satellite image as input and returns the ndvi: normalized difference vegetation index

    Args:
        nir (np.ndarray): [Near-infrared band image]
        red (np.ndarray): [Red band image]
        eps (float): Epsilon to avoid ZeroDivisionError in numpy

    Returns:
        np.ndarray: [Normalized difference vegetation index]
    """
    
    assert nir.shape == red.shape, f"Both images must be of the same dimaension, {nir.shape}, {red.shape}"
    
    ndvi = np.empty(nir.shape)
    ndvi = (nir - red) / (nir + red + eps)
    
    to_return = np.where(np.abs(ndvi)>1,np.nan, ndvi) 
    
    mask_nir = generate_mask(nir)
    mask_red = generate_mask(red)
    mask = np.logical_and(mask_nir, mask_red)
    i, j = np.where(~mask)
    to_return[i, j] = np.nan
    
    return to_return
