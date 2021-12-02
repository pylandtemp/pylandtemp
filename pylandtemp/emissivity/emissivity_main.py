import numpy as np 
from pylandtemp.emissivity.methods import ComputeMonoWindowEmissivity, ComputeEmissivityNBEM, ComputeEmissivityGopinadh



#EMISSIVITY_METHODS = ['avdan', 'xiaolei', 'gopinadh']

EMISSIVITY_METHODS = {'avdan': ComputeMonoWindowEmissivity, 
                        'xiaolei': ComputeEmissivityNBEM, 
                        'gopinadh': ComputeEmissivityGopinadh
                        }

class Emissivity:

    def __init__(self, ndvi, red_band=None, methods=EMISSIVITY_METHODS):
        """
        This class computes the land surface emissivity and returns it as a numpy array

        Args:
            ndvi (np.ndarray[float]): Normalized difference vegetation index (NDVI) image matrix
            red_band (np.ndarray[float]): Red band of image (0.63-0.69 micrometers)
        """
        self.ndvi = ndvi
        self.red_band = red_band
        self.methods = methods
    
    def __call__(self, method):
        assert method in self.methods, ValueError("Requested method not implemented. Choose among available methods: {self.methods}")

        compute_method = self._get_method(method)

        return compute_method(self.ndvi, self.red_band)()


    def _get_method(self, method):

        if method not in self.methods:
            raise NotImplementedError("Requested method not implemented. Choose among available methods: {self.methods}")
        
        return self.methods.get(method)

        








