import numpy as np

class EmissivityParent:
    def __init__(self, ndvi, red_band):
        """ Parent class for all emissivity methods. Contains general methods and attributes

        Args:
            ndvi (np.ndarray[float]): Normalized difference vegetation index in matrix form

        """
        assert len(ndvi.shape) == 2, ValueError("Input must be single band image with two dimensions only. {}".format(ndvi.shape))
        self.ndvi = ndvi #nvdi image
        self.red_band = red_band
        
        self.emissivity = np.zeros_like(ndvi) 
        self.nan_mask = np.isnan(ndvi) # mask for nan values 

        self.ndvi_min = -1
        self.ndvi_max = 1
        self.baresoil_ndvi_max = 0.2
        self.vegatation_ndvi_min = 0.5

    def __call__(self):

        if self.red_band is not None:
            assert self.ndvi.shape == self.red_band.shape , ValueError("Input images (NDVI and Red band) must be of equal dimension")

        emm = self._compute_emissivity()

        emm[self.nan_mask] = np.nan

        return emm
        

    def _compute_emissivity(self):
        raise NotImplementedError("No concrete implementation of emissivity method yet")
    

    def _compute_cavity_effect(self):
        """Computes cavity effect from fractional vegetation cover matrix

        Args:
            frac_vegetation_cover (np.ndarray): Fractional vegetation cover matrix

        Returns:
            np.ndarray: Cavity effect matric
        """
        fractional_veg_cover = self._compute_fvc()
        return  cavity_effect(fractional_veg_cover)
    
    def _get_land_surface_mask(self):
    
        mask_baresoil = (self.ndvi >= self.ndvi_min) & (self.ndvi < self.baresoil_ndvi_max)
        mask_vegetation = (self.ndvi > self.vegatation_ndvi_min) & (self.ndvi <= self.ndvi_max)
        mask_mixed = (self.ndvi >= self.baresoil_ndvi_max) & (self.ndvi <= self.vegatation_ndvi_min)

        return {
                'baresoil': mask_baresoil, 
                'vegetation': mask_vegetation, 
                'mixed': mask_mixed
                }

    def _get_landcover_mask_indices(self):
        """Returns indices corresponding to the different landcover classes of of interest namely:
            vegetation, baresoil and mixed"

        Args:
            landcover ([type]): [description]
        """

        masks = self._get_land_surface_mask()

        # Baresoil value assignment
        baresoil = np.where(masks['baresoil'])
        vegetation = np.where(masks['vegetation'])
        mixed = np.where(masks['mixed'])

        return {'baresoil': baresoil, 'vegetation': vegetation, 'mixed': mixed}

    def _compute_fvc(self):
        # Returns the fractional vegegation cover from the NDVI image.
        # Can be called externally as: fvc = emmisivity_object._compute_fvc()
        return fractional_vegetation_cover(self.ndvi)





def fractional_vegetation_cover(ndvi):
    """[summary]

    Args:
        ndvi (np.ndarray):  Normalized difference vegetation index (m x n)
    Returns:
        np.ndarray: Fractional vegetation cover 
    """
    assert len(ndvi.shape) == 2, "NDVI image should be 2-dimensional"

    return ((ndvi - 0.2)/(0.5 - 0.2))**2



def cavity_effect(fractional_vegetation_cover):
    """Computes cavity effect from fractional vegetation cover matrix

    Args:
        frac_vegetation_cover (np.ndarray): Fractional vegetation cover matrix

    Returns:
        np.ndarray: Cavity effect matric
    """
    #fractional_veg_cover = fractional_vegetation_cover()
    return  0.018009838 * (1 - fractional_vegetation_cover)