import numpy as np 


class Emissivity:

    def __init__(self, method:str):
        """[summary]

        Args:
            method (str): The computation method to use for obtaining the land surface emmisivity.
                            defaults to 'avdan' method

                            'avdan': 
        """
        assert method in ['avdan', 'xiaolei', 'gopinadh'], ValueError("Method not implemented")
        self.method = method


    def __call__(self, ndvi, red = None):
        if self.method == 'avdan':
            return mono_window_emmissivity(ndvi)
        elif self.method == 'xiaolei':
            assert red is not None, ValueError("'xiaolei' emmisivity method requires the red band input")

            return compute_LSE_NBEM(ndvi, red)
        else:
            return compute_LSE_using_fvc(ndvi)

def mono_window_emmissivity(ndvi: np.ndarray)->np.ndarray:
    """
    compute emmissivity from ndvi image 

    # Reference:

    Args:
        ndvi (np.ndarray): normalised difference vegetation index (cloud and water masked). Use getemp.compute_ndvi(...) to obtain 
        ndvi image that is masked 

    Returns:
        np.ndarray: Emissivity image
    """
    emissivity = np.empty(ndvi.shape)
    # Reference: Avdan, Ugur, and Gordana Jovanovska. "Algorithm for automated mapping of land surface temperature using LANDSAT 8 satellite data." Journal of Sensors 2016 (2016).
    nan_mask = np.isnan(ndvi)
    
    # Set values in emissivity matrix based on NDVI matrix value with same index
    mask1 = (ndvi >= -1) & (ndvi < 0.2)
    mask2 = (ndvi > 0.5) & (ndvi <= 1)
    mask3 = (ndvi >= 0.2) & (ndvi <= 0.5)
    

    i, j = np.where(mask1)
    emissivity[i, j] = 0.97
    i, j =np.where(mask2)
    emissivity[i, j] = 0.99
    i, j = np.where(mask3)
    emissivity[i, j] = (0.004*(((ndvi[i, j] - 0.2)/(0.5 - 0.2))**2)) + 0.986
    i, j = np.where(nan_mask)
    emissivity[i, j] = np.nan
    return emissivity


    
# Method 2 for LSE
def compute_LSE_NBEM(NDVI, red_band) :
    #Reference: https://www.sciencedirect.com/science/article/pii/S0169204618306480#b0240
    #reference : https://www.mdpi.com/2072-4292/6/10/9829 # Xiaolei Yu ,Xulin Guo andZhaocong Wu 
    #NDVI : NDVI image
    #Red_band: Red band of image (0.63-0.69 micrometers)

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