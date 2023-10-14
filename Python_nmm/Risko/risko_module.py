"""
Created on Mon 30 Nov 12:15 2020
Finished on
@author: Παύλος Λοΐζου (nm16801)
                                  """
import numpy as np

""" Tables of probabilities for side damage """
Horizontal_Axis = np.arange(0, 1.05, 0.05)

# The probability the damage will lie entirely aft of location Xa/L
Psa = [i / 1000 for i in range(117, 1017, 50)]
Psa.insert(0, 0.068)
Psa.insert(0, 0.023)
Psa.insert(0, 0)

# The probability the damage will lie entirely forward of location Xf/L
Psf = Psa[:]
Psf.reverse()

# The probability the damage will lie entirely below the tank
Psl = [0, 0, 0.001, 0.003, 0.007, 0.013, 0.021, 0.034, 0.055, 0.085, 0.123,
       0.172, 0.226, 0.285, 0.347, 0.413, 0.482, 0.553, 0.626, 0.7, 0.775]

# The probability the damage will lie entirely above the tank
Psu = np.array([968, 952, 931, 905, 873, 836, 789, 733, 670, 599, 525, 452, 383,
                317, 255, 197, 143, 92, 46, 13, 0]) * (10 ** -3)

""" Tables of probabilities for bottom damage """
# The probability the damage will lie entirely aft of location Xa/L
Pba = np.array([0, 2, 8, 17, 29, 42, 58, 76, 96, 119, 143, 171, 203, 242,
                289, 344, 409, 482, 565, 658, 761]) * (10 ** -3)

# The probability the damage will lie entirely forward of location Xf/L
Pbf = np.array([969, 953, 936, 916, 894, 870, 842, 810, 775, 734, 687, 630, 563,
                489, 413, 333, 252, 170, 89, 26, 0]) * (10 ** -3)

# The probability the damage will lie entirely to port of the tank
Pbp = [0.884, 0.794, 0.744, 0.694, 0.644, 0.594, 0.544, 0.494, 0.444, 0.394, 0.344, 0.297,
       0.253, 0.211, 0.171, 0.133, 0.097, 0.063, 0.032, 0.009, 0]

# The probability the damage will lie entirely to starboard of the tank
Pbs = Pbp[:]
Pbs.reverse()


def regulation23(inputs: list, TankList: list):
    L, B, D, Z1, ds, ps, pn, C = inputs

    # Linear Interpolation Function
    def linearInterpolation(_xm: float, P_axis: list):
        for _i, _x in enumerate(Horizontal_Axis):
            if _x < _xm < Horizontal_Axis[_i + 1]:
                _x1 = _x
                _x2 = Horizontal_Axis[_i + 1]
                _p1 = P_axis[_i]
                _p2 = P_axis[_i + 1]
                _pm = _p1 + (_p2 - _p1) / (_x2 - _x1) * (_xm - _x1)
                break
            elif _xm == _x:
                _pm = P_axis[_i]
                break
        return _pm

    """ Calculating OMs (mean oil outflow for side damage) """

    # Function for calculating the side damage probability for a specific tank
    def calculatingPSi(_xa, _xf, _zl, _zu, _y):
        _Psf = linearInterpolation(_xf / L, Psf)
        _Psa = linearInterpolation(_xa / L, Psa)
        _Psu = linearInterpolation(_zu / D, Psu)
        _Psl = linearInterpolation(_zl / D, Psl)

        if _y / B <= 0.05:
            _Psy = (24.96 - 199.6 * _y / B) * (_y / B)
        elif 0.05 < _y / B < 0.1:
            _Psy = 0.749 + (5 - 44.4 * (_y / B - 0.05)) * (_y / B - 0.05)
        else:
            _Psy = 0.888 + 0.56 * (_y / B - 0.1)
        if _Psy > 1:
            _Psy = 1

        _PSL = 1 - _Psf - _Psa
        _PSV = 1 - _Psu - _Psl
        _PST = 1 - _Psy
        _PS = _PSL * _PSV * _PST

        return _PS

    C3 = 1  # Regulation 23.6
    OMs = 0
    n = len(TankList)
    for i in range(n):
        xai, xfi, zli, zui, ypi, ysi, tankB, Vi = TankList[i]
        PSi = calculatingPSi(xai, xfi, zli, zui, ysi)
        OMsi = PSi * Vi
        OMs += OMsi

    OMs *= C3

    """ Calculating OMb (mean oil outflow for bottom damage) """

    # Function for calculating the volume under tidal change circumstances
    def calculatingOB(_tc, _xa, _xf, _tankB, _Vi):
        p = 5  # inert gas overpressure in kPa
        hc = ((ds + _tc - Z1) * (ps * 1000) - 1000 * p / 9.81) / (pn * 1000)
        _x = _xf - _xa
        return _Vi - hc * _tankB * _x

    # Function for calculating the bottom damage probability for a specific tank
    def calculatingPBi(_xa, _xf, _ypi, _ysi):
        _Pbf = linearInterpolation(_xf / L, Pbf)
        _Pba = linearInterpolation(_xa / L, Pba)
        _Pbp = linearInterpolation(_ypi / B, Pbp)
        _Pbs = linearInterpolation(_ysi / B, Pbs)

        if Z1 / D <= 0.1:
            _Pbz = (14.5 - 67 * Z1 / D) * Z1 / D
        else:
            _Pbz = 0.78 + 1.1 * (Z1 / D - 0.1)

        if _Pbz > 1:
            _Pbz = 1

        _PBL = 1 - _Pbf - _Pba
        _PBT = 1 - _Pbp - _Pbs
        _PBV = 1 - _Pbz
        _PB = _PBL * _PBV * _PBT
        return _PB

    OMb_0 = 0
    OMb_25 = 0
    CDb = 0.6

    for i in range(n):
        xai, xfi, zli, zui, ypi, ysi, tankB, Vi = TankList[i]
        PBi = calculatingPBi(xai, xfi, ypi, ysi)
        # 0m tide
        Obi_0 = calculatingOB(0, xai, xfi, tankB, Vi)
        OMb_0 += CDb * PBi * Obi_0
        # 2.5m tide
        Obi_25 = calculatingOB(-2.5, xai, xfi, tankB, Vi)
        OMb_25 += CDb * PBi * Obi_25

    OMb = 0.7 * OMb_0 + 0.3 * OMb_25

    """ Calculating final mean Outflow (OM) and total Probability of mean outflow (PM) """
    OM = (0.4 * OMs + 0.6 * OMb) / C
    print(f"Mean Outflow: {OM}")

    return OM