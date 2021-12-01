import numpy as np
from emissivity.utils import EmissivityParent        


class ComputeMonoWindowEmissivity(EmissivityParent):
    
    def __init__(self, ndvi, red_band=None, mask=None):
        super(ComputeMonoWindowEmissivity, self).__init__(ndvi, red_band, mask)
        self.emissivity_soil = 0.97 
        self.emissivity_veg = 0.99

    def _compute_emissivity(self):

        
        landcover_mask_indices = self._get_landcover_mask_indices()

        # Baresoil value assignment
        self.emissivity[landcover_mask_indices['baresoil']] = self.emissivity_soil

        # Vegetation value assignment
        self.emissivity[landcover_mask_indices['vegetation']] = self.emissivity_veg

        # Mixed value assignment
        self.emissivity[landcover_mask_indices['mixed']] = ((0.004 *
                                                            (((self.ndvi[landcover_mask_indices['mixed']] - 
                                                            0.2)/(0.5 - 0.2))**2)) +
                                                            0.986
        )

        self.emissivity[self.nan_mask] = np.nan

        return self.emissivity

 
    

class ComputeEmissivityNBEM(EmissivityParent):


    def __init__(self, ndvi, red_band, mask=None):
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
        super(ComputeEmissivityNBEM, self).__init__(ndvi, red_band, mask)
        self.emissivity_soil = 0.9668 
        self.emissivity_veg = 0.9863


    
    def _compute_emissivity(self):
        
        assert self.red_band is not None, \
            ValueError("Red band cannot be {} for this emissivity computation method".format(self.red_band))

        landcover_mask_indices = self._get_landcover_mask_indices()

        fractional_veg_cover = self._compute_fvc()

        cavity_effect_10 = self._compute_cavity_effect()    

        self.emissivity[landcover_mask_indices['baresoil']] = (0.973 - 
                                                                (0.047 * 
                                                                self.red_band[landcover_mask_indices['baresoil']])
        )

        self.emissivity[landcover_mask_indices['mixed']] = ((self.emissivity_veg * 
                                                            fractional_veg_cover[landcover_mask_indices['mixed']]) + 
                                                            (self.emissivity_soil *
                                                            (1 - fractional_veg_cover[landcover_mask_indices['mixed']])) +
                                                            cavity_effect_10[landcover_mask_indices['mixed']]
        )

        self.emissivity[landcover_mask_indices['vegetation']] = (self.emissivity_veg + 
                                                                cavity_effect_10[landcover_mask_indices['vegetation']]
        )

        self.emissivity[self.nan_mask] = np.nan

        return self.emissivity
    
    
    

class ComputeEmissivityGopinadh(EmissivityParent):

    def __init__(self, ndvi, red_band=None, mask=None):
        """
        Method reference:

        Rongali, Gopinadh, et al. "Split-window algorithm for retrieval of land surface temperature 
        using Landsat 8 thermal infrared data." Journal of Geovisualization and Spatial Analysis 2.2 
        (2018): 1-19.

        Args:
            ndvi (np.ndarray[float]): Normalized difference vegetation index (NDVI) image matrix
            red_band (np.ndarray[float]): Red band of image (0.63-0.69 micrometers). Defaults to None.
        """
        super(ComputeEmissivityGopinadh, self).__init__(ndvi, red_band, mask)
        self.emissivity_soil = 0.9668
        self.emissivity_veg = 0.9747
    
    def _compute_emissivity(self):
    
        fractional_veg_cover = self._compute_fvc()

        self.emissivity = ((self.emissivity_soil * 
                            (1 - fractional_veg_cover)) + 
                            (self.emissivity_veg * 
                            fractional_veg_cover))

        self.emissivity[self.nan_mask] = np.nan

        return  self.emissivity



