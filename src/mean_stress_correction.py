"""Mean stress correction module"""
def haigh_none(stress_amplitude, mean_stress, material_dict):
    """No mean stress correction. Usefull for example shear based criterion as
        many believe there is no mean shear effect"""
    return material_dict["fR1"]


def haigh_goodman(stress_amplitude, mean_stress, material_dict):
    """ Goodman mean stress correction is recommended for high-strength/low-ductility materials

    Parameters
    ----------
        stress_amplitude: float
            Equivalent stress amplitude
        mean_stress: float
            Equivalent mean stress
        material_dict: dict
            Dictionary with keys and values (at least)
                "fR1": float
                "Rm": float

    Returns
    -------
        fatigue_limit_mean_stress_corrected: float
            Fatigue limit or stress amplitude with Googman mean stress correction

    Note: This versio of Goodman mean stress correction is symmetric for tension and compression,
        and not costant fatigue limit for compresion as it is often modelled.
    """
    assert stress_amplitude >= 0
    fatigue_limit_fully_reversed = material_dict["fR1"]
    ultimate_limit = material_dict["Rm"]

    # Check if there is value for compression side then use that value if there is
    if "Rmc" in material_dict:
        ultimate_limit_compression = material_dict["Rmc"]
    else:
        ultimate_limit_compression = -ultimate_limit

    if ultimate_limit > mean_stress >= 0:
        fatigue_limit_mean_stress_corrected =  -(fatigue_limit_fully_reversed/ultimate_limit) * \
        mean_stress + fatigue_limit_fully_reversed
    elif ultimate_limit_compression < mean_stress < 0:
        fatigue_limit_mean_stress_corrected = \
        -(fatigue_limit_fully_reversed/ultimate_limit_compression) * \
        mean_stress + fatigue_limit_fully_reversed
    else:
        fatigue_limit_mean_stress_corrected = 0
    return fatigue_limit_mean_stress_corrected


def haigh_gerbel(stress_amplitude, mean_stress, material_dict):
    """ Gerbel mean stress correction is recommended for ductile materials

    Parameters
    ----------
        stress_amplitude: float
            Equivalent stress amplitude
        mean_stress: float
            Equivalent mean stress
        material_dict: dict
            Dictionary with keys and values (at least)
                "fR1": float
                "Rm": float

    Returns
    -------
        fatigue_limit_mean_stress_corrected: float
            Fatigue limit or stress amplitude with Gerbel mean stress correction

    Note: This versio of Gerbel mean stress correction is symmetric for tension and compression,
        and not costant fatigue limit for compresion as it is often modelled.
    """
    assert stress_amplitude >= 0
    fatigue_limit_fully_reversed = material_dict["fR1"]
    ultimate_limit = material_dict["Rm"]

    # Check if there is value for compression side then use that value if there is
    if "Rmc" in material_dict:
        ultimate_limit_compression = material_dict["Rmc"]
    else:
        ultimate_limit_compression = -ultimate_limit

    if ultimate_limit > mean_stress >= 0:
        fatigue_limit_mean_stress_corrected =  -(fatigue_limit_fully_reversed/ultimate_limit**2) * \
        mean_stress**2 + fatigue_limit_fully_reversed

    elif ultimate_limit_compression < mean_stress < 0:
        fatigue_limit_mean_stress_corrected = \
            -(fatigue_limit_fully_reversed/ultimate_limit_compression**2) * \
            mean_stress**2 + fatigue_limit_fully_reversed
    else:
        fatigue_limit_mean_stress_corrected = 0
    return fatigue_limit_mean_stress_corrected


def haigh_soderberg(stress_amplitude, mean_stress, material_dict):
    """ Soderberg mean stress correction

    Parameters
    ----------
        stress_amplitude: float
            Equivalent stress amplitude
        mean_stress: float
            Equivalent mean stress
        material_dict: dict
            Dictionary with keys and values (at least)
                "fR1": float
                "Rp02": float

    Returns
    -------
        fatigue_limit_mean_stress_corrected: float
            Fatigue limit or stress amplitude with Soderberg mean stress correction

    Note: This versio of Soderberg mean stress correction is symmetric for tension and compression,
        and not costant fatigue limit for compresion as it is often modelled.
    """
    assert stress_amplitude >= 0
    fatigue_limit_fully_reversed = material_dict["fR1"]
    rp02_limit = material_dict["Rp02"]

    # Check if there is value for compression side then use that value if there is
    if "Rpc02" in material_dict:
        rp02_compression_limit = material_dict["Rpc02"]
    else:
        rp02_compression_limit = -rp02_limit

    # Tension side
    if rp02_limit > mean_stress >= 0:

        fatigue_limit_mean_stress_corrected =  -(fatigue_limit_fully_reversed/rp02_limit) * \
        mean_stress + fatigue_limit_fully_reversed

    # Compression side
    elif rp02_compression_limit < mean_stress < 0:
        fatigue_limit_mean_stress_corrected = \
            -(fatigue_limit_fully_reversed/rp02_compression_limit) * \
            mean_stress + fatigue_limit_fully_reversed
    else:
        fatigue_limit_mean_stress_corrected = 0
    return fatigue_limit_mean_stress_corrected
