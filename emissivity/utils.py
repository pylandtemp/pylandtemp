


def fractional_vegetation_cover(ndvi):
    return ((ndvi - 0.2)/(0.5 - 0.2))**2

def cavity_effect(fractional_vegetation_cover):
    """Computes cavity effect from fractional vegetation cover matrix

    Args:
        frac_vegetation_cover (np.ndarray): Fractional vegetation cover matrix

    Returns:
        np.ndarray: Cavity effect matric
    """
    #fractional_veg_cover = fractional_vegetation_cover()
    return  0.018009838 *(1 - fractional_vegetation_cover)