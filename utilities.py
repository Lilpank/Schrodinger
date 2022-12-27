from numba import njit, prange, float64, int64, jit
import math
import matplotlib.pyplot as plt
import numpy as np


@njit(nogil=True)
def u_potential(x):
    return -1 / (np.exp(x - 5) + 1)


@njit(nogil=True)
def f_potential(x):
    return -1 / (np.exp(x - 5) + 1)


@njit(nogil=True)
def oscillator(x):
    return 0.5 * np.power(x, 2)


def find_vector_value(e_min, e_max, h_energy, accuracy, b_coef, u, n, h):
    a = e_min
    vectors = np.array([])
    values = np.array([])
    indexes = np.array([])
    psi_temp = np.array([])
    discrepancy_temp = 1

    while a <= e_max:
        discrepancy, psi, m = shoot_method(b_coef, a, u, n, h)
        if discrepancy < accuracy:
            if discrepancy_temp > discrepancy:
                discrepancy_temp = discrepancy
                psi_temp = psi

        else:
            if len(psi_temp) != 0:
                values = np.append(values, a)
                indexes = np.append(indexes, m)
                if len(vectors) == 0:
                    vectors = np.array([psi_temp])
                else:
                    vectors = np.vstack((vectors, psi_temp))

                psi_temp = np.array([])
                discrepancy_temp = 1
        a += h_energy

    return vectors, values, indexes


@njit
def find_node(energy, n, u):
    i, m = 0, 0
    while i < n - 2:
        crossing_i_plus_1 = energy - u[i + 2]
        crossing_i = energy - u[i + 1]
        if crossing_i_plus_1 * crossing_i < 0:
            m = i + 2
            break
        i += 1
    return i, m


@njit
def shoot_method(b_coef: np.int64, energy: np.float64, u: np.array, n: np.int64, h: np.float64):
    i, m = find_node(energy, n, u)
    hi = np.zeros(n, dtype=np.float64)
    if i == n - 2:
        return np.float64(1), hi, np.int64(0)

    hi = np.zeros(n, dtype=np.float64)
    hi[1] = 10E-10
    i = 0
    while i < m - 1:
        second_derivative_hi_i = -b_coef * (energy - u[i]) * hi[i]
        hi[i + 2] = h ** 2 * second_derivative_hi_i + 2 * hi[i + 1] - hi[i]
        i += 1
    hi_left_i = hi[m]
    hi_left_i_minus_1 = hi[m - 1]

    hi[n - 2] = 10E-10
    i = n - 3
    while i >= m - 1:
        hi[i] = (2 * hi[i + 1] - hi[i + 2]) / (1 + h ** 2 * b_coef * (energy - u[i]))
        i -= 1
    hi_right_i = hi[m]
    hi_right_i_minus_1 = hi[m - 1]

    c = hi_left_i / hi_right_i
    hi_right_i_minus_1 *= c
    i = m - 1
    while i < n:
        hi[i] *= c
        i += 1

    psi_max = np.amax(np.abs(hi))
    discrepancy = np.abs(hi_left_i_minus_1 - hi_right_i_minus_1) / psi_max

    a = 0
    for i in range(n):
        a += h * hi[i] ** 2
    a = a ** (-0.5)
    hi *= a

    return np.float64(discrepancy), hi, np.int64(m)
