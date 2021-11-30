import math
import numpy as np





def compute_cwv(TB_band1, TB_band2, window_size):
    """
    TB_band1: Band 10 TOA brightness temperature on obtained from the function is STEP 1 
    TB_band2: Band 11 TOA brightness temperature on obtained from the function is STEP 1
    window_size: Size of kernel in computing transmittance ratio. (See reference publication)
    """
    assert (window_size % 2) == 1, "Window size should be a odd number"
    trans_mat_output = np.zeros(TB_band1.shape) #Transmitance ratio
    padding_pixels = math.floor(window_size / 2)
    TB_band1_pad = np.pad(TB_band1, padding_pixels, 'reflect')
    TB_band2_pad = np.pad(TB_band2, padding_pixels, 'reflect')
    for i in range(0, TB_band1_pad.shape[0] - window_size + 1):
        for j in range(0, TB_band2_pad.shape[1] - window_size + 1):
            window_TB_band1 = TB_band1_pad[i:i + window_size, j:j + window_size]
            window_TB_band2 = TB_band2_pad[i:i + window_size, j:j + window_size]
            numerator = np.sum(np.multiply((window_TB_band1 - (np.median(window_TB_band1))),
                                           (window_TB_band2 - (np.median(window_TB_band2)))))
            # print(window_TB_band1, window_TB_band2)
            denominator = np.sum((window_TB_band1 - np.median(window_TB_band1)) ** 2)
            # print(numerator)
            trans_mat_output[i, j] = numerator / denominator
   
    C0 = 9.087
    C1 = 0.653
    C2 = -9.674
    cwv_matrix = C0 + (C1 * trans_mat_output) + (C2 * (trans_mat_output ** 2))
    
    return cwv_matrix