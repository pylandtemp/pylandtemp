import numpy as np


class MonoWindowLST:
    def __init__(self):
        """
        Method reference:
        Avdan, Ugur, and Gordana Jovanovska. "Algorithm for automated mapping of land surface
        temperature using LANDSAT 8 satellite data." Journal of sensors 2016 (2016).
        """

    def __call__(self, **kwargs) -> np.ndarray:
        """

        kwargs:

        **emissivity_10 (np.ndarray): Emissivity image obtained for band 10
        **brightness_temperature_10 (np.ndarray): Brightness temperature image obtained for band 10
        **mask (np.ndarray[bool]): Mask image. Output will have NaN value where mask is True.

        Returns:
            np.ndarray: Land surface temperature image
        """
        return self._compute_lst_mono_window(**kwargs)

    def _compute_lst_mono_window(self, **kwargs) -> np.ndarray:
        """
        Computes the LST

        kwargs:

        **emissivity_10 (np.ndarray): Emissivity image obtained for band 10
        **brightness_temperature_10 (np.ndarray): Brightness temperature image obtained for band 10
        **mask (np.ndarray[bool]): Mask image. Output will have NaN value where mask is True.

        Returns:
            np.ndarray: Land surface temperature image
        """

        if "brightness_temperature_10" not in kwargs:
            raise ValueError(
                "Keyword arg 'bright_temperature_10' should be provided in input for this LST method"
            )

        if "emissivity_10" not in kwargs:
            raise ValueError(
                "Keyword arg 'emissivity_10' should be provided in input for this LST method"
            )

        if "mask" not in kwargs:
            raise ValueError(
                "Keyword arg 'mask' should be provided in input for this LST method"
            )

        temperature_band = kwargs["brightness_temperature_10"]
        emissivity = kwargs["emissivity_10"]
        mask = kwargs["mask"]

        if temperature_band.shape != emissivity.shape:
            raise ValueError("Input images must be of the same size/shape")

        land_surface_temp = temperature_band / (
            1 + (((0.0000115 * temperature_band) / 14380) * np.log(emissivity))
        )
        land_surface_temp[mask] = np.nan
        return land_surface_temp
