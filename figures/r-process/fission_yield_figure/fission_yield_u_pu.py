# read and plot fission yield from file
import matplotlib.pyplot as plt
import numpy as np


def fy_reader(fname):
    """Read fission yield and return as np.array

    :param fname: File name
    :type fname: str

    :return: fission yields as table: Z, A, FPS, YIELD, UNCERTAINTY
    :rtype: np.array
    """
    with open(fname, "r") as f:
        data_in = f.read().split("\n")

    # remove header
    data_in = data_in[1:]

    # create data array
    data = []
    for line in data_in:
        if line != "":
            data.append([float(it) for it in line.split()])

    if len(data[-1]) == 5:
        corr = 1
    else:
        corr = 0
    data_ret = np.zeros((2 * len(data) - corr, 5))
    # sort the data into return array
    for it in range(len(data)):
        for jt in range(5):
            data_ret[2 * it][jt] = data[it][jt]
            if it < len(data) - 1 or corr == 0:
                data_ret[2 * it + 1][jt] = data[it][jt + 5]

    return data_ret


def fy_of_a(data):
    """Return the fission yield as a function of mass number A, summed up!

    :param data: data array, as returned from fy_reader
    :type data: ndarray

    :return: A, FY
    :rtype: ndarray, ndarray
    """
    all_a = data.transpose()[1]
    all_fy = data.transpose()[3]

    a_vec = np.arange(all_a.min(), all_a.max() + 1, dtype=int)
    a_fy = np.zeros_like(a_vec, dtype=float)

    for it, aval in enumerate(all_a):
        ind_new = int(aval - all_a.min())
        a_fy[ind_new] += all_fy[it]

    # norm a_fy
    a_fy /= np.sum(a_fy) / 2

    return a_vec, a_fy


# setup file names, etc.
fnames = ("fy_u235_thermal.txt", "fy_pu239_thermal.txt")
labels = ("$^{235}$U", "$^{239}$Pu")
line_styles = ("-", "--", ":")

# make the plot
fig, ax = plt.subplots(1, 1)
fig.set_size_inches((6, 4))

for it, fname in enumerate(fnames):
    data = fy_reader(fname)
    xdat, ydat = fy_of_a(data)
    ax.plot(xdat, ydat, linestyle=line_styles[it], label=labels[it])

# make y log
ax.semilogy()

ax.legend()
ax.set_xlabel("Mass Number ($A$)")
ax.set_ylabel("Relative Fission Yield")

fig.text(0.18, 0.2, "Thermal neutrons", ha="left")

fig.tight_layout()
# fig.show()
fig.savefig("fission_yield_thermal_u_pu.pdf")
