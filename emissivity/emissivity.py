import numpy as np 
from emissivity.utils import fractional_vegetation_cover, cavity_effect
from emissivity.methods import ComputeMonoWindowEmissivity, ComputeEmissivityNBEM, ComputeEmissivityGopinadh



EMISSIVITY_METHODS = ['avdan', 'xiaolei', 'gopinadh']

class Emissivity:

    def __init__(self, ndvi, red_band=None):
        self.ndvi = ndvi
        self.red_band = red_band
    
    def __call__(self, method):
        assert method in EMISSIVITY_METHODS, ValueError("Method not implemented")
        compute_method = self.get_method(method)

        return compute_method(self.ndvi, self.red_band)()


    def get_method(self, method):

        if method == 'avdan':
            return ComputeMonoWindowEmissivity
        elif method == 'xiaolei':
            return ComputeEmissivityNBEM
        elif method == 'gopinadh':
            return ComputeEmissivityGopinadh
        else:
            raise NotImplementedError("Requested method not implemented. Choose among available methods: {EMMISIVITY_METHODS}")

        








