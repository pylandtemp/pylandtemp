import numpy as np
from typing import Optional, List



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

def rescale_band(image, mult=2e-05, add=0.1):
    """[summary]

    Args:
        image ([type]): Image, bands 1 - 9 landsat 8
        mult ([type]): Multiplicative factor
        add ([type]): additive factor
    """
    return (mult * image) + 0.1