from math import log, exp

# Eyring-Polanyi equation: k_off = (kappa*kB*T/h) * exp(-dGrevbarr/(R*T))
kappa = 1  # Transmission coefficient, reflects fraction of flux through TSS proceeds to P without recrossing TSS
# (Assumes that the no-recrossing assumption of TST holds perfectly)
kB = 1.380649 * 10 ** -23  # Boltzmann constant, relates avg relative KE of particles (g) with T [J/K]
h = 6.62607015 * 10 ** -34  # Planck's constant, relates photon E to its f, quantum of electromagnetic action [Js]
R = 8.314462618  # Ideal gas constant, equivalent to kB, but expressed in per mole [J/molK]
cal2J = 4.184


def energyUnitsConversion(E_kcal, E_kJ, verbose=False):
    """Convert between kcal and kJ.

    Parameters
    ----------
    E_kcal : Union[float,bool]
        Energy (kcal).
    E_kJ : Union[float,bool]
        Energy (kJ).
    verbose : bool
        Whether to display details.

    Returns
    -------
    E_kcal : float
        Energy (kcal).
    E_kJ : float
        Energy (kJ).

    Examples
    --------
    >>> energyUnitsConversion(100, False, True)
    """
    if not(E_kcal):  # If no value is provided
        E_kcal = E_kJ/cal2J
    elif not(E_kJ):
        E_kJ = E_kcal*cal2J
    else:
        raise Exception("Both E_kcal & E_kJ are missing! Provide one.")
    if verbose:
        print("E_kcal =", E_kcal, "kcal/mol, E_kJ =", E_kJ, "kJ/mol")
    return E_kcal, E_kJ


def eyringEquation(k, dGbarr, T, verbose=False):
    """Calculate off rate or elimination barrier from each other at a specific temperature using Eyring-Polanyi equation.

    Parameters
    ----------
    k : Union[float,bool]
        Off rate (s^-1).
    dGbarr : Union[float,bool]
        Elimination barrier (kcal/mol).
    T : float
        Temperature (K)
    verbose : bool
        Whether to display details.

    Returns
    -------
    k : float
        Off rate (s^-1).
    dGbarr : float
        Elimination (kcal/mol).

    Examples
    --------
    >>> eyring(None, 4.5, 300, True)
    """
    if not(k):  # If no value is provided
        print("\n--------------------------------------\n\n# Converting energy unit...")
        E_kcal, dGbarr = E_unit_conv(dGbarr, None)  # Convert to kJ/mol [kcal/mol], [kJ/mol]
        dGbarr *= 1000  # Convert to J/mol
        k = (kappa*kB*T/h) * exp(-dGbarr/(R*T))  # Calculate off rate
    elif not(dGbarr):
        dGbarr = -R*T*log(h*k/(kappa*kB*T))
    else:
        raise Exception("Both k & dGbarr are missing! Provide one.")
    dGbarr /= cal2J*1000  # Convert to kcal/mol
    if verbose:
        print("\n--------------------------------------\n\n# Using Eyring-Polanyi equation...")
        print("At T =", T, "K, k =", k, "s^-1, dGbarr =", dGbarr, "kcal/mol")
    return k, dGbarr


def timeUnitsConversion(k, t_half, RT, verbose=False):
    """Interconvert between off rate (s^-1), half life (s), and residence time (s).

    Parameters
    ----------
    k : Union[float,bool]
        Off rate (s^-1).
    t_hald : Union[float,bool]
        Half life (s).
    RT : Union[float,bool]
        Residence time (s)
    verbose : bool
        Whether to display details.

    Returns
    -------
    k : float
        Off rate (s^-1).
    t_hald : float
        Half life (s).
    RT : float
        Residence time (s).

    Examples
    --------
    >>> exp_time(None, 30.8, None, True)
    """
    if k:  # If value is provided
        t_half, RT = log(2)/k, 1/k
    elif t_half:
        k, RT = log(2)/t_half, t_half/log(2)
    elif RT:
        k, t_half = 1/RT, RT*log(2)
    else:
        raise Exception("All parameters are missing! Provide one.")
    if verbose:
        print("\n--------------------------------------\n\n# Kinetic parameters conversion...")
        print("k =", k, "s^-1, t_half =", t_half, "s, RT =", RT, "s")
    return k, t_half, RT


if __name__ == "__main__":
    T = 310.15  # Temperature, assumes RT at the moment [K]
    k, dGbarr = None, 30.8  # off rate [s^-1], elimination barrier [kcal/mol]
    t_half, RT = None, None  # half_life [s], residence time [s]

    k, dGbarr = eyring(k, dGbarr, T, True)
    k, t_half, RT = exp_time(k, t_half, RT, True)

