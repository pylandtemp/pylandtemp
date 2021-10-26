
import numpy as np

class MonoWindow:
    def __init__(self):
        """
        Method reference:
        Avdan, Ugur, and Gordana Jovanovska. "Algorithm for automated mapping of land surface 
        temperature using LANDSAT 8 satellite data." Journal of sensors 2016 (2016).

        Args:
            compute_brightness_temp (bool, optional): Whether of not convert the input temperature 
                                                        band to TOA brightness temperature equivaent. 
                                                        Defaults to True.
        """


    def __call__(self, brightness_temperature, emmisivity):
        return compute_lst_mono_window(brightness_temperature, emmisivity)
        
    def compute_lst_mono_window(temperature_band, emissivity):
        """[summary]

        Args:
            temperature_band (np.ndarray): Landsat image temperature band (converted to brightness temperature). 
                                            If landsat 8, it's Band 10.
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