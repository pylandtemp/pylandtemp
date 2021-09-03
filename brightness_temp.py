
import numpy as np
from utils import compute_brightness_temp
from typing import List, Optional 
import numpy.ma as ma



class LandsatBrightnessTemp:
    def __init__(
                self, 
                mult_factor: float, 
                add_factor: float , 
                k1_constant: float, 
                k2_constant: float, 
                unit: str='kelvin'
                
            ):
        """[Converts image raw digital numbers to brightness temperature]

        Args:
            mult_factor (float): Band-specific multiplicative rescaling factor from the image folder metadata (RADIANCE_MULT_BAND_x, where x is the band index).
            add_factor (float): Band-specific additive rescaling factor from the image folder metadata (RADIANCE_ADD_BAND_x, where x is the band index).
            k1_constant (float): Band-specific thermal conversion constant from the image folder metadata (K1_CONSTANT_BAND_x, where x is the thermal band index)
            k2_constant (float): Band-specific thermal conversion constant from the image folder metadata (K2_CONSTANT_BAND_x, where x is the thermal band index
            unit (str):  'kelvin' or 'celcius'. Defaults to 'kelvin'
            

        Returns:
            [np.ndarray]: [Brightness temperature corrected image]
        """

        self.mult_factor = mult_factor
        self.add_factor = add_factor
        self.k1_constant = k1_constant
        self.k2_constant = k2_constant
        self.unit = unit
    
    def __call__(self, image: np.ndarray, mask=None)->np.ndarray: #: Optional[np.ndarray]=None)
        """
        image (np.ndarray): Level 1 quantized and calibrated scaled Digital Numbers (DN) TIR band data (e.g Band 10 landsat 8 data)
        mask (bool): Mask zero or NaN values. Defaults to True 
        """
        return self._brightness_temp(image, mask)
    
    
    def _brightness_temp(self, image: np.ndarray, mask: bool=True):

        return compute_brightness_temp(image, self.mult_factor, self.add_factor, self.k1_constant, self.k2_constant, unit=self.unit, mask=mask)


    def _collect_fns(self, methods: List[str]):
        
        raise NotImplementedError