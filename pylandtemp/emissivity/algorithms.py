import numpy as np

from pylandtemp.utils import rescale_band, cavity_effect, fractional_vegetation_cover


class Emissivity:
    def __init__(self):
        """Parent class for all emissivity methods. Contains general methods and attributes"""
        self.ndvi_min = -1
        self.ndvi_max = 1
        self.baresoil_ndvi_max = 0.2
        self.vegatation_ndvi_min = 0.5

    def __call__(self, **kwargs) -> np.ndarray:
        """Computes the emissivity

        kwargs:
        **ndvi (np.ndarray): NDVI image
        **red_band (np.ndarray): Band 4 or Red band image.
        **mask (np.ndarray[bool]): Mask image. Output will have NaN value where mask is True.


        Returns:
            Tuple(np.ndarray, np.ndarray): Emissivity for bands 10 and 11 respectively
        """
        if "ndvi" not in kwargs:
            raise ValueError("NDVI image is not provided")

        if "red_band" not in kwargs:
            raise ValueError("Band 4 (red band) image is not provided")

        self.ndvi = kwargs["ndvi"]
        self.red_band = kwargs["red_band"]

        if (
            self.ndvi is not None
            and self.red_band is not None
            and self.ndvi.shape != self.red_band.shape
        ):
            raise ValueError(
                "Input images (NDVI and Red band) must be of equal dimension"
            )

        emm_10, emm_11 = self._compute_emissivity()
        mask = emm_10 == 0
        emm_10[mask] = np.nan
        if emm_11 is not None:
            emm_11[mask] = np.nan
        return emm_10, emm_11

    def _compute_emissivity(self):
        raise NotImplementedError("No concrete implementation of emissivity method yet")

    def _get_land_surface_mask(self):
        mask_baresoil = (self.ndvi >= self.ndvi_min) & (
            self.ndvi < self.baresoil_ndvi_max
        )
        mask_vegetation = (self.ndvi > self.vegatation_ndvi_min) & (
            self.ndvi <= self.ndvi_max
        )
        mask_mixed = (self.ndvi >= self.baresoil_ndvi_max) & (
            self.ndvi <= self.vegatation_ndvi_min
        )
        return {
            "baresoil": mask_baresoil,
            "vegetation": mask_vegetation,
            "mixed": mask_mixed,
        }

    def _get_landcover_mask_indices(self):
        """Returns indices corresponding to the different landcover classes of of interest namely:
        vegetation, baresoil and mixed"
        """
        masks = self._get_land_surface_mask()
        baresoil = np.where(masks["baresoil"])
        vegetation = np.where(masks["vegetation"])
        mixed = np.where(masks["mixed"])
        return {"baresoil": baresoil, "vegetation": vegetation, "mixed": mixed}

    def _compute_fvc(self):
        # Returns the fractional vegegation cover from the NDVI image.
        return fractional_vegetation_cover(self.ndvi)


class ComputeMonoWindowEmissivity(Emissivity):

    emissivity_soil_10 = 0.97
    emissivity_veg_10 = 0.99
    emissivity_soil_11 = None
    emissivity_veg_11 = None

    def _compute_emissivity(self) -> np.ndarray:
        emm = np.empty_like(self.ndvi)
        landcover_mask_indices = self._get_landcover_mask_indices()

        # Baresoil value assignment
        emm[landcover_mask_indices["baresoil"]] = self.emissivity_soil_10
        # Vegetation value assignment
        emm[landcover_mask_indices["vegetation"]] = self.emissivity_veg_10
        # Mixed value assignment
        emm[landcover_mask_indices["mixed"]] = (
            0.004
            * (((self.ndvi[landcover_mask_indices["mixed"]] - 0.2) / (0.5 - 0.2)) ** 2)
        ) + 0.986
        return emm, emm


class ComputeEmissivityNBEM(Emissivity):
    """
    Method references:

    1. Li, Tianyu, and Qingmin Meng. "A mixture emissivity analysis method for
        urban land surface temperature retrieval from Landsat 8 data." Landscape
        and Urban Planning 179 (2018): 63-71.

    2. Yu, Xiaolei, Xulin Guo, and Zhaocong Wu. "Land surface temperature retrieval
        from Landsat 8 TIRS—Comparison between radiative transfer equation-based method,
        split window algorithm and single channel method." Remote sensing 6.10 (2014): 9829-9852.

    """

    emissivity_soil_10 = 0.9668
    emissivity_veg_10 = 0.9863
    emissivity_soil_11 = 0.9747
    emissivity_veg_11 = 0.9896

    def _compute_emissivity(self) -> np.ndarray:

        if self.red_band is None:
            raise ValueError(
                "Red band cannot be {} for this emissivity computation method".format(
                    self.red_band
                )
            )

        self.red_band = rescale_band(self.red_band)
        landcover_mask_indices = self._get_landcover_mask_indices()
        fractional_veg_cover = self._compute_fvc()

        def calc_emissivity_for_band(
            image,
            emissivity_veg,
            emissivity_soil,
            cavity_effect,
            red_band_coeff_a=None,
            red_band_coeff_b=None,
        ):
            image[landcover_mask_indices["baresoil"]] = red_band_coeff_a - (
                red_band_coeff_b * self.red_band[landcover_mask_indices["baresoil"]]
            )

            image[landcover_mask_indices["mixed"]] = (
                (emissivity_veg * fractional_veg_cover[landcover_mask_indices["mixed"]])
                + (
                    emissivity_soil
                    * (1 - fractional_veg_cover[landcover_mask_indices["mixed"]])
                )
                + cavity_effect[landcover_mask_indices["mixed"]]
            )

            image[landcover_mask_indices["vegetation"]] = (
                emissivity_veg + cavity_effect[landcover_mask_indices["vegetation"]]
            )
            return image

        emissivity_band_10 = np.empty_like(self.ndvi)
        emissivity_band_11 = np.empty_like(self.ndvi)
        frac_vegetation_cover = self._compute_fvc()

        cavity_effect_10 = cavity_effect(
            self.emissivity_veg_10, self.emissivity_soil_10, fractional_veg_cover
        )
        cavity_effect_11 = cavity_effect(
            self.emissivity_veg_11, self.emissivity_soil_11, fractional_veg_cover
        )

        emissivity_band_10 = calc_emissivity_for_band(
            emissivity_band_10,
            self.emissivity_veg_10,
            self.emissivity_soil_10,
            cavity_effect_10,
            red_band_coeff_a=0.973,
            red_band_coeff_b=0.047,
        )
        emissivity_band_11 = calc_emissivity_for_band(
            emissivity_band_11,
            self.emissivity_veg_11,
            self.emissivity_soil_11,
            cavity_effect_11,
            red_band_coeff_a=0.984,
            red_band_coeff_b=0.026,
        )
        return emissivity_band_10, emissivity_band_11


class ComputeEmissivityGopinadh(Emissivity):
    """
    Method reference:

    Rongali, Gopinadh, et al. "Split-window algorithm for retrieval of land surface temperature
    using Landsat 8 thermal infrared data." Journal of Geovisualization and Spatial Analysis 2.2
    (2018): 1-19.
    """

    emissivity_soil_10 = 0.971
    emissivity_veg_10 = 0.987

    emissivity_soil_11 = 0.977
    emissivity_veg_11 = 0.989

    def _compute_emissivity(self) -> np.ndarray:

        fractional_veg_cover = self._compute_fvc()

        def calc_emissivity_for_band(
            image, emissivity_veg, emissivity_soil, fractional_veg_cover
        ):
            emm = (emissivity_soil * (1 - fractional_veg_cover)) + (
                emissivity_veg * fractional_veg_cover
            )
            return emm

        emissivity_band_10 = np.empty_like(self.ndvi)
        emissivity_band_10 = calc_emissivity_for_band(
            emissivity_band_10,
            self.emissivity_veg_10,
            self.emissivity_soil_10,
            fractional_veg_cover,
        )

        emissivity_band_11 = np.empty_like(self.ndvi)
        emissivity_band_11 = calc_emissivity_for_band(
            emissivity_band_11,
            self.emissivity_veg_11,
            self.emissivity_soil_11,
            fractional_veg_cover,
        )
        return emissivity_band_10, emissivity_band_11
