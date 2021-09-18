import numpy as np 
from osgeo import gdal
from osgeo import osr
import math

#Contact: mudeledimeji@gmail.com

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


#STEP 4: COMPUTE LST WITH SPLIT WINDOW TECHNIQUE

#1st split-window method by Skokovic et al 2014
def compute_LST_splitWindow(t1, t2, e1, e2, cwv):
    #REFERENCE: Skokovic D, Sobrino JA, Jiménez Muñoz JC, SoriaG, Julien Y,Mattar C, Cristóbal J (2014)
    """
    t1 = TOA brightness temperature band 10
    t2 = TOA brightness temperature band 11
    e1 = Emissivity band 10
    e2 = Emissivity band 11
    cwv = Column water vapour
    """
    mean_e = (e1 + e2) / 2
    diff_e = np.subtract(e1, e2)

    assert t1.shape == t2.shape == e1.shape == e2.shape == cwv.shape, "Images should have the same size"

    lst = (t1 + (1.387 * (t1 - t2)) + (0.183 * ((t1 - t2)**2))
          - 0.268 + ((54.3 - (2.238 * cwv))* (1 - mean_e)) + ((-129.2 + (16.4 * cwv)) * diff_e))
    return lst

#2nd split window technique (Generalized split window with quadratic factor) by Du Chen et al 2015
def compute_LST_gsw_quad(t1, t2, e1, e2, cwv):
    #REFERENCE: Du, Chen, et al. "A practical split-window algorithm for estimating land surface temperature from Landsat 8 data." Remote Sensing 7.1 (2015): 647-665.
    """
    t1 = TOA brightness temperature band 10
    t2 = TOA brightness temperature band 11
    e1 = Emissivity band 10
    e2 = Emissivity band 11
    cwv = Column water vapour
    """
    lst = np.zeros(t1.shape)
    assert cwv.max() <= 8.0, "CWV should not have elements above 8.0"
    assert cwv.min() >= 0.0, "CWV should not have elements below 0"

    ave_emm = (e1 + e2) / 2
    change_emm = e1 - e2

    mask_cwv_range_1 = (cwv >= 0) & (cwv <= 2.0)
    mask_cwv_range_2 = (cwv > 2.0) & (cwv <= 3.0)
    mask_cwv_range_3 = (cwv > 3.0) & (cwv <= 4.0)
    mask_cwv_range_4 = (cwv > 4.0) & (cwv <= 5.0)
    mask_cwv_range_5 = (cwv > 5.0) & (cwv <= 6.8)

    a, b = np.where(mask_cwv_range_1)
    mean_tab = ((t1[a, b] + t2[a, b])/2)
    diff_tab = ((t1[a, b] - t2[a, b])/2)

    lst[a,b] = (-2.78009 + ((1.01408 + (0.15833*((1- ave_emm[a,b])/ave_emm[a,b]))
                     + (-0.34991 * (change_emm[a,b] / ((ave_emm[a,b])**2)))) * mean_tab)
               + ((4.04487 + (3.55414*((1- ave_emm[a,b])/ave_emm[a,b]))
                     + (-8.88394 * (change_emm[a,b] / (ave_emm[a,b]**2)))) * diff_tab)
                + (0.09152 * (diff_tab**2)))

    c,d = np.where(mask_cwv_range_2)
    mean_tcd = ((t1[c, d] + t2[c, d]) / 2)
    diff_tcd = ((t1[c, d] - t2[c, d]) / 2)

    lst[c, d] = (11.00824 + ((0.95995 + (0.17243 * ((1 - ave_emm[c, d]) / ave_emm[c, d]))
                        + (-0.28852 * (change_emm[c, d] / ((ave_emm[c, d]) ** 2)))) * mean_tcd )
                 + ((7.11492 + (0.42684 * ((1 - ave_emm[c, d]) / ave_emm[c, d]))
                     + (-6.62025 * (change_emm[c, d] / (ave_emm[c, d] ** 2)))) * diff_tcd )
                    + (-0.06381 * (diff_tcd **2 )))


    e,f = np.where(mask_cwv_range_3)
    mean_tef = ((t1[e, f] + t2[e, f]) / 2)
    diff_tef = ((t1[e, f] - t2[e, f]) / 2)
    lst[e, f] = (9.62610 + ((0.96202 + (0.13834 * ((1 - ave_emm[e, f]) / ave_emm[e, f]))
                        + (-0.17262 * (change_emm[e, f] / ((ave_emm[e, f]) ** 2)))) * mean_tef)
                 + ((7.87883 + (5.17910 * ((1 - ave_emm[e, f]) / ave_emm[e, f]))
                     + (-13.26611 * (change_emm[e, f] / (ave_emm[e, f] ** 2)))) * diff_tef )
                    + (-0.07603 *(diff_tef ** 2)))


    g,h = np.where(mask_cwv_range_4)
    mean_tgh = ((t1[g, h] + t2[g, h]) / 2)
    diff_tgh = ((t1[g, h] - t2[g, h]) / 2)
    lst[g,h] = (0.61258 + ((0.99124 + (0.10051 * ((1 - ave_emm[g, h]) / ave_emm[g, h]))
                        + (-0.09664 * (change_emm[g,h] / ((ave_emm[g,h]) ** 2)))) * mean_tgh)
                 + ((7.85758 + (6.86626 * ((1 - ave_emm[g,h]) / ave_emm[g,h]))
                     + (-15.00742 * (change_emm[g,h] / (ave_emm[g, h] ** 2)))) * diff_tgh )
                    + (-0.01185 * (diff_tgh ** 2)))

    i,j = np.where(mask_cwv_range_5)
    mean_tij = ((t1[i, j] + t2[i, j]) / 2)
    diff_tij = ((t1[i, j] - t2[i, j]) / 2)
    lst[i,j] = (-0.34808 + ((0.98123 + (0.05599 * ((1 - ave_emm[i,j]) / ave_emm[i,j]))
                        + (-0.03518 * (change_emm[i, j] / ((ave_emm[i,j]) ** 2)))) * mean_tij)
                 + ((11.96444 + (9.06710 * ((1 - ave_emm[i,j]) / ave_emm[i,j]))
                     + (-14.74085 * (change_emm[i, j] / (ave_emm[i,j] ** 2)))) * diff_tij)
                 + (-0.20471 * (diff_tij ** 2)))
    return lst


#STEP 5: Obtain geotiff image of land surface temperature

def array2raster(newRasterfn, dataset, array, dtype):
    """
    save GTiff file from numpy.array
    input:
        newRasterfn: name to save file with
        dataset : original tif file to obtain geo information. You should use the Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data (e.g Band 10 landsat 8 data)
        array : The Land surface temperature array
        dtype: Byte or Float32.
    """
    cols = array.shape[1]
    rows = array.shape[0]
    originX, pixelWidth, b, originY, d, pixelHeight = dataset.GetGeoTransform()

    driver = gdal.GetDriverByName('GTiff')

    # set data type to save.
    GDT_dtype = gdal.GDT_Unknown
    if dtype == "Byte":
        GDT_dtype = gdal.GDT_Byte
    elif dtype == "Float32":
        GDT_dtype = gdal.GDT_Float32
    else:
        print("Not supported data type.")

    # set number of band.
    if array.ndim == 2:
        band_num = 1
    else:
        band_num = array.shape[2]

    outRaster = driver.Create(newRasterfn, cols, rows, band_num, GDT_dtype)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

    # Loop over all bands.
    for b in range(band_num):
        outband = outRaster.GetRasterBand(b + 1)
        # Read in the band's data into the third dimension of our array
        if band_num == 1:
            outband.WriteArray(array)
        else:
            outband.WriteArray(array[:,:,b])

    # setteing srs from input tif file.
    prj=dataset.GetProjection()
    outRasterSRS = osr.SpatialReference(wkt=prj)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()