
import numpy as np

from temperature.utils import  compute_brightness_temperature


#! Take the brightness temperature variables as **kwargs to the class
#! continue from here 

class MonoWindow:
    def __init__(self, compute_brightness_temp=True):
        """
        Method reference:
        Avdan, Ugur, and Gordana Jovanovska. "Algorithm for automated mapping of land surface 
        temperature using LANDSAT 8 satellite data." Journal of sensors 2016 (2016).

        Args:
            compute_brightness_temp (bool, optional): Whether of not convert the input temperature 
                                                        band to TOA brightness temperature equivaent. 
                                                        Defaults to True.
        """

        self.compute_brightness_temp = compute_brightness_temp

    def __call__(self):
        pass 
        
    #STEP 3: DERIVE LST WITH MONO-WINDOW ALGORITHM (This function takes the TOA brightness temperature and emissivity images as imput to comput LST)
    def compute_lst_mono_window(temperature_band, emissivity):
        """[summary]

        Args:
            temperature_band (np.ndarray): Landsat image temperature band. If landsat 8, it's Band 10.
            emissivity (np.ndarray): The emmisivity image derived from computing emissivity

        Returns:
            np.ndarray: Land surface temmperature
        """
        if temperature_band.shape != emissivity.shape:
            raise ValueError("Temperature image and emissivity images must be of the same size/shape")

        land_surface_temp = (temperature_band / 
                            (1 + 
                            (((0.0000115 * 
                            TB_temperature_bandband10) / 
                            14380) * 
                            np.log(emissivity)))
        )
        return land_surface_temp