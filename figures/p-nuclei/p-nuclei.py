from iniabu import ini
import matplotlib.pyplot as plt
import numpy as np

# p-nuclei
nuc_names = [
    "Se-74",
    "Kr-78",
    "Sr-84",
    "Mo-92",
    "Mo-94",
    "Ru-96",
    "Ru-98",
    "Pd-102",
    "Cd-106",
    "Cd-108",
    "Sn-112",
    "Sn-114",
    "Te-120",
    "Xe-124",
    "Xe-126",
    "Ba-130",
    "Ba-132",
    "Ce-136",
    "Ce-138",
    "Sm-144",
    "Dy-156",
    "Dy-158",
    "Er-162",
    "Yb-168",
    "Hf-174",
    "W-180",
    "Os-184",
    "Pt-190",
    "Hg-196",
]
iso_inst = ini.iso[nuc_names]

fig, ax = plt.subplots(1, 1)
fig.set_size_inches((8, 4))

xax = np.arange(len(nuc_names))
barwidth = 0.4
ax.bar(
    xax - barwidth / 2,
    iso_inst.abu_solar / np.sum(iso_inst.abu_solar),
    width=barwidth,
    label="Fraction of solar $p$-nuclei",
)
ax.bar(
    xax + barwidth / 2,
    iso_inst.abu_rel,
    width=barwidth,
    label="Fraction of isotope with respect to element",
)
# ax.semilogy()

# create axis labels
nuc_names_fmt = [
    f"$^{{{it.split('-')[1]}}}\\mathrm{{{it.split('-')[0]}}}$" for it in nuc_names
]
ax.set_xticks(xax)
ax.set_xticklabels(nuc_names_fmt, rotation=90)

# labels, etc.
ax.legend()
ax.set_xlabel("$p$-nuclei")
ax.set_ylabel("Relative abundance")

fig.tight_layout()

# fig.show()
fig.savefig("p-nuclei.pdf")
