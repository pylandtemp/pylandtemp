
import numpy as np

from emissivity import Emissivity


class MonoWindow:
    def __init__(self, compute_brightness_temp=False):
        self.compute_brightness_temp = compute_brightness_temp

    def __call__(self, )
#STEP 3: DERIVE LST WITH MONO-WINDOW ALGORITHM (This function takes the TOA brightness temperature and emissivity images as imput to comput LST)
def compute_LST_mono_window(TB_band10, emissivity):
    #REFERENCE: Avdan, Ugur, and Gordana Jovanovska. "Algorithm for automated mapping of land surface temperature using LANDSAT 8 satellite data." Journal of Sensors 2016 (2016).
    assert TB_band10.shape == emissivity.shape, "TOA Brightness Temperature and emissivity images must be of the same size"
    #Compute and Surface Temperature matrix
    land_surface_temp = TB_band10 / (1 + (((0.0000115 * TB_band10) / 14380) * np.log(emissivity)))
    return land_surface_temp