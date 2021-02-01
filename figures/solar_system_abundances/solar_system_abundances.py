from typing import Tuple

import iniabu
from iniabu import ini
import matplotlib.pyplot as plt


def annotation_offset_calc(
    xyc: Tuple[float, float],
    xyc_prev: Tuple[float, float],
    xyc_next: Tuple[float, float],
    xoffset: float,
    yoffset: float,
    logy=True,
) -> Tuple[float, float]:
    """Calculate the annotation offset for annotating an element.

    :param xyc: x and y coordinate of data point
    :type xyc: Tuple[float, float]
    :param xyc_prev: x and y coordinate of previous data point, None if N/A
    :type xyc_prev: Tuple[float, float]
    :param xyc_next: x and y coordinate of next data point, None if N/A
    :type xyc_next: Tuple[float, float]
    :param xoffset: Offset in x direction from
    :type xoffset: float
    :param yoffset: Offset in x direction from
    :type yoffset: float
    :param logy: Is the y axis logarithmic (default True)
    :type logy: bool

    :return: X and Y coordinate tuple where the label should be
    :rtype: Tuple[float, float]
    """
    any_none = True if xyc_prev is None or xyc_next is None else False
    if not any_none and xyc_prev[1] > xyc[1] and xyc_next[1] > xyc[1]:
        if logy:
            return xyc[0], xyc[1] / yoffset
        else:
            return xyc[0], xyc[1] - yoffset
    elif not any_none and xyc_prev[1] < xyc[1] and xyc_next[1] < xyc[1]:
        if logy:
            return xyc[0], xyc[1] * yoffset
        else:
            return xyc[0], xyc[1] + yoffset
    else:
        if logy:
            return xyc[0] + xoffset, xyc[1] * yoffset / 2
        else:
            return xyc[0] + xoffset, xyc[1] * yoffset / 2


# CREATE THE SOLAR ABUNDANCE FIGURE #

ini.database = "lodders09"

ele_names = list(ini.ele_dict.keys())
eles_lodders = ini.ele[ele_names]
proton_number = [iniabu.data.nist15.elements_z[ele] for ele in ele_names]
abus = eles_lodders.abu_solar

fig, ax = plt.subplots(1, 1)
fig.set_size_inches((8, 4))

ax.semilogy(proton_number, abus, "o-", ms=3, mec="k", mew=0.5, linewidth=0.5)

ax.set_xlabel("Number of protons Z")
ax.set_ylabel("Abundance (normed to Si=$10^{6}$)")
print(len(proton_number))
# write text next to all the elements
for it, xc in enumerate(proton_number):
    xyc = (xc, abus[it])
    lbl = ele_names[it]
    # prepare for offset calculation of annotation
    xyc_prev = None
    xyc_next = None
    if it < len(proton_number) - 1:
        xyc_next = (proton_number[it + 1], abus[it + 1])
    if it > 0:
        xyc_prev = (proton_number[it - 1], abus[it - 1])

    xyc_shifted = annotation_offset_calc(xyc, xyc_prev, xyc_next, 1.2, 2.25)
    ax.annotate(
        lbl,
        xyc_shifted,
        fontsize=6,
        horizontalalignment="center",
        verticalalignment="center",
    )

    ax.text(
        proton_number[-1],
        abus[0],
        "Lodders et al. (2009)",
        verticalalignment="top",
        horizontalalignment="right",
    )

fig.tight_layout()
fig.savefig("solar_system_abundances.pdf")
# fig.show()
