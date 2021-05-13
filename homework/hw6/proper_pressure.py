import matplotlib.pyplot as plt
import numpy as np

# constants in mks
PRESSURE = 1e19
GRAV = 6.67408e-11
MSUN = 2e30
RSUN = 6.957e8

# white dwarf
rwd = 0.01 * RSUN


def maccr(mwd):
    """Calculate accreted mass for thermonuclear runaway based on white dwarf mass

    :param mwd: Mass of white dwarf in solar masses
    :type mwd: float

    :return: accreted total mass in solar masses
    :rtype: float
    """
    mret = PRESSURE * 4 * np.pi * rwd ** 4 / (GRAV * mwd * MSUN)
    return mret / MSUN


# make the figure
fig, ax = plt.subplots(1, 1)

xdat = np.arange(1, 1.401, 0.01)
ydat = maccr(xdat)

ax.plot(xdat, ydat, "-")
ax.set_xlabel("Mass of white dwarf ($M_\\odot$)")
ax.set_ylabel("$M_\\mathrm{accr}$ ($M_\\odot$)")
fig.tight_layout()
# fig.show()
fig.savefig("proper_pressure_figure_1a.pdf")

# question 1b
res1b = maccr(1.2)
print("\nQuestion 1b:\n")
print(f"Accreted mass of 1.2 $M_\\odot$ star for explosion: {res1b:.2e} M_\\odot")

# compare to solar density
vol_sun = 4 / 3 * np.pi * RSUN ** 3
vol_wd = 4 / 3 * np.pi * rwd ** 3
rho_sun = MSUN / vol_sun
rho_wd = 1.2 * MSUN / vol_wd
print(f"Density of WD as multiples of solar density: {rho_wd / rho_sun:.2e}")


# question 2
print("\n\nQuestion 2:\n")
print(f"Min time for recurring event: {res1b/10**(-11):.2e} a")
print(f"Max time for recurring event: {res1b/10**(-7):.2e} a")

print(
    "Recurring novae must happen in systems that have either higher mass accretion "
    "rates, or lower requried proper pressures."
)
