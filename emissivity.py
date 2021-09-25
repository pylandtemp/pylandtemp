import numpy as np 


# class Emissivity_:

#     def __init__(self, method:str):
#         """[summary]

#         Args:
#             method (str): The computation method to use for obtaining the land surface emmisivity.
#                             defaults to 'avdan' method

#                             'avdan': 
#         """
#         assert method in ['avdan', 'xiaolei', 'gopinadh'], ValueError("Method not implemented")
#         self.method = method


#     def __call__(self, ndvi, red = None):
#         if self.method == 'avdan':
#             return mono_window_emmissivity(ndvi)
#         elif self.method == 'xiaolei':
#             assert red is not None, ValueError("'xiaolei' emmisivity method requires the red band input")

#             return compute_LSE_NBEM(ndvi, red)
#         else:
#             return compute_LSE_using_fvc(ndvi)


class ComputeEmissivity:

    def __init__(self, ndvi, red_band=None):
        self.ndvi = ndvi
        self.red_band = red_band
    
    def __call__(self, method):
        assert method in ['avdan', 'xiaolei', 'gopinadh'], ValueError("Method not implemented")
        compute_method = self.get_method(method)

        return compute_method(self.ndvi, self.red_band)()


    def get_method(self, method):

        if method == 'avdan':
            return MonoWindowEmissivity
        elif method == 'xiaolei':
            return ComputeEmissivityNBEM
        elif method == 'gopinadh':
            return ComputeEmissivityFVC
        else:
            raise NotImplementedError("Requested method not implemented. Choose between ['avdan', 'xiaolei', 'gopinadh']")

        


class Emissivity:
    def __init__(self, ndvi, red_band):
        """[summary]

        Args:
            ndvi (np.ndarray[float]): Normalized difference vegetation index in matrix form

        """
        assert len(ndvi.shape) == 2, ValueError("Input must be single band image with two dimensions only. {}".format(ndvi.shape))
        self.ndvi = ndvi #nvdi image
        self.red_band = red_band
        self.emissivity = np.zeros_like(ndvi) 
        self.nan_mask = np.isnan(ndvi) # mask for nan values 

       

    def __call__(self):

        if self.red_band is not None:
            assert self.ndvi.shape == self.red_band.shape , ValueError("Input images (NDVI and Red band) must be of equal dimension")

        emm = self._compute_emissivity()

        emm[self.nan_mask] = np.nan

        return emm
        
        
    def _get_land_surface_mask(self):
        
        mask_baresoil = (self.ndvi >= -1) & (self.ndvi < 0.2)
        mask_vegetation = (self.ndvi > 0.5) & (self.ndvi <= 1)
        mask_mixed = (self.ndvi >= 0.2) & (self.ndvi <= 0.5)

        return {
                'baresoil': mask_baresoil, 
                'vegetation': mask_vegetation, 
                'mixed': mask_mixed
                }

    def _compute_emissivity(self):
        raise NotImplementedError("No emissivity computation logic implemented yet")

    

    #def _compute_fvc(self):
    #    raise NotImplementedError("Fractional vegetation cover computation not implemented yet, or not applied")
        


class MonoWindowEmissivity(Emissivity):
    
    def _compute_emissivity(self):

        

        masks = self._get_land_surface_mask()

        # Baresoil value assignment
        i, j = np.where(masks['baresoil'])
        self.emissivity[i, j] = 0.97

        # Vegetation value assignment
        i, j =np.where(masks['vegetation'])
        self.emissivity[i, j] = 0.99

        # Mixed value assignment
        i, j = np.where(masks['mixed'])
        self.emissivity[i, j] = (0.004*(((self.ndvi[i, j] - 0.2)/(0.5 - 0.2))**2)) + 0.986

        i, j = np.where(self.nan_mask)
        self.emissivity[i, j] = np.nan
        return self.emissivity
    

class ComputeEmissivityNBEM(Emissivity):

    def __init__(self, ndvi, red_band):
        super(ComputeEmissivityNBEM, self).__init__(ndvi, red_band)
        self.emissivity_soil_10 = 0.9668 
        self.emissivity_veg_10 = 0.9863


    
    def _compute_emissivity(self):
        
        #Reference: https://www.sciencedirect.com/science/article/pii/S0169204618306480#b0240
        #reference : https://www.mdpi.com/2072-4292/6/10/9829 # Xiaolei Yu ,Xulin Guo andZhaocong Wu 
        #NDVI : NDVI image
        #Red_band: Red band of image (0.63-0.69 micrometers)

        
        assert self.red_band is not None, ValueError("Red band cannot be {} for this emissivity computation method".format(self.red_band))

        masks = self._get_land_surface_mask()

        # define constants

        #p = FRACTIONAL VEGETATION COVER = (NDVI - NDVI_min) / (NDVI_max - NDVI_min)^2
        p = self._compute_fvc()

        #Cavity effect = C (Defined in reference literature)
        c_10 = self.compute_cavity_effect(p)    

        #Create mask to compute LSE based on NDVIO value ranges
        #mask_ndvi_baresoil = (self.ndvi < 0.2) #Baresoil class is defined with NDVI less than 0.2
        #mask_ndvi_veg = (self.ndvi > 0.5)      #veg pixels are defined with NDVI greater than 0.5
        #mask_ndvi_mixed = (self.ndvi >= 0.2) & (NDVI <= 0.5) #Mixed pixels are defined with NDVI less than or equal to 0.5 and Greater than of equal to 0.2

        i, j = np.where(masks['baresoil'])
        self.emissivity[i, j] = 0.973 - (0.047 * self.red_band[i, j])

        k, l = np.where(masks['mixed'])
        self.emissivity[k, l] = (self.emissivity_veg_10 * p[k, l]) + (self.emissivity_soil_10 *(1 - p[k, l])) + c_10[k, l]

        m, n = np.where(masks['vegetation'])
        self.emissivity[m, n] = self.emissivity_veg_10 + c_10[m, n]

        return self.emissivity

    def _compute_fvc(self):
        """This function computes the fractional vegetation cover

        Returns:
            [np.ndarray]: [fractional vegetaion cover matrix
        """
        return ((self.ndvi - 0.2)/(0.5 - 0.2))**2

    def compute_cavity_effect(self, frac_vegetation_cover):
        """Computes cavity effect from fractional vegetation cover matrix

        Args:
            frac_vegetation_cover (np.ndarray): Fractional vegetation cover matrix

        Returns:
            np.ndarray: Cavity effect matric
        """
        return  0.018009838 *(1 - frac_vegetation_cover)
    
    
    

class ComputeEmissivityFVC(Emissivity):

    def __init__(self, ndvi, red_band):
        super(ComputeEmissivityFVC, self).__init__(ndvi, red_band)
        #super(compute_LSE_using_fvc, self).__init__()
        self.emissivity_soil_10 = 0.9668
        self.emissivity_veg_10 = 0.9747
    
    def _compute_emissivity(self):
        #FVC mean fractional vegetation cover. This method uses fractional vegetation cover to estimate LSE
    
        #Reference: Split window Algorithm for Retrieval of Land surface temperature using Landsat 8 Thermal infrared data
        #by Gopinadh Rongali et al (2018)

        # Assign different emissivity values to different NDVI ranges
        # 1st build a mask based on iNDVI values to assign emissivity values based on NDVI ranges



        # Define variables given in algorithm (See publication)
        
    

        # p = FRACTIONAL VEGETATION COVER = (NDVI - NDVI_min) / (NDVI_max - NDVI_min)^2
        p = self._compute_fvc()
        #p = ((NDVI - 0.2) / (0.5 - 0.2)) ** 2

        self.emissivity = (self.emissivity_soil_10 * (1 - p)) + (self.emissivity_veg_10 * p)
    
        return  self.emissivity

    def _compute_fvc(self):
        """This function computes the fractional vegetation cover

        Returns:
            [np.ndarray]: [fractional vegetaion cover matrix
        """
        return ((self.ndvi - 0.2)/(0.5 - 0.2))**2



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

    assert NDVI.shape == red_band.shape , ValueError("Input images (NDVI and Red band) must be of equal dimension")
    
    emiss_matrix_10 = np.zeros(NDVI.shape) #Emissivity matrix for band 10 landsat 8 data (applies also to LST bands in other landsat data)


    # Assign different emissivity values to different NDVI ranges
    # 1st build a mask based on iNDVI values to assign emissivity values based on NDVI ranges

    # Define variables given in algorithm
    emissivity_soil_10 = 0.9668 # Baresoil emissivity value
    emissivity_veg_10 = 0.9863 # Vegetation emmisivity value
  

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