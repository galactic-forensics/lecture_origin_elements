"""Plot the Planck radiation

Demonstrate that deuterium cannot form after neutron/proton ratio is frozen
out after the Big Bang
"""

from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy import constants as const


def planck(freq: float, temp: float) -> float:
    """Return spectral radiance for given frequency and temperature.

    :param freq: Frequency in Hz
    :type freq: float
    :param temp: Temperature in Kelvin
    :type temp: float

    :return: Spectral radiance in mks units
    :rtype: float
    """
    return ((2 * const.h * freq ** 3) / const.c ** 2) * (
        1 / (np.exp((const.h * freq) / (const.k * temp)) - 1)
    )


def plot_planck_curve(
    ax, temp: float, freq_range: Tuple[float, float], points=10000, **kwargs
) -> None:
    """Plot Planck curve on a given axis.

    Additional keyword arguments for the matplotlib plotting routine can be
    passes as fit.

    :param ax: Axis to plot on
    :type ax: matplotlib.Axis
    :param temp: Temperature in Kelvin
    :type temp: float
    :param freq_range: Lower and upper frequency range to plot for
    :type freq_range: Tuple(float, float)
    :param points: Number of points to plot (defaults to 10000)
    :type points: int
    """
    xvals = np.linspace(freq_range[0], freq_range[1], num=points)
    yvals = planck(xvals, temp)
    ax.loglog(xvals, yvals, **kwargs)


def freq_to_mev(freq: float) -> float:
    """Convert frequency to energy.

    :param freq: Frequency in Hz
    :type freq: float

    :return: Energy in MeV
    :rtype: float
    """
    energy_joules = const.h * freq
    return energy_joules / const.e / 1e6


def mev_to_freq(energy: float) -> float:
    """Convert energy to frequency.

    :param energy: Energy in MeV
    :type energy: float

    :return: Frequency in Hz
    :rtype: float
    """
    energy_joules = energy * 1e6 * const.e
    return energy_joules / const.h


# Make the figure
fig, ax = plt.subplots(1, 1)
fig.set_size_inches((4, 4))

# define plot ranges
freq_range = (1e18, 5e21)
y_range = (1e-10, 1e12)

# Plot the Planck curves
plot_planck_curve(ax, 5e9, freq_range, label="$T_{9} = 5$")
plot_planck_curve(ax, 1e9, freq_range, label="$T_{9} = 1$", linestyle="dashed")

# plot binding energy line for deuterium
ax.vlines(
    mev_to_freq(2.2225),
    ymin=y_range[0],
    ymax=y_range[1],
    color="k",
    linestyle="dotted",
    label="D binding energy",
)

# limits
ax.set_xlim(freq_range)
ax.set_ylim(y_range)

# second axis with energy
secax = ax.secondary_xaxis("top", functions=(freq_to_mev, mev_to_freq))

# Labels
ax.set_xlabel("Frequency (Hz)")
secax.set_xlabel("Energy (MeV)")
ax.set_ylabel("Radiance (W sr$^{-1}$ m$^{-2}$ Hz$^{-1}$)")
ax.legend(loc="lower left")

# Layout
fig.tight_layout()

# Save or show
fig.savefig("planck_radiation_bbn.pdf")
# fig.show()
