#Import dependencies 
from osgeo import gdal
from osgeo import osr
import numpy as np
import math

#FISRT ACTION
#Convert Landsat data digital number to TA brightness temperature
#This follows procedures defined by NASA in the data documentation here: https://landsat.usgs.gov/using-usgs-landsat-8-product

def DN_to_BrightnessTemp(image, M , A , mask, k1, k2):
    # Reference :  https://landsat.usgs.gov/using-usgs-landsat-8-product
    # image = Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data (e.g Band 10 landsat 8 data)
    # M = Band-specific multiplicative rescaling factor from the metadata (RADIANCE_MULT_BAND_x, where x is the band number).
    # A = Band-specific additive rescaling factor from the metadata (RADIANCE_ADD_BAND_x, where x is the band number).
    # mask = bitmap to define bound computation.
    # Image = Input landsat Level-1 data product
    # k1 = Band-specific thermal conversion constant from the metadata (K1_CONSTANT_BAND_x, where x is the thermal band number)
    # k2 = Band-specific thermal conversion constant from the metadata (K2_CONSTANT_BAND_x, where x is the thermal band number
    
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

#SECOND ACTION
#Obtain Land surface Emissivity (LSE). There are multiple ways found in the literature defining how this can be done.
#This repo focuses on the NDVI based approaches. You only have to apply one of the functions defined below to obtain your LSE.

#Method 1 RECOMMENDED for mono-window technique)
def emmissivity_NDVI_treshold_TIR10(NDVI, mask):
    emissivity = np.zeros(NDVI.shape)
    # Reference:
    assert NDVI.shape == mask.shape,"Image and mask should be of the same size"
# Apply mask to Input image
# Extract indices of the zero elements in mask and set elements in input matrix with same indices into zero
    if mask != None:
        mask_zeros = mask == 0
        mask_ones = ~mask_zero


        # Set values in emissivity matrix based on NDVI matrix value with same index
        mask1 = mask_ones & (NDVI < 0.2)
        mask2 = mask_ones & (NDVI > 0.5)
        mask3 = mask_ones & (NDVI >= 0.2) & (NDVI <= 0.5)

        i, j = np.where(mask1)
        e[i, j] = 0.97
        k, l = np.where(mask2)
        e[k, l] = 0.99
        m, n = np.where(mask3)
        emissivity[m, n] = (0.004*(((NDVI[m, n] - 0.2)/(0.5 - 0.2))**2)) + 0.986
    else:


        # Set values in emissivity matrix based on NDVI matrix value with same index
        mask1 = NDVI < 0.2
        mask2 = NDVI > 0.5
        mask3 = (NDVI >= 0.2) & (NDVI <= 0.5)

        i, j = np.where(mask1)
        e[i, j] = 0.97
        k, l = np.where(mask2)
        e[k, l] = 0.99
        m, n = np.where(mask3)
        emissivity[m, n] = (0.004*(((NDVI[m, n] - 0.2)/(0.5 - 0.2))**2)) + 0.986

        return emissivity
    
# Method 2 
def compute_LSE_NBEM(NDVI, red_band) :
    #Reference: https://www.sciencedirect.com/science/article/pii/S0169204618306480#b0240
    #reference : https://www.mdpi.com/2072-4292/6/10/9829
    #NDVI : NDVI image

    assert NDVI.shape == red_band.shape , "Input images (NDVI and Red band) must be equal"
    
    emiss_matrix_10 = np.zeros(NDVI.shape) #Emissivity matrix for band 10 landsat 8 data (applies also to LST bands in other landsat data)


    # Assign different emissivity values to different NDVI ranges
    # 1st build a mask based on iNDVI values to assign emissivity values based on NDVI ranges

    # Define variables given in algorithm
    emissivity_soil_10 = 0.9668
    emissivity_veg_10 = 0.9863
  

    #p = FRACTIONAL VEGETATION COVER = (NDVI - NDVI_min) / (NDVI_max - NDVI_min)^2
    p = ((NDVI - 0.2)/(0.5 - 0.2))**2

    #Cavity effect = C (Defined in reference literature)
    c_10 = 0.018009838 *(1 - p) #For Band 10
  

    #Create mask to compute LSE based on NDVIO value ranges
    mask_ndvi_baresoil = (NDVI < 0.2) #Baresoil class is defined with NDVI less than 0.2
    mask_ndvi_veg = (NDVI > 0.5)      #veg pixels are defined with NDVI greater than 0.5
    mask_ndvi_mixed = (NDVI >= 0.2) & (NDVI <= 0.5)

    i, j = np.where(mask_ndvi_baresoil)
    emiss_matrix_10[i, j] = 0.973 - (0.047 * red_band[i, j])

    k, l = np.where(mask_ndvi_mixed)
    emiss_matrix_10[k, l] = (emissivity_veg_10 * p[k, l]) + (emissivity_soil_10 *(1 - p[k, l])) + c_10[k, l]

    m, n = np.where(mask_ndvi_veg)
    emiss_matrix_10[m, n] = emissivity_veg_10 + c_10[m, n]


    return emiss_matrix_10
