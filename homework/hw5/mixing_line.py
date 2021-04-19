from iniabu import ini
import matplotlib.pyplot as plt
import numpy as np


zr92zr94_solar = ini.iso_ratio("Zr-92", "Zr-94")
zr96zr94_solar = ini.iso_ratio("Zr-96", "Zr-94")

# Lugaro values
lug_d92zr = -207
lug_d96zr = -937

# calculate lugaro ratios
lug_r92zr = (lug_d92zr / 1000 + 1) * zr92zr94_solar
lug_r96zr = (lug_d96zr / 1000 + 1) * zr96zr94_solar

# calculate contamination and thus final ratio
cont = np.arange(0, 1.01, 0.01)
ratio_92zr_mix = cont * zr92zr94_solar + (1 - cont) * lug_r92zr
ratio_96zr_mix = cont * zr96zr94_solar + (1 - cont) * lug_r96zr

# transfer to delta values
delta_92zr_mix = (ratio_92zr_mix / zr92zr94_solar - 1) * 1000
delta_96zr_mix = (ratio_96zr_mix / zr96zr94_solar - 1) * 1000

# create the figure
fig, ax = plt.subplots(1, 1)

ax.plot(lug_d96zr, lug_d92zr, "o", label="s-process")
ax.plot(delta_96zr_mix, delta_92zr_mix, "-", label="Mixing Line")
ax.plot(0, 0, "*", label="solar", ms=12)

# lines for 0, 0
ax.axhline(0, linestyle="dashed", linewidth=0.5, color="k")
ax.axvline(0, linestyle="dashed", linewidth=0.5, color="k")

# labels
ax.legend()
ax.set_xlabel("$\\delta^{96}\\mathrm{Zr}_{94}$   (‰)")
ax.set_ylabel("$\\delta^{92}\\mathrm{Zr}_{94}$   (‰)")

# fig.show()
fig.savefig("mixing_line.pdf")
