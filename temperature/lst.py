from mono_window import MonoWindow
from emissivity.emissivity import Emissivity

LST_METHODS = {'mono_window': MonoWindow}

class LST:

    def __init__(self, method, lst_methods=LST_METHODS):

        assert method in lst_methods, ValueError(f"method must be one of {LST_METHODS}")

        self.lst_methods = lst_methods
        self.method = method

    def __call__(self, emissivity, brightness_temperature_10, brightness_temperature_11=None, column_water_vapour=None):

        lst_method_fn = get_method(self.method)
        dict_input = dict()
        dict_input['emisivity'] = emissivity
        dict_input['brightness_temperature_10'] = brightness_temperature_10
        return

        #! Continue from here
    def _get_methods(self, method):

        return self.lst_methods[self.method]
