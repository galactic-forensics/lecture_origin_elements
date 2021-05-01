"""Plot SLR initial abundance with respect to half-life"""

import matplotlib.pyplot as plt
import numpy as np


def read_data(fname="slr_initial_abundances.csv"):
    """Read in data file.

    :param fname: file name and path
    :type fname: str

    :return: Isotope Name, Half-life (Ma), Initial Abundance,
            Uncertainty
    :rtype: list, ndarray, ndarray, ndarray
    """
    data = []
    with open(fname, "r") as f:
        for line in f:
            data.append(np.array(line.rstrip().split(",")))
    # initialize return stuff
    name = []
    half_life = np.empty(len(data) - 1)
    abu = np.empty_like(half_life)
    abu_unc = np.empty_like(half_life)

    for it in range(1, len(data)):
        line = data[it]
        name.append([line[0], line[1]])
        half_life[it - 1] = float(line[2])
        abu[it - 1] = float(line[3])
        abu_unc[it - 1] = float(line[4])
    return name, half_life, abu, abu_unc


def iso_splitter(iso):
    """Split isotope by mass number and name.

    :param iso: isotope as one string
    :type iso: str

    :return: mass number, isotope name
    :rtype: list(int, str)
    """
    ind = len(iso)
    while ind > 0:
        try:
            int(iso[:ind])
            break
        except ValueError:
            ind -= 1
    return int(iso[:ind]), iso[ind:]


def iso_formatter(iso, menv=True):
    """Format isotope as TeX string.

    :param iso: isotope, e.g., "129I"
    :type iso: str
    :param menv: add $ for math environment? Default: True
    :type menv: bool

    :return: isotope formatted as TeX string
    :rtype: str
    """
    sp = iso_splitter(iso)
    tmp = f"^{{{sp[0]}}}\\mathrm{{{sp[1]}}}"
    if menv:
        return f"${tmp}$"
    else:
        return tmp


def isoratio_formatter(nom, denom):
    """Format isotope ratio as TeX.

    :param nom: nominator isotope
    :type nom: str
    :param denom: denominator isotope
    :type denom: str

    :return: formatted string with isotope ratio as frac
    :rtype: str
    """
    rstr = f"$\\frac{{{iso_formatter(nom, menv=False)}}}{{{iso_formatter(denom,menv=False)}}}$"
    return rstr


labels, half_lifes, abus, abus_unc = read_data()

# make the figure
fig, ax = plt.subplots(1, 1)
fig.set_size_inches((6, 4))

ax.loglog(half_lifes, abus, "o", mew="1.5", mfc="w")
ax.errorbar(
    half_lifes, abus, yerr=abus_unc, linestyle="none", color="tab:blue", linewidth=0.5
)
for it in range(len(abus)):
    xpt = 1.1 * half_lifes[it]
    ypt = abus[it]
    lbl = isoratio_formatter(labels[it][0], labels[it][1])
    if it % 2 == 0:
        ypt *= 1.2
    else:
        ypt *= 0.3
    ax.text(xpt, ypt, lbl)

ax.set_xlim(right=ax.get_xlim()[1] * 2)
ax.set_ylim(top=ax.get_ylim()[1] * 2)

ax.set_xlabel("Half life (Ma)")
ax.set_ylabel("Solar System initial ratio")

fig.tight_layout()
# fig.show()
fig.savefig("slr_initial_abundances.pdf")
