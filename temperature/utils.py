import numpy as np

def compute_brightness_temperature(image: np.ndarray, 
                                    M: float, 
                                    A: float , 
                                    k1: float, 
                                    k2: float, 
                                    unit: str='kelvin', 
                                    mask: bool =True)-> np.ndarray:

    """Converts image raw digital numbers to brightness temperature
        Refer to USGS page https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product 
            for more details.

    Args:
        image (np.ndarray): Level 1 quantized and calibrated scaled Digital Numbers 
                                (DN) TIR band data (e.g Band 10 landsat 8 data)
        M (float): Band-specific multiplicative rescaling factor from the image 
                    folder metadata (RADIANCE_MULT_BAND_x, where x is the band number).
        A (float): Band-specific additive rescaling factor from the image 
                    folder metadata (RADIANCE_ADD_BAND_x, where x is the band number).
        k1 (float): Band-specific thermal conversion constant from the image 
                    folder metadata (K1_CONSTANT_BAND_x, where x is the thermal band number)
        k2 (float): Band-specific thermal conversion constant from the image 
                    folder metadata (K2_CONSTANT_BAND_x, where x is the thermal band number.
                    unit (str):  'kelvin' or 'celcius'
        unit (str): 'kelvin' or 'celcius', the unit of the temperature to be computed.  
        mask (bool): True if you want to mask NaN, O or irregular values from the computation

    Returns:
        np.ndarray: Brightness temperature corrected landsat image
    """

    if unit not in ['kelvin', 'celcius']:
        raise ValueError("unit argument should be set to either 'kelvin' or 'celcius'")


    toa_radiance = np.empty(image.shape)
    brightness_temp = np.empty(image.shape)

    
    if mask:  
        mask_true = generate_mask(image)
        #i,j = np.where(mask_true)
        toa_radiance[mask_true] = (M * image[mask_true]) + A
        brightness_temp[mask_true] = k2 / (np.log((k1/toa_radiance[mask_true]) + 1))

    else:
        toa_radiance = (M * image) + A
        brightness_temp = (k2 / (np.log((k1 / toa_radiance) + 1))) 
    
    if unit == 'celcius':
        brightness_temp = brightness_temp - 273.15
    return brightness_temp

def get_lst_compute_fn_input(
                            emissivity, 
                            brightness_temperature_10, 
                            brightness_temperature_11, 
                            column_water_vapour
                            ):
    to_return = dict()

    to_return['emissivity'] = emissivity
    to_return['brightness_temperature_10'] = brightness_temperature_10
    to_return['brightness_temperature_11'] = brightness_temperature_11
    to_return['column_water_vapour'] = column_water_vapour

    return to_return