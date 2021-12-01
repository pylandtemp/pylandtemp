import numpy as np
from emissivity.utils import EmissivityParent   
from general_utils import cavity_effect     


class ComputeMonoWindowEmissivity(EmissivityParent):
    
    def __init__(self, ndvi, red_band=None):
        super(ComputeMonoWindowEmissivity, self).__init__(ndvi, red_band)
        self.emissivity_soil_10 = 0.97 
        self.emissivity_veg_10 = 0.99
        self.emissivity_soil_11 = None
        self.emissivity_veg_11 = None
    def _compute_emissivity(self):

        emm = np.empty_like(self.ndvi)

        landcover_mask_indices = self._get_landcover_mask_indices()

        # Baresoil value assignment
        emm[landcover_mask_indices['baresoil']] = self.emissivity_soil_10

        # Vegetation value assignment
        emm[landcover_mask_indices['vegetation']] = self.emissivity_veg_10

        # Mixed value assignment
        emm[landcover_mask_indices['mixed']] = ((0.004 *
                                                (((self.ndvi[landcover_mask_indices['mixed']] - 
                                                0.2)/(0.5 - 0.2))**2)) +
                                                0.986
        )

        #self.emissivity[self.nan_mask] = np.nan

        return emm, emm

 
    

class ComputeEmissivityNBEM(EmissivityParent):


    def __init__(self, ndvi, red_band):
        """
        Method references:

        1. Li, Tianyu, and Qingmin Meng. "A mixture emissivity analysis method for 
            urban land surface temperature retrieval from Landsat 8 data." Landscape 
            and Urban Planning 179 (2018): 63-71.
        
        2. Yu, Xiaolei, Xulin Guo, and Zhaocong Wu. "Land surface temperature retrieval 
            from Landsat 8 TIRS—Comparison between radiative transfer equation-based method, 
            split window algorithm and single channel method." Remote sensing 6.10 (2014): 9829-9852.

        
        Args:
            ndvi (np.ndarray[float]): Normalized difference vegetation index (NDVI) image matrix
            red_band (np.ndarray[float]): Red band of image (0.63-0.69 micrometers)
        """
        super(ComputeEmissivityNBEM, self).__init__(ndvi, red_band)
        self.emissivity_soil_10 = 0.9668 
        self.emissivity_veg_10 = 0.9863
        self.emissivity_soil_11 = 0.9747 
        self.emissivity_veg_11 = 0.9896


    
    def _compute_emissivity(self):
        
        assert self.red_band is not None, \
            ValueError("Red band cannot be {} for this emissivity computation method".format(self.red_band))

        landcover_mask_indices = self._get_landcover_mask_indices()

        fractional_veg_cover = self._compute_fvc()

        def calc_emissivity_for_band(image, emissivity_veg, emissivity_soil, cavity_effect, red_band_coeff_a=None, red_band_coeff_b=None):
            image[landcover_mask_indices['baresoil']] = (red_band_coeff_a -
                                                        (red_band_coeff_b * self.red_band[landcover_mask_indices['baresoil']])

            )

            image[landcover_mask_indices['mixed']] = ((emissivity_veg * 
                                                        fractional_veg_cover[landcover_mask_indices['mixed']]) + 
                                                        (emissivity_soil *
                                                        (1 - fractional_veg_cover[landcover_mask_indices['mixed']])) +
                                                        cavity_effect[landcover_mask_indices['mixed']]
            )

            image[landcover_mask_indices['vegetation']] = (emissivity_veg + 
                                                            cavity_effect[landcover_mask_indices['vegetation']]
            )

            return image 
        
        
        emissivity_band_10 = np.empty_like(self.ndvi)
        emissivity_band_11 = np.empty_like(self.ndvi)
        frac_vegetation_cover = self._compute_fvc()

        cavity_effect_10 = cavity_effect(self.emissivity_veg_10, self.emissivity_soil_10, fractional_veg_cover)
        cavity_effect_11 = cavity_effect(self.emissivity_veg_11, self.emissivity_soil_11, fractional_veg_cover)

        emissivity_band_10 = calc_emissivity_for_band(
                                    emissivity_band_10, 
                                    self.emissivity_veg_10, 
                                    self.emissivity_soil_10, 
                                    cavity_effect_10,
                                    red_band_coeff_a=0.973,
                                    red_band_coeff_b=0.047
        )
        emissivity_band_11 = calc_emissivity_for_band(
                                emissivity_band_11, 
                                self.emissivity_veg_11, 
                                self.emissivity_soil_11, 
                                cavity_effect_11,
                                red_band_coeff_a=0.984,
                                red_band_coeff_b=0.026
        )

        return emissivity_band_10, emissivity_band_11
    
    

class ComputeEmissivityGopinadh(EmissivityParent):

    def __init__(self, ndvi, red_band=None):
        """
        Method reference:

        Rongali, Gopinadh, et al. "Split-window algorithm for retrieval of land surface temperature 
        using Landsat 8 thermal infrared data." Journal of Geovisualization and Spatial Analysis 2.2 
        (2018): 1-19.

        Args:
            ndvi (np.ndarray[float]): Normalized difference vegetation index (NDVI) image matrix
            red_band (np.ndarray[float]): Red band of image (0.63-0.69 micrometers). Defaults to None.
        """
        super(ComputeEmissivityGopinadh, self).__init__(ndvi, red_band)
        self.emissivity_soil_10 = 0.971
        self.emissivity_veg_10 = 0.987

        self.emissivity_soil_11 = 0.977
        self.emissivity_veg_11 = 0.989
    
    def _compute_emissivity(self):
    
        fractional_veg_cover = self._compute_fvc()

        def calc_emissivity_for_band(image, emissivity_veg, emissivity_soil, fractional_veg_cover):
            emm = ((emissivity_soil * 
                    (1 - fractional_veg_cover)) + 
                    (emissivity_veg * 
                    fractional_veg_cover))
            return emm 

        emissivity_band_10 = np.empty_like(self.ndvi)
        emissivity_band_10 = calc_emissivity_for_band(emissivity_band_10, self.emissivity_veg_10, self.emissivity_soil_10, fractional_veg_cover)

        emissivity_band_11 = np.empty_like(self.ndvi)
        emissivity_band_11 = calc_emissivity_for_band(emissivity_band_11, self.emissivity_veg_11, self.emissivity_soil_11, fractional_veg_cover)
        return  emissivity_band_10, emissivity_band_11 



