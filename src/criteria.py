"""Stress, equivalent stress and stress_amplitudefety factor calculations"""

def _mises(stress: list):
    """ Calculates signed von mises stress"""
    if sum(stress[:3]) >= 0.0:
        sign = 1
    else:
        sign = -1
    signed_mises = sign * (0.5 * ((stress[0]-stress[1])**2 +
                    (stress[1]-stress[2])**2 + (stress[2]-stress[0])**2 +
                    6*(stress[3]**2+stress[4]**2+stress[5]**2)))**0.5
    return signed_mises


def calculate_equivalent_mises(stress_history: list):
    """Takes stress history of one node"""
    mises_stresses = []
    for stress in stress_history:
        mises_stresses.append(_mises(stress))

    stress_amplitude = 0.5 * (max(mises_stresses) - min(mises_stresses))
    mean_stress = 0.5 * (max(mises_stresses) + min(mises_stresses))
    return stress_amplitude, mean_stress


def calculate_mises_sf(stress_history_dict: dict, material_dict: dict, msc):
    """ Calculates stress_amplitudefety Factor based on material values and stress history"""

    result_dict = {}
    for id_, stress_history in stress_history_dict.items():

        # Equivalent stress
        stress_amplitude, mean_stress = calculate_equivalent_mises(stress_history)

        # Mean stress correction
        stress_amplitudef = msc(stress_amplitude, mean_stress, material_dict)
        try:
            safety_factor = stress_amplitudef / stress_amplitude
        except ZeroDivisionError:
            safety_factor = stress_amplitudef / 1e-9
        result_dict[id_] = {"SF": safety_factor,
                           "Saf":stress_amplitudef,
                           "Sa":stress_amplitude,
                           "Sm": mean_stress}
    return result_dict
