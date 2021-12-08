import numpy as np

from pylandtemp.utils import fractional_vegetation_cover
from pylandtemp.exceptions import assert_required_keywords_provided


class SplitWindowParentLST:

    # A comparison of all the methods can be found here:
    # https://link.springer.com/article/10.1007/s40808-020-01007-1/tables/3

    def __init__(self):
        self.max_earth_temp = 273.15 + 56.7

    def __call__(self, **kwargs) -> np.ndarray:
        lst = self._compute_lst(**kwargs)
        lst[lst > self.max_earth_temp] = np.nan
        return lst

    def _compute_lst(self, **kwargs):
        raise NotImplementedError("Concrete method yet to be implemented")


class SplitWindowJiminezMunozLST(SplitWindowParentLST):
    cwv = 0.013

    """
    Method reference:

    Jiménez-Muñoz, Juan-Carlos, and José A. Sobrino. "Split-window coefficients for land surface
    temperature retrieval from low-resolution thermal infrared sensors." IEEE geoscience and
    remote sensing letters 5.4 (2008): 806-809.

    """

    def _compute_lst(self, **kwargs) -> np.ndarray:
        """Computes the LST

        kwargs:

        **emissivity_10 (np.ndarray): Emissivity image obtained for band 10
        **emissivity_11 (np.ndarray): Emissivity image obtained for band 11
        **brightness_temperature_10 (np.ndarray): Brightness temperature image obtained for band 10
        **brightness_temperature_11 (np.ndarray): Brightness temperature image obtained for band 11
        **mask (np.ndarray[bool]): Mask image. Output will have NaN value where mask is True.

        Returns:
            np.ndarray: Land surface temperature image
        """

        required_keywords = [
            "emissivity_10",
            "emissivity_11",
            "brightness_temperature_10",
            "brightness_temperature_11",
            "mask",
        ]
        assert_required_keywords_provided(required_keywords, **kwargs)

        tb_10 = kwargs["brightness_temperature_10"]
        tb_11 = kwargs["brightness_temperature_11"]
        emissivity_10 = kwargs["emissivity_10"]
        emissivity_11 = kwargs["emissivity_11"]
        mask = kwargs["mask"]

        mean_e = (emissivity_10 + emissivity_11) / 2
        diff_e = emissivity_10 - emissivity_11
        diff_tb = tb_10 - tb_11

        lst = (
            tb_10
            + (1.387 * diff_tb)
            + (0.183 * (diff_tb ** 2))
            - 0.268
            + ((54.3 - (2.238 * self.cwv)) * (1 - mean_e))
            + ((-129.2 + (16.4 * self.cwv)) * diff_e)
        )
        lst[mask] = np.nan
        return lst


class SplitWindowKerrLST(SplitWindowParentLST):

    """
    Method reference:

    Kerr Y, Lagouarde J, Nerry F, Ottlé C (2004) Land surface temperature
    retrieval techniques and applications: case of the AVHRR. Thermal remote
    sensing in land surface processing. CRC Press, New York, pp 55–131


    """

    def _compute_lst(self, **kwargs) -> np.ndarray:
        """Computes the LST

        kwargs:

        **brightness_temperature_10 (np.ndarray): Brightness temperature image obtained for band 10
        **brightness_temperature_11 (np.ndarray): Brightness temperature image obtained for band 11
        **ndvi (np.ndarray): NDVI image
        **mask (np.ndarray[bool]): Mask image. Output will have NaN value where mask is True.

        Returns:
            np.ndarray: Land surface temperature image
        """

        required_keywords = [
            "brightness_temperature_10",
            "brightness_temperature_11",
            "ndvi",
            "mask",
        ]
        assert_required_keywords_provided(required_keywords, **kwargs)

        tb_10 = kwargs["brightness_temperature_10"]
        tb_11 = kwargs["brightness_temperature_11"]
        ndvi = kwargs["ndvi"]
        mask = kwargs["mask"]

        pv = fractional_vegetation_cover(ndvi)

        lst = (
            (tb_10 * ((0.5 * pv) + 3.1))
            + (tb_11 * ((-0.5 * pv) - 2.1))
            - ((5.5 * pv) + 3.1)
        )
        lst[mask] = np.nan
        return lst


class SplitWindowMcMillinLST(SplitWindowParentLST):
    """
    Method reference:

    McMillin LM (1975) Estimation of sea surface temperatures
    from two infrared window measurements with different absorption.
    J Geophys Res 80(36):5113–5117. https://doi.org/10.1029/JC080i036p05113


    """

    def _compute_lst(self, **kwargs) -> np.ndarray:
        """Computes the keyword arguments

        kwargs:
        **brightness_temperature_10 (np.ndarray): Brightness temperature image obtained for band 10
        **brightness_temperature_11 (np.ndarray): Brightness temperature image obtained for band 11
        **mask (np.ndarray[bool]): Mask image. Output will have NaN value where mask is True.

        Returns:
            np.ndarray: Land surface temperature image
        """
        required_keywords = [
            "brightness_temperature_10",
            "brightness_temperature_11",
            "mask",
        ]
        assert_required_keywords_provided(required_keywords, **kwargs)

        tb_10 = kwargs["brightness_temperature_10"]
        tb_11 = kwargs["brightness_temperature_11"]
        mask = kwargs["mask"]

        lst = (1.035 * tb_10) + (3.046 * (tb_10 - tb_11)) - 10.93
        lst[mask] = np.nan
        return lst


class SplitWindowPriceLST(SplitWindowParentLST):
    """
    Method reference:

    Price JC (1984) Land surface temperature measurements from the split window
    channels of the NOAA advanced very high-resolution radiometer. J Geophys Res 89:7231–7237.
    https://doi.org/10.1029/JD089iD05p07231

    """

    def _compute_lst(self, **kwargs) -> np.ndarray:
        """Computes the LST

        kwargs:
        **emissivity_10 (np.ndarray): Emissivity image obtained for band 10
        **emissivity_11 (np.ndarray): Emissivity image obtained for band 11
        **brightness_temperature_10 (np.ndarray): Brightness temperature image obtained for band 10
        **brightness_temperature_11 (np.ndarray): Brightness temperature image obtained for band 11
        **mask (np.ndarray[bool]): Mask image. Output will have NaN value where mask is True.

        Returns:
            np.ndarray: Land surface temperature image
        """
        required_keywords = [
            "emissivity_10",
            "emissivity_11",
            "brightness_temperature_10",
            "brightness_temperature_11",
            "mask",
        ]
        assert_required_keywords_provided(required_keywords, **kwargs)

        tb_10 = kwargs["brightness_temperature_10"]
        tb_11 = kwargs["brightness_temperature_11"]
        emm_10 = kwargs["emissivity_10"]
        emm_11 = kwargs["emissivity_11"]
        mask = kwargs["mask"]

        lst = (tb_10 + 3.33 * (tb_10 - tb_11)) * ((5.5 - emm_10) / 4.5) + (
            0.75 * tb_11 * (emm_10 - emm_11)
        )
        lst[mask] = np.nan
        return lst


class SplitWindowSobrino1993LST(SplitWindowParentLST):
    """
    Method reference:

    Sobrino JA, Caselles V, Coll C (1993) Theoretical split window algorithms
    for determining the actual surface temperature. I1Nuovo Cimento 16:219–236.
    https://doi.org/10.1007/BF02524225

    """

    def _compute_lst(self, **kwargs) -> np.ndarray:

        """
        kwargs:

        **emissivity_10 (np.ndarray): Emissivity image obtained for band 10
        **emissivity_11 (np.ndarray): Emissivity image obtained for band 11
        **brightness_temperature_10 (np.ndarray): Brightness temperature image obtained for band 10
        **brightness_temperature_11 (np.ndarray): Brightness temperature image obtained for band 11
        **mask (np.ndarray[bool]): Mask image. Output will have NaN value where mask is True.

        Returns:
            np.ndarray: Land surface temperature image
        """
        required_keywords = [
            "emissivity_10",
            "emissivity_11",
            "brightness_temperature_10",
            "brightness_temperature_11",
            "mask",
        ]
        assert_required_keywords_provided(required_keywords, **kwargs)

        tb_10 = kwargs["brightness_temperature_10"]
        tb_11 = kwargs["brightness_temperature_11"]
        emm_10 = kwargs["emissivity_10"]
        emm_11 = kwargs["emissivity_11"]
        mask = kwargs["mask"]

        diff_tb = tb_10 - tb_11
        diff_e = emm_10 - emm_11

        lst = (
            tb_10
            + (1.06 * (diff_tb))
            + (0.46 * diff_tb ** 2)
            + (53 * (1 - emm_10))
            - (53 * (diff_e))
        )
        lst[mask] = np.nan
        return lst
