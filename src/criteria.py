"""Stress, equivalent stress, stress_amplitude, mean_stress and safety factor calculations"""

import numpy as np


def _mises(stress: list):
    """Calculates signed von mises stress

    Parameters:
    ----------
        stress: list
            A stress using Voigh notation

    Returns
    -------
        signed_mises: float
            Signed Von Mises stress
    """

    if sum(stress[:3]) >= 0.0:
        sign = 1
    else:
        sign = -1
    signed_mises = sign * (0.5 * ((stress[0]-stress[1])**2 +
                    (stress[1]-stress[2])**2 + (stress[2]-stress[0])**2 +
                    6*(stress[3]**2+stress[4]**2+stress[5]**2)))**0.5
    return signed_mises


def _tresca(stress: list):
    """Calculates Tresca stress

    Parameters:
    ----------
        stress: list
            A stress using Voigh notation

    Returns
    -------
        tresca: float
            Tresca stress
    """
    stress_tensor = np.array([[stress[0], stress[5], stress[4]],
                              [stress[5], stress[1], stress[3]],
                              [stress[4], stress[3], stress[2]]])

    eigenvalues, eigenvectors = np.linalg.eig(stress_tensor)
    p3,p2,p1 = np.sort(eigenvalues)
    tresca = 0.5*(p1-p3)
    return tresca


def calculate_equivalent_tresca(stress_history: list):
    """Takes stress history of one node and returns stress amplitude and mean stress
        ie equivalent stress

    Parameters
    ----------
        stress_history: list
            Time history of stress for one node

    Returns
    -------
        stress_amplitude: float
            Stress amplitude of given stress history
        mean_stress: float
            Mean stress of given stress history

    Note! If only one stress history loading is given, it will be compared to zero loading state
    """

    tresca_stresses = []
    for stress in stress_history:
        tresca_stresses.append(_tresca(stress))

    stress_amplitude = max(tresca_stresses)
    mean_stress = 0.5*(max(tresca_stresses)+min(tresca_stresses))

    return stress_amplitude, mean_stress


def calculate_equivalent_mises(stress_history: list):
    """Takes stress history of one node and returns stress amplitude and mean stress
        ie equivalent stress

    Parameters
    ----------
        stress_history: list
            Time history of stress for one node

    Returns
    -------
        stress_amplitude: float
            Stress amplitude of given stress history
        mean_stress: float
            Mean stress of given stress history

    Note! If only one stress history loading is given, it will be compared to zero loading state
    """

    mises_stresses = []
    for stress in stress_history:
        mises_stresses.append(_mises(stress))

    if len(mises_stresses) == 1:
        stress_amplitude = 0.5 * (mises_stresses[0] - 0)
        mean_stress = 0.5 * (mises_stresses[0] + 0)
    else:
        stress_amplitude = 0.5 * (max(mises_stresses) - min(mises_stresses))
        mean_stress = 0.5 * (max(mises_stresses) + min(mises_stresses))

    return stress_amplitude, mean_stress


def calculate_tresca_sf(stress_history_dict: dict, material_dict: dict, msc):
    """ Calculates safety factor based on material values and stress history
        for all nodes in the stress_history_dict using provided mean stress correction msc

        Note! Tresca needs only tR1

    Parameters
    ----------
        stress_history_dict: dict
            Stress history for every node. The node is the key in the dict
            and value is list of stress tensors as history.
        material_dict: dict:
            Material parameters as dictionary for example [example units]:
                "fR1" : fatigue limit for fully alternating loading R=-1 [MPa]
                "fR0" : fatigue limit for pulsating loading R=0 [MPa]
                "tR1" : fatigue limit for fully alternating shear loading R=-1 [Mpa]
                "tR0" : fatigue limit for pulsating shear loading R=0 [Mpa]
                "Rm" : ultimate strenght (for tension) [MPa]
                "Rp02" : Relatively limit 0.2 % for tension [MPa]
                "Rmc" : Ultimate strenght for compresion [MPa]
                "Rp02c" : Relatively limit 0.2 % for compression [MPa]
        msc: func
            Function for mean stress correction

    Returns
    -------
        result_dict: dict
            Dictionary with results:
                "SF" safety factor
                "Saf" mean stress corrected stress amplitude
                "Sa" stress amplitude
                "Sm" mean stress
            The dictionary keys are strings and values floats
    """

    result_dict = {}
    for id_, stress_history in stress_history_dict.items():

        # Equivalent stress
        stress_amplitude, mean_stress = calculate_equivalent_tresca(stress_history)

        # Mean stress correction is ignored for shear criterion like tresca
        # Shear fatigue limit is used instead
        stress_amplitudef = material_dict["tR1"]
        if stress_amplitude == 0:
            safety_factor = stress_amplitudef / 1e-9
        else:
            safety_factor = stress_amplitudef / stress_amplitude

        result_dict[id_] = {"SF": safety_factor,
                           "Saf":stress_amplitudef,
                           "Sa":stress_amplitude,
                           "Sm": mean_stress}
    return result_dict


def calculate_mises_sf(stress_history_dict: dict, material_dict: dict, msc):
    """ Calculates safety factor based on material values and stress history
        for all nodes in the stress_history_dict using provided mean stress correction msc

        Note! Goodman mean stress correction needs only fR1 and Rm

    Parameters
    ----------
        stress_history_dict: dict
            Stress history for every node. The node is the key in the dict
            and value is list of stress tensors as history.
        material_dict: dict:
            Material parameters as dictionary for example [example units]:
                "fR1" : fatigue limit for fully alternating loading R=-1 [MPa]
                "fR0" : fatigue limit for pulsating loading R=0 [MPa]
                "Rm" : ultimate strenght (for tension) [MPa]
                "Rp02" : Relatively limit 0.2 % for tension [MPa]
                "Rmc" : Ultimate strenght for compresion [MPa]
                "Rp02c" : Relatively limit 0.2 % for compression [MPa]
        msc: func
            Function for mean stress correction

    Returns
    -------
        result_dict: dict
            Dictionary with results:
                "SF" safety factor
                "Saf" mean stress corrected stress amplitude
                "Sa" stress amplitude
                "Sm" mean stress
            The dictionary keys are strings and values floats
    """

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
