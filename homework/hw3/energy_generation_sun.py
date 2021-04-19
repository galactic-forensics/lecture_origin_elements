"""Graph the energies that are gained in pp-chain and CNO cycle as functions
of the stellar temperature."""

from iniabu import inimf
from matplotlib import pyplot as plt
import numpy as np

RHO = 150000  # assume fixed density, good for Sun
H_ABU = inimf.ele["H"].abu_solar


def epsilon_pp(temp: float) -> float:
    """Calculate energy generation rate in W/kg (at fixed density) in pp-chain

    :param temp: Temperature (T6)
    :type temp: float

    :return: Energy generation rate in W/kg
    :rtype: float
    """
    eps = 0.241 * RHO * H_ABU ** 2 * temp ** (-2 / 3) * np.exp(-33.8 * temp ** (-1 / 3))
    return eps


def epsilon_cno(temp: float) -> float:
    """Calculate energy generation rate in W/kg (at fixed density) for CNO cycle

    :param temp: Temperature (T6)
    :type temp: float

    :return: Energy generation rate in W/kg
    :rtype: float
    """
    cno_abu = np.sum(inimf.ele[["C", "N", "O"]].abu_solar)
    eps = (
        8.67e20
        * RHO
        * H_ABU
        * cno_abu
        * temp ** (-2 / 3)
        * np.exp(-152.28 * temp ** (-1 / 3))
    )
    return eps


def epsilon_3a(temp: float) -> float:
    """Calculate energy generation rate in W/kg (at fixed density) for Salpeter

    :param temp: Temperature (T6)
    :type temp: float

    :return: Energy generation rate in W/kg
    :rtype: float
    """
    he_abu = inimf.ele["He"].abu_solar
    temp8 = temp / 100  # need T8, not T6
    eps = (
        50.9 * RHO ** 2 * he_abu ** 3 * temp8 ** (-3) * np.exp(-44.027 * temp8 ** (-1))
    )
    return eps


# PLOT
fig, ax = plt.subplots(1, 1)
fig.set_size_inches((6, 4))

# temperature in T6
dtemp = 0.1
temp = np.arange(5, 1000 + dtemp, dtemp)

# epsilon over rho
eps_pp = epsilon_pp(temp)
eps_cno = epsilon_cno(temp)
eps_3a = epsilon_3a(temp)

ax.loglog(temp, eps_pp, label="pp-chain")
ax.loglog(temp, eps_cno, linestyle="dashed", label="CNO cycle")
ax.loglog(temp, eps_3a, linestyle="dashdot", label="3$\\alpha$")

# axes limits
ylims = np.min(eps_pp), np.max(eps_cno)
ax.set_ylim(ylims)

ax.set_xlabel("Temperature ($T_6$)")
ax.set_ylabel("Energy generation rate (W kg$^{-1}$)")

# vertical axes for Sun
ax.vlines(15, ylims[0], ylims[1], linestyle="dotted", color="k")
ax.text(1.02 * 15, 2 * ylims[0], "Sun", rotation=90)

# rho label:
ax.text(0.98 * ax.get_xlim()[1], 2 * ylims[0], "$\\rho$ = 150 g cm$^{-3}$", ha="right")

ax.legend()

fig.tight_layout()

# fig.show()
plt.savefig("energy_generation_sun.pdf")
