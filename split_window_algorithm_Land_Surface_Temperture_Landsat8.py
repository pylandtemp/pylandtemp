import numpy as np 
from osgeo import gdal
from osgeo import osr
import math

#STEP 1: Convert landsat 8 bands 10 and 11 (Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data) to TOA brightness temperature
def DN_to_BrightnessTemp(image, M , A , mask, k1, k2):
    # Reference :  https://landsat.usgs.gov/using-usgs-landsat-8-product
    # image = Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data (e.g Band 10 landsat 8 data)
    # M = Band-specific multiplicative rescaling factor from the image folder metadata (RADIANCE_MULT_BAND_x, where x is the band number).
    # A = Band-specific additive rescaling factor from the image folder metadata (RADIANCE_ADD_BAND_x, where x is the band number).
    # mask = bitmap to define bound computation.
    # Image = Input landsat Level-1 data product
    # k1 = Band-specific thermal conversion constant from the image folder metadata (K1_CONSTANT_BAND_x, where x is the thermal band number)
    # k2 = Band-specific thermal conversion constant from the image folder metadata (K2_CONSTANT_BAND_x, where x is the thermal band number
    # Apply function to TIRS bands 10 and 11 individually using constands as specified in image folder metadata
    assert image.shape == mask.shape , "Image and mask should be of the same size"

    TOA_radiance = np.zeros(image.shape)
    brightness_temp = np.zeros(image.shape)
 
    
    if mask != 'None':  #If mask is used
        mask_true = mask == 1
        i,j = np.where(mask_true)
        TOA_radiance[i,j] = (M * image[i,j]) + A
        brightness_temp[i,j] = k2 / (np.log((k1/TOA_radiance[i,j]) + 1))

    else:
        TOA_radiance = (M * image) + A
        # The minus 273.15 below is so as to obtain the result in degree celcius
        brightness_temp = (k2 / (np.log((k1 / TOA_radiance) + 1))) - 273.15
    return brightness_temp

#STEP 2: Derive column water vapour 
"""
Split window techiniques require the atmospheric column water vapour (CWV) value.
The Modified  split-window covariance and variance ratio (MSWCVR) method was developed to retrieve CWV from the TIRS data.

REFERENCE: 
Du, Chen, et al. "A practical split-window algorithm for estimating land surface temperature from Landsat 8 data." Remote Sensing 7.1 (2015): 647-665.

The functions below are used to derive the CWV
"""

def compute_cwv(TB_band1, TB_band2, window_size):
    """
    TB_band1: Band 10 TOA brightness temperature on obtained from the function is STEP 1 
    TB_band2: Band 11 TOA brightness temperature on obtained from the function is STEP 1
    window_size: Size of kernel in computing transmittance ratio. (See reference publication)
    """
    assert (window_size % 2) == 1, "Window size should be a odd number"
    trans_mat_output = np.zeros(TB_band1.shape) #Transmitance ratio
    padding_pixels = math.floor(window_size / 2)
    TB_band1_pad = np.pad(TB_band1, padding_pixels, 'reflect')
    TB_band2_pad = np.pad(TB_band2, padding_pixels, 'reflect')
    for i in range(0, TB_band1_pad.shape[0] - window_size + 1):
        for j in range(0, TB_band2_pad.shape[1] - window_size + 1):
            window_TB_band1 = TB_band1_pad[i:i + window_size, j:j + window_size]
            window_TB_band2 = TB_band2_pad[i:i + window_size, j:j + window_size]
            numerator = np.sum(np.multiply((window_TB_band1 - (np.median(window_TB_band1))),
                                           (window_TB_band2 - (np.median(window_TB_band2)))))
            # print(window_TB_band1, window_TB_band2)
            denominator = np.sum((window_TB_band1 - np.median(window_TB_band1)) ** 2)
            # print(numerator)
            trans_mat_output[i, j] = numerator / denominator
   
    C0 = 9.087
    C1 = 0.653
    C2 = -9.674
    cwv_matrix = C0 + (C1 * trans_mat_output) + (C2 * (trans_mat_output ** 2))
    return cwv_matrix
    
    
#STEP 3: Derive land surface emissivity (LSE) 
#There are multiple ways found in the literature defining how this can be done.
#This repo focuses on the NDVI based approaches. 
#You only have to apply one of the functions defined below to obtain your LSE.

#1st Mthod for LSE
def compute_LSE_NBEM(NDVI, red_band ):
    # Reference: https://www.sciencedirect.com/science/article/pii/S0169204618306480#b0240
    #REFERENCE : https://www.mdpi.com/2072-4292/6/10/9829
      #NDVI : NDVI image
    #Red_band: Red band of image (0.63-0.69 micrometers)
    
    assert NDVI.shape == red_band.shape , "Input images must be equal"
    emiss_matrix_10 = np.zeros(NDVI.shape)
    emiss_matrix_11 = np.zeros(NDVI.shape)
  
    # Assign different emissivity values to different NDVI ranges
    # 1st build a mask based on iNDVI values to assign emissivity values based on NDVI ranges

    # Define variables given in algorithm
    emissivity_soil_10 = 0.9668
    emissivity_soil_11 = 0.9747
    emissivity_veg_10 = 0.9863
    emissivity_veg_11 = 0.9896

    #p = FRACTIONAL VEGETATION COVER = (NDVI - NDVI_min) / (NDVI_max - NDVI_min)^2
    # NDVI_min = 0.2 AND ndvi_max = 0.5 (Mixed pixels)
    p = ((NDVI - 0.2)/(0.5 - 0.2))**2

    #Cavity effect = C
    c_10 = 0.018009838 *(1 - p)
    c_11 = 0.013770284 *(1 - p)

    mask_ndvi_baresoil = (NDVI < 0.2)
    mask_ndvi_mixed = (NDVI > 0.5)
    mask_ndvi_veg = (NDVI >= 0.2) & (NDVI <= 0.5)

    i, j = np.where(mask_ndvi_baresoil)
    emiss_matrix_10[i, j] = 0.973 - (0.047 * red_band[i, j])
    emiss_matrix_11[i, j] = 0.984 - (0.026 * red_band[i, j])

    k, l = np.where(mask_ndvi_mixed)
    emiss_matrix_10[k, l] = (emissivity_veg_10 * p[k, l]) + (emissivity_soil_10 *(1 - p[k, l])) + c_10[k, l]
    emiss_matrix_11[k, l] = (emissivity_veg_11 * p[k, l]) + (emissivity_soil_11 *(1 - p[k, l])) + c_11[k, l]


    m, n = np.where(mask_ndvi_veg)
    emiss_matrix_10[m, n] = emissivity_veg_10 + c_10[m, n]
    emiss_matrix_11[m, n] = emissivity_veg_10 + c_11[m, n]

    return emiss_matrix_10, emiss_matrix_11 #Returns a tuple: 1st element for band 10, 2nd for band 11

def compute_LSE_using_fvc(NDVI):

    #Reference: Split window Algorithm for Retrieval of Land surface temperature using Landsat 8 Thermal infrared data
    #by Gopinadh Rongali et al (2018)

    # Assign different emissivity values to different NDVI ranges
    # 1st build a mask based on iNDVI values to assign emissivity values based on NDVI ranges



    # Define variables given in algorithm
    emissivity_soil_10 = 0.9668
    emissivity_soil_11 = 0.9863
    emissivity_veg_10 = 0.9747
    emissivity_veg_11 = 0.9896

    # p = FRACTIONAL VEGETATION COVER = (NDVI - NDVI_min) / (NDVI_max - NDVI_min)^2
    p = ((NDVI - 0.2) / (0.5 - 0.2)) ** 2

    emiss_matrix_10 = (emissivity_soil_10 * (1 - p)) + (emissivity_veg_10 * p)
    emiss_matrix_11 = (emissivity_soil_11 * (1 - p)) + (emissivity_veg_11 * p)
    return emiss_matrix_10, emiss_matrix_11