import numpy as np 

def compute_LST_splitWindow(t1, t2, e1, e2, cwv=0.013, mask=None):
    #REFERENCE: Skokovic D, Sobrino JA, Jiménez Muñoz JC, SoriaG, Julien Y,Mattar C, Cristóbal J (2014)
    """
    t1 = TOA brightness temperature band 10
    t2 = TOA brightness temperature band 11
    e1 = Emissivity band 10
    e2 = Emissivity band 11
    cwv = Column water vapour
    """

    # TODO: Implement mask. If mask, compute for only non masked locations. 
    # TODO: Optimize code performance. Don't precompute mean_e and diff_e
    # TODO: Move assertion test into a different function 
    # TODO: Move function class with __call__ method 

    mean_e = (e1 + e2) / 2
    diff_e = np.subtract(e1, e2)

    assert t1.shape == t2.shape == e1.shape == e2.shape == cwv.shape, "Images should have the same size"

    lst = (t1 + (1.387 * (t1 - t2)) + (0.183 * ((t1 - t2)**2))
          - 0.268 + ((54.3 - (2.238 * cwv))* (1 - mean_e)) + ((-129.2 + (16.4 * cwv)) * diff_e))
    return lst