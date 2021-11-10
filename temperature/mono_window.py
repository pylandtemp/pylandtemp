
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


    #def __call__(self, brightness_temperature, emmisivity):
    #   
    #    dict_input = dict()
    #    dict_input['brightness_temperature_10'] = brightness_temperature
    #    dict_input['emissivity'] = emissivity
    #
    #    return compute_lst_mono_window(dict_input)
    
    def __call__(self, dict_):
        return self._compute_lst_mono_window(dict_)

    def _compute_lst_mono_window(self, dict_):
        """[summary]
        dict_ should contain the following keys
        dict_ keys:
                brightness_temperature_10 (np.ndarray): Landsat 8 image band 10  (converted to brightness temperature). 
                emissivity (np.ndarray): The emmisivity image derived from computing emissivity

        Returns:
            np.ndarray: Land surface temmperature
        """
        temperature_band = dict_['brightness_temperature_10']
        emissivity = dict_['emissivity']

        if temperature_band.shape != emissivity.shape:
            raise ValueError("Temperature image and emissivity images must be of the same size/shape")

        land_surface_temp = (temperature_band / 
                            (1 + 
                            (((0.0000115 * 
                            temperature_band) / 
                            14380) * 
                            np.log(emissivity)))
        )

        nan_mask = np.isnan(emissivity)
        land_surface_temp[nan_mask] = np.nan 
        return land_surface_temp

        def generate_nan_mask(self, image)-> ndarray:
            
            return np.isnan(image) 