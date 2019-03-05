#Import dependencies 
from osgeo import gdal
from osgeo import osr
import numpy as np

#Apply code in this sequence
# FIRST ACTION --> SECOND ACTION --> THIRD ACTION --> FOURTH ACTION

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

#Method 1 (RECOMMENDED for mono-window technique)
def emmissivity_NDVI_treshold_TIR10(NDVI, mask):
    emissivity = np.zeros(NDVI.shape)
    # Reference:
    assert NDVI.shape == mask.shape,"Image and mask should be of the same size"
# Apply mask to Input image
# Extract indices of the zero elements in mask and set elements in input matrix with same indices into zero
    if mask != None:
        mask_zeros = mask == 0
        mask_ones = ~mask_zeros


        # Set values in emissivity matrix based on NDVI matrix value with same index
        mask1 = mask_ones & (NDVI < 0.2)
        mask2 = mask_ones & (NDVI > 0.5)
        mask3 = mask_ones & (NDVI >= 0.2) & (NDVI <= 0.5)

        i, j = np.where(mask1)
        emissivity[i, j] = 0.97
        k, l = np.where(mask2)
        emissivity[k, l] = 0.99
        m, n = np.where(mask3)
        emissivity[m, n] = (0.004*(((NDVI[m, n] - 0.2)/(0.5 - 0.2))**2)) + 0.986
    else:


        # Set values in emissivity matrix based on NDVI matrix value with same index
        mask1 = NDVI < 0.2
        mask2 = NDVI > 0.5
        mask3 = (NDVI >= 0.2) & (NDVI <= 0.5)

        i, j = np.where(mask1)
        emissivity[i, j] = 0.97
        k, l = np.where(mask2)
        emissivity[k, l] = 0.99
        m, n = np.where(mask3)
        emissivity[m, n] = (0.004*(((NDVI[m, n] - 0.2)/(0.5 - 0.2))**2)) + 0.986

        return emissivity
    
# Method 2 for LSE
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
    mask_ndvi_mixed = (NDVI >= 0.2) & (NDVI <= 0.5) #Mixed pixels are defined with NDVI less than or equal to 0.5 and Greater than of equal to 0.2

    i, j = np.where(mask_ndvi_baresoil)
    emiss_matrix_10[i, j] = 0.973 - (0.047 * red_band[i, j])

    k, l = np.where(mask_ndvi_mixed)
    emiss_matrix_10[k, l] = (emissivity_veg_10 * p[k, l]) + (emissivity_soil_10 *(1 - p[k, l])) + c_10[k, l]

    m, n = np.where(mask_ndvi_veg)
    emiss_matrix_10[m, n] = emissivity_veg_10 + c_10[m, n]


    return emiss_matrix_10

# Method 3 for LSE
def compute_LSE_using_fvc(NDVI):
    #FVC mean fractional vegetation cover. This method uses fractional vegetation cover to estimate LSE
    
    #Reference: Split window Algorithm for Retrieval of Land surface temperature using Landsat 8 Thermal infrared data
    #by Gopinadh Rongali et al (2018)

    # Assign different emissivity values to different NDVI ranges
    # 1st build a mask based on iNDVI values to assign emissivity values based on NDVI ranges



    # Define variables given in algorithm (See publication)
    emissivity_soil_10 = 0.9668
    emissivity_veg_10 = 0.9747
   

    # p = FRACTIONAL VEGETATION COVER = (NDVI - NDVI_min) / (NDVI_max - NDVI_min)^2
    p = ((NDVI - 0.2) / (0.5 - 0.2)) ** 2

    emiss_matrix_10 = (emissivity_soil_10 * (1 - p)) + (emissivity_veg_10 * p)
   
    return emiss_matrix_10

#3RD ACTION
#MAIN LST ALGORITHM (This function takes the TOA brightness temperature and emissivity images as imput to comput LST)
def compute_LST_mono_window(TB_band10, emissivity):
    #REFERENCE: 
    assert TB_band10.shape == emissivity.shape, "TOA Brightness Temperature and emissivity images must be of the same size"
    #Compute and Surface Temperature matrix
    land_surface_temp = TB_band10 / (1 + (((0.0000115 * TB_band10) / 14380) * np.log(emissivity)))
    return land_surface_temp


# FOURTH ACTION: Obtain geotiff image of landsurface temperature

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

