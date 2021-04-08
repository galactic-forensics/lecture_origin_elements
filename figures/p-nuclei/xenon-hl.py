from iniabu import ini
import matplotlib.pyplot as plt
import numpy as np

# normalizing isotope
normiso_name = "Xe-132"
normiso_mass = ini.iso[normiso_name].mass

# solar isotope ratios and mass numbers (rounded numbers)
xe_mass_number = np.round(ini.iso["Xe"].mass, 0)
xe_solar = ini.iso_ratio("Xe", normiso_name)

# ratios take from Gilmour for Xe-HL
xe_hl = np.array([0.00833, 0.00564, 0.0905, 1.056, 0.1542, 0.8457, 1, 0.6356, 0.6991])
xe_hl_unc = np.array(
    [0.00009, 0.00008, 0.0006, 0.002, 0.0003, 0.0013, 0.0, 0.0013, 0.0]
)

# make the plot
fig, ax = plt.subplots(1, 1)
fig.set_size_inches((6, 4))

# plot the data
ax.axhline(1, linestyle="--", color="k", linewidth=0.75, label="solar")
ax.plot(xe_mass_number, xe_hl / xe_solar, "o--", ms=8, mfc="w", mew=2, label="Xe-HL")

# labels
ax.set_xlabel("Mass number of xenon isotope $i$")
ax.set_ylabel(
    "($^{i}$Xe/$^{132}$Xe)$_{\\mathrm{HL}}$ / ($^{i}$Xe/$^{132}$Xe)$_{\\odot}$"
)
ax.legend()
fig.tight_layout()

fig.show()
# fig.savefig("xenon-hl.pdf")
