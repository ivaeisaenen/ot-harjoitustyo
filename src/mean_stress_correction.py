
"""Mean stress corrections"""

def haigh_goodman(stress_amplitude, mean_stress, material_dict):
    """ Goodman mean stress correction

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
    if ultimate_limit > mean_stress >= 0:
        fatigue_limit_mean_stress_corrected =  -(fatigue_limit_fully_reversed/ultimate_limit) * \
        mean_stress + fatigue_limit_fully_reversed
    elif -ultimate_limit < mean_stress < 0:
        fatigue_limit_mean_stress_corrected = (fatigue_limit_fully_reversed/ultimate_limit) * \
        mean_stress + fatigue_limit_fully_reversed
    else:
        fatigue_limit_mean_stress_corrected = 0
    return fatigue_limit_mean_stress_corrected
