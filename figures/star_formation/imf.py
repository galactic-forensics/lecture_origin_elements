"""Figure showing Salpeter, Kroupa, and Chabrier IMFs"""

import matplotlib.pyplot as plt
import numpy as np


def create_kroupa(masses):
    """Create Kroupa IMF distribution

    :params masses: Masses to be calculated at
    :type masses: ndarray<float>

    :return: Mass function
    :rtype: ndarray<float>
    """
    out = np.zeros_like(masses)

    # constants
    c1 = 1
    c2 = 2 * c1
    c3 = 25 * c1

    # mass > 0.5
    ind_r1 = np.where(masses > 0.5)
    out[ind_r1] = c1 * masses[ind_r1] ** -2.3

    # 0.08 < mass <= 0.5
    ind_r2 = np.where(np.logical_and(masses <= 0.5, masses > 0.08))
    out[ind_r2] = c2 * masses[ind_r2] ** -1.3

    # mass <= 0.08
    ind_r3 = np.where(masses <= 0.08)
    out[ind_r3] = c3 * masses[ind_r3] ** -0.3

    return out


def create_chabrier(masses):
    """Create Chabrier IMF distribution

    :params masses: Masses to be calculated at
    :type masses: ndarray<float>

    :return: Mass function
    :rtype: ndarray<float>
    """
    out = np.zeros_like(masses)

    # constants
    c1 = 1
    c2 = 3.539 * c1

    # mass < 1
    ind_r1 = np.where(masses < 1.0)
    out[ind_r1] = (
        c2
        * masses[ind_r1] ** -1
        * np.exp(-((np.log10(masses[ind_r1] / 0.08)) ** 2) / 0.952)
    )
    # mass >= 1
    ind_r2 = np.where(masses >= 1)
    out[ind_r2] = c1 * masses[ind_r2] ** -2.3

    return out


# create masses logarithmically spaced
masses = np.logspace(-2, 2, 10000)

# calculate mass functions
salpeter_mf = masses ** -2.35
kroupa_mf = create_kroupa(masses)
chabrier_mf = create_chabrier(masses)

# Make the figure
fig, ax = plt.subplots(1, 1)
fig.set_size_inches((4, 4))
ax.loglog(masses, salpeter_mf, label="Salpeter (1955)")
ax.loglog(masses, kroupa_mf, linestyle="dashed", label="Kroupa (2001)")
ax.loglog(masses, chabrier_mf, linestyle="dotted", label="Chabrier (2003)")

# labels
ax.legend()
ax.set_xlabel("Mass ($M_\\odot$)")
ax.set_ylabel("Mass Function $\\xi(m)\\Delta m$")

# limits
ax.set_xlim((1e-2, 1e2))
ax.set_ylim((1e-4, 1e3))

fig.tight_layout()

# fig.show()
fig.savefig("imf.pdf")
