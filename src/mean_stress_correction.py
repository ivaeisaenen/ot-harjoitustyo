
"""Mean stress corrections"""

def haigh_goodman(stress_amplitude, mean_stress, material_dict):
    """ Goodman mean stress correction"""
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
