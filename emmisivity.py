import numpy as np 


class Emissivity():

    def __init__(self, method:str):
        assert method in [], '...'
        self.method= method

    def __call__(self, ndvi):
        pass

def mono_window_emmissivity(ndvi: np.ndarray)->np.ndarray:
    """
    compute emmissivity from ndvi image 

    # Reference:

    Args:
        ndvi (np.ndarray): normalised difference vegetation index (cloud and water masked). Use getemp.compute_ndvi(...) to obtain 
        ndvi image that is masked 

    Returns:
        np.ndarray: Emissivity image
    """
    emissivity = np.empty(ndvi.shape)
    # Reference:
    nan_mask = np.isnan(ndvi_image)
    
    # Set values in emissivity matrix based on NDVI matrix value with same index
    mask1 = (ndvi >= -1) & (ndvi < 0.2)
    mask2 = (ndvi > 0.5) & (ndvi <= 1)
    mask3 = (ndvi >= 0.2) & (ndvi <= 0.5)
    

    i, j = np.where(mask1)
    emissivity[i, j] = 0.97
    i, j =np.where(mask2)
    emissivity[i, j] = 0.99
    i, j = np.where(mask3)
    emissivity[i, j] = (0.004*(((ndvi[i, j] - 0.2)/(0.5 - 0.2))**2)) + 0.986
    i, j = np.where(nan_mask)
    emissivity[i, j] = np.nan
    return emissivity