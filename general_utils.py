import numpy as np
from typing import Optional, List
#
#def compute_brightness_temp(image: np.ndarray, 
#                            M: float, 
#                            A: float , 
#                            k1: float, 
#                            k2: float, 
#                            unit: str='kelvin', 
#                            mask: bool =True)-> np.ndarray:
#
#    """Converts image raw digital numbers to brightness temperature
#        Refer to USGS page https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product 
#            for more details.
#
#    Args:
#        image (np.ndarray): Level 1 quantized and calibrated scaled Digital Numbers 
#                                (DN) TIR band data (e.g Band 10 landsat 8 data)
#        M (float): Band-specific multiplicative rescaling factor from the image 
#                    folder metadata (RADIANCE_MULT_BAND_x, where x is the band number).
#        A (float): Band-specific additive rescaling factor from the image 
#                    folder metadata (RADIANCE_ADD_BAND_x, where x is the band number).
#        k1 (float): Band-specific thermal conversion constant from the image 
#                    folder metadata (K1_CONSTANT_BAND_x, where x is the thermal band number)
#        k2 (float): Band-specific thermal conversion constant from the image 
#                    folder metadata (K2_CONSTANT_BAND_x, where x is the thermal band number.
#                    unit (str):  'kelvin' or 'celcius'
#        unit (str): 'kelvin' or 'celcius', the unit of the temperature to be computed.  \
#        mask (bool): True if you want to mask NaN, O or irregular values from the computation
#
#    Returns:
#        np.ndarray: Brightness temperature corrected landsat image
#    """
#
#    if unit not in ['kelvin', 'celcius']:
#        raise ValueError("unit argument should be set to either 'kelvin' or 'celcius'")
#
#
#    toa_radiance = np.empty(image.shape)
#    brightness_temp = np.empty(image.shape)
#
#    
#    if mask:  
#        mask_true = generate_mask(image)
#        #i,j = np.where(mask_true)
#        toa_radiance[mask_true] = (M * image[mask_true]) + A
#        brightness_temp[mask_true] = k2 / (np.log((k1/toa_radiance[mask_true]) + 1))
#
#    else:
#        toa_radiance = (M * image) + A
#        brightness_temp = (k2 / (np.log((k1 / toa_radiance) + 1))) 
#    
#    if unit == 'celcius':
#        brightness_temp = brightness_temp - 273.15
#    return brightness_temp
#""" 


def generate_mask(image)-> np.ndarray:
    """
    Return a bool array masking 0 and NaN values as False and others as True

    Args:
        image (np.ndarray): Single-band image which is True where we do not want to mask and False where we want to mask
    """

    zero_mask = image != 0 #or image != np.nan
    nan_mask = image != np.nan
    mask_true = np.logical_and(zero_mask, nan_mask)

    return mask_true


def compute_ndvi(nir: np.ndarray, 
                red: np.ndarray, 
                eps=1e-15,
                mask= None)-> np.ndarray:
    """Takes the near infrared and red bands of an optical satellite image as input and returns the ndvi: normalized difference vegetation index

    Args:
        nir (np.ndarray): Near-infrared band image
        red (np.ndarray): Red-band image
        eps (float): Epsilon to avoid ZeroDivisionError in numpy
        use_mask (bool): If True, mask NaN and 0 values in input images. 

    Returns:
        np.ndarray: Normalized difference vegetation index
    """
    
    assert nir.shape == red.shape, f"Both images must be of the same dimension, {nir.shape}, {red.shape}"
    
    #ndvi = np.empty(nir.shape)
    ndvi = (nir - red) / (nir + red + eps)
    
    ndvi[abs(ndvi) > 1] = np.nan
    
    #if use_mask:
    #    mask_nir = generate_mask(nir)
    #    mask_red = generate_mask(red)
    #    mask = np.logical_and(mask_nir, mask_red)
    #    i, j = np.where(~mask)
    #    to_return[i, j] = np.nan
    if mask is not None:
        ndvi[mask] = np.nan 
        
    return ndvi

def fractional_vegetation_cover(ndvi):
    """[summary]

    Args:
        ndvi (np.ndarray):  Normalized difference vegetation index (m x n)
    Returns:
        np.ndarray: Fractional vegetation cover 
    """
    assert len(ndvi.shape) == 2, "NDVI image should be 2-dimensional"

    return ((ndvi - 0.2)/(0.5 - 0.2))**2



def cavity_effect(
            emissivity_veg, 
            emissivity_soil, 
            fractional_vegetation_cover, 
            geometrical_factor=0.55
    ):

    """Computes cavity effect from fractional vegetation cover matrix

    Args:
        frac_vegetation_cover (np.ndarray): Fractional vegetation cover matrix

    Returns:
        np.ndarray: Cavity effect matric
    """
    #fractional_veg_cover = fractional_vegetation_cover()
    to_return = (
        (1 - emissivity_soil) * 
        emissivity_veg * geometrical_factor * 
        (1 - fractional_vegetation_cover)
    )

    return to_return 