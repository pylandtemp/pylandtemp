import numpy as np
from utils import compute_brightness_temp
from typing import List, Optional 
import numpy.ma as ma


def generate_mask(image, mask_zeros=False)-> np.ndarray:
    """
    Return a bool array masking 0 and NaN values as False and others as True

    Args:
        image (np.ndarray): Single-band image

    return:
        np.ndarray
    """

    
    nan_mask = image == np.nan
    if mask_zeros:
        zero_mask = image == 0 
        mask_true = np.logical_and(zero_mask, nan_mask)
    else:
        mask_true = nan_mask

    return mask_true

# class ComputeMask:
#     def __init__(self, value_to_mask: int)->np.ndarray:
#         """This class takes a raster image and returns a mask which is true where the pixel values are equal value_to_mask

#         Args:
#             mask_values (int): value to mask. E.g 0 will return True for all 0 values and False everywhere else.
#         """
#         self.value_to_mask = value_to_mask

#     def __call__(self, img: np.ndarray):
#         masked_img = ma.masked_less_equal(img, self.value_to_mask)
#         return masked_img.mask



class ClipToBound:
    raise NotImplementedError


class MaskCloudyPixels:
    raise NotImplementedError