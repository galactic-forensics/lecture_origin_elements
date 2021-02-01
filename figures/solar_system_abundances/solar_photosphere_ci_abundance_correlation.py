from iniabu import ini
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# COMPARISON PLOT CI CHONDRITES AND PHOTOSPHERE #

ini.database = "asplund09"
ele_names = list(ini.ele_dict.keys())
eles_asplund = ini.ele[ele_names]
abus_asplund = eles_asplund.abu_solar

# read CI abundance in ppm by weight (!)
ci_abu = pd.read_csv("ci_abus_lodders20.csv", index_col=0)
ci_ele_names = list(ci_abu["E"])
ci_abus_ppm = list(ci_abu["CI_ppm"])
ci_dict = dict(zip(ci_ele_names, ci_abus_ppm))

# drop elements with no stable nuclides -> not in `iniabu` tables!
ci_dict.pop("Tc")
ci_dict.pop("Pm")

# now calculate the number fraction of CI composition normalized to Si = 1e6
multiplier = 1e6 / ci_dict["Si"]
si_mass = ini.ele["Si"].mass
for ele in ci_dict.keys():
    ci_dict[ele] *= multiplier * si_mass / ini.ele[ele].mass

# create CI abus list depending on names
ci_abus = np.zeros_like(abus_asplund)
for it, ele in enumerate(ele_names):
    ci_abus[it] = ci_dict[ele]

fig, ax = plt.subplots(1, 1)
fig.set_size_inches((4, 4))

ax.set_xlabel("Photosphere abundances (Asplund et al., 2009)")
ax.set_ylabel("CI abundances (Lodders et al., 2020)")

ax.loglog(abus_asplund, ci_abus, "o", ms=4, mec="k", mew=0.5)

# define or get axes limits for data (xlim, ylim)
min_ax = 1e-4
max_ax = 5e11

# draw 1:1 correlation line
ax.plot(
    [min_ax, max_ax],
    [min_ax, max_ax],
    "-",
    color="k",
    linewidth=0.5,
    label="1:1 correlation",
)

# annotate elements of interest (outliers)
eles_to_annotate = ["Li", "Xe", "Kr", "Ar", "Ne", "He", "N", "C", "O", "H"]
for ele in eles_to_annotate:
    x_offset = 1.5
    y_offset = 0.9
    xy = (ini.ele[ele].abu_solar, ci_dict[ele])
    xy_offset = xy[0] * x_offset, xy[1] * y_offset
    ax.annotate(ele, xy, xy_offset)

# set y ticks the same as x ticks
ax_ticks = np.logspace(-4, 11, 6)
ax.set_xticks(ax_ticks)
ax.set_yticks(ax_ticks)

# apply xlim, ylim of data
ax.set_xlim(min_ax, max_ax)
ax.set_ylim(min_ax, max_ax)

# legend
ax.legend()

# set axes aspect ratio and layout
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig("solar_photosphere_ci_abundances_correlation.pdf")
# fig.show()
