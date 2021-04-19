"""Plot local approximation for tellurium isotopes."""

from iniabu import ini
import matplotlib.pyplot as plt
import numpy as np


# MACS at 30keV for Xe-126, Xe-128, Xe-129, Xe-130 isotopes from KADoNiS v0.3 in mb
xe_macs = np.array([359, 262.5, 617, 132])

# load Xe isotopes from ini
xe_isos = ini.iso[["Xe-126", "Xe-128", "Xe-129", "Xe-130"]]

# labels for Te production
xe_labels = ("p", "s", "s,r", "s")

# Make solar_abundance*macs vs. mass plot
xdata = xe_isos.mass
ydata = xe_isos.abu_solar * xe_macs

fig, ax = plt.subplots(1, 1)
fig.set_size_inches((6, 4))
ax.plot(xdata, ydata, "o")

# labels
for it in range(len(xdata)):
    xdat = xdata[it]
    ydat = ydata[it]
    lbl = xe_labels[it]
    ax.text(xdat + 0.2, ydat + 2, lbl)

# nicer ticks
fancy_xticks = [f"$^{{{int(np.round(m,0))}}}$Xe" for m in xe_isos.mass]
ax.set_xticks(xe_isos.mass)
ax.set_xticklabels(fancy_xticks)

# bar at constant values
avg_const = np.average([ydata[1], ydata[3]])
ax.hlines(avg_const, xmin=128, xmax=130, color="k", linestyle="dashed")

# axes labels
ax.set_ylabel("$\\langle \\sigma \\rangle_{A} N_\\odot(A)$ [mb ($10^6$ Si)]$^{-1}$")

fig.tight_layout()
# fig.show()
fig.savefig("local_approx_xe.pdf")
