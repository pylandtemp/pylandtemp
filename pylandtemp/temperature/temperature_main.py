from pylandtemp.temperature.methods.mono_window import MonoWindowLST
from pylandtemp.temperature.methods.split_window.split_window_methods import (
    SplitWindowJiminezMunozLST,
    SplitWindowKerrLST,
    SplitWindowMcMillinLST,
    SplitWindowPriceLST,
    SplitWindowSobrino1993LST,
    SplitWindowCollCasellesLST
)
from pylandtemp.temperature.utils import get_lst_compute_fn_input
import numpy as np

SINGLE_WINDOW_METHODS = {
        'mono-window': MonoWindowLST
}

SPLIT_WINDOW_METHODS = {
        'jiminez-munoz': SplitWindowJiminezMunozLST,
        'kerr': SplitWindowKerrLST,
        'mc-millin': SplitWindowMcMillinLST,
        'price': SplitWindowPriceLST,
        'sobrino-1993': SplitWindowSobrino1993LST,
        'coll-caselles': SplitWindowCollCasellesLST

}
LST_METHODS = dict(SPLIT_WINDOW_METHODS, **SINGLE_WINDOW_METHODS)


class LST:
    def __init__(self, method, lst_methods=LST_METHODS):

        assert method in lst_methods, ValueError(f"method must be one of {list(lst_methods.keys())}")

        self.lst_methods = lst_methods
        self.method = method
        self.max_earth_temp = (273.15 + 56.7)

    def __call__(
            self, 
            emissivity_10, 
            brightness_temperature_10, 
            emissivity_11=None, 
            brightness_temperature_11=None, 
            ndvi=None,
            mask=None,
            column_water_vapour=None,
            unit = 'kelvin'
        ):

        if unit not in ['kelvin', 'celcius']:
            raise ValueError("unit argument should be set to either 'kelvin' or 'celcius'")

        lst_method_fn = LST_METHODS[self.method]

        dict_input = get_lst_compute_fn_input(
                                    emissivity_10,
                                    emissivity_11, 
                                    brightness_temperature_10, 
                                    brightness_temperature_11, 
                                    ndvi,
                                    mask,
                                    column_water_vapour
                                )

        lst = lst_method_fn()(dict_input)

        if unit == 'celcius':
            lst = lst - 273.15 
        max_temp = self.max_earth_temp if unit == 'kelvin' else self.max_earth_temp - 273.15
        lst[lst > max_temp] = np.nan
        
        return lst

    def _get_methods(self, method):
        if method not in self.lst_methods:
            raise NotImplementedError("Requested method not implemented. Choose among available methods: {self.methods}")
        return self.lst_methods[method]



