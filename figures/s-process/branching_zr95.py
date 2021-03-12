"""Calculate branching ratio at Zr95"""

import matplotlib.pyplot as plt
import numpy as np


# constants
MNEUTRON = 1.674927471e-24  # neutron mass in g
KB = 1.38064852e-16  # boltzmann constant in erg / K
LAMDA_ZR95 = [[1.25e-7]]  # decay constant for Zr95 (not temperature dependent)
MACS_ZR95 = 79e-27  # MACS of Zr95 in cm^2
TEMP = 1.0  # Temperature in C13 pocket in T8

# thermal speed
vth = np.sqrt(2.0 * KB * TEMP * 1e8 / MNEUTRON)


def calc_branching_ratio(nn: float) -> float:
    """Calculate branching ratio at given temperature

    :param nn: neutron number density in cm^-3
    :type nn: float, np.array

    :return: branching ratio
    :rtype: float
    """
    lambda_n = nn * MACS_ZR95 * vth
    lambda_b = LAMDA_ZR95
    bratio = lambda_n / (lambda_b + lambda_n)
    if isinstance(nn, np.ndarray):
        bratio = bratio[0]
    return bratio


# make plot
xlim_exp = (5, 12)
nn_range = np.logspace(xlim_exp[0], xlim_exp[1], 100)

fig, ax = plt.subplots(1, 1)
fig.set_size_inches((6, 4))

ax.semilogx(nn_range, calc_branching_ratio(nn_range), "-", label="$f_n$ at $T_8=1$")

ax.vlines(1e7, 0, 1, linestyles="dotted", color="k", label="$^{13}$C pocket")
ax.vlines(
    5e9, 0, 1, linestyles="solid", color="k", label="$^{22}$Ne$(\\alpha, n){^{25}}$Mg"
)

ax.legend()

ax.set_xlabel("Neutron density (cm$^{-3}$)")
ax.set_ylabel("Branching ratio $f_n$")

# limits
ax.set_xlim(10 ** np.array(xlim_exp))
ax.set_ylim((0, 1))


fig.tight_layout()
# fig.show()
fig.savefig("branching_zr95.pdf")
