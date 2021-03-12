"""Plot local approximation for tellurium isotopes."""

from iniabu import ini
import matplotlib.pyplot as plt
import numpy as np


# MACS at 30keV for all stable Te isotopes from KADoNiS v0.3 in mb
te_macs = np.array([538, 295, 832, 155, 431, 81.3, 44.4, 14.7])

# load Te isotopes from ini
te_isos = ini.iso["Te"]

# labels for Te production
te_labels = ("p", "s", "s", "s", "s,r", "s,r", "r", "r")

# Make solar_abundance*macs vs. mass plot
xdata = te_isos.mass
ydata = te_isos.abu_solar * te_macs

fig, ax = plt.subplots(1, 1)
fig.set_size_inches((6, 4))
ax.plot(xdata, ydata, "o")

# labels
for it in range(len(xdata)):
    xdat = xdata[it]
    ydat = ydata[it]
    lbl = te_labels[it]
    ax.text(xdat + 0.2, ydat + 2, lbl)

# nicer ticks
fancy_xticks = [f"$^{{{int(np.round(m,0))}}}$Te" for m in te_isos.mass]
ax.set_xticks(te_isos.mass)
ax.set_xticklabels(fancy_xticks)

# bar at constant values
avg_const = np.average(ydata[1:4])
ax.hlines(avg_const, xmin=122, xmax=124, color="k", linestyle="dashed")

# axes labels
ax.set_ylabel("$\\langle \\sigma \\rangle_{A} N_\\odot(A)$ [mb ($10^6$ Si)]$^{-1}$")

fig.tight_layout()
# fig.show()
fig.savefig("local_approx.pdf")
