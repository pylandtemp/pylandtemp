import numpy as np

from .utils import compute_brightness_temperature


class BrightnessTemperatureLandsat:
    def __init__(self):

        self.mult_factor = 0.0003342
        self.add_factor = 0.1
        self.k1_constant_10 = 774.89
        self.k1_constant_11 = 480.89
        self.k2_constant_10 = 1321.08
        self.k2_constant_11 = 1201.14

    def __call__(
        self, band_10: np.ndarray, band_11: np.ndarray = None, mask=None
    ) -> np.ndarray:
        """

        Args:
            band_10 (np.ndarray): Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data  for Band 10 landsat 8 data
            band_11 (np.ndarray): Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data  for Band 11 landsat 8 data
            unit (str): 'kelvin' or 'celcius'
            mask (bool): Mask zero or NaN values. Defaults to True.


        Returns:
            Tuple(np.ndarray, np.ndarray) -> Band 10 brightness temperature, Band 11 brightness temperature
        """
        tb_band_10 = self._compute_brightness_temp(
            band_10, self.k1_constant_10, self.k2_constant_10, mask
        )

        tb_band_11 = None
        if band_11 is not None:
            tb_band_11 = self._compute_brightness_temp(
                band_11, self.k1_constant_11, self.k2_constant_11, mask
            )

        return tb_band_10, tb_band_11

    def _compute_brightness_temp(
        self, image: np.ndarray, k1: float, k2: float, mask: np.ndarray
    ) -> np.ndarray:

        """Converts image raw digital numbers to brightness temperature

        Args:
            mult_factor (float): Band-specific multiplicative rescaling factor
                                    from the image folder metadata (RADIANCE_MULT_BAND_x, where x is the band index).
            add_factor (float): Band-specific additive rescaling factor
                                    from the image folder metadata (RADIANCE_ADD_BAND_x, where x is the band index).
            k1 (float): Band-specific thermal conversion constant
                                    from the image folder metadata (K1_CONSTANT_BAND_x, where x is the thermal band index)
            k2 (float): Band-specific thermal conversion constant
                                    from the image folder metadata (K2_CONSTANT_BAND_x, where x is the thermal band index
            unit (str):  'kelvin' or 'celcius'. Defaults to 'kelvin'
            mask (n.ndarray[bool]): Truie for pixels to mask out


        Returns:
            np.ndarray: Brightness temperature corrected image.
        """
        return compute_brightness_temperature(
            image, self.mult_factor, self.add_factor, k1, k2, mask
        )
