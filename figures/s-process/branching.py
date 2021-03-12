import numpy as np


class Branching:
    """
    Branching ratio class to calculate branching ratios
    Temperature shall be given throughout the class in T8
    """

    def __init__(self):
        # available isotopes, need to make sure that decay_const & macs is updated
        self.isos = ["Zr93", "Zr95", "W185"]
        self.isodict = dict(zip(self.isos, range(len(self.isos))))

        # constants
        self.mneutron = 1.674927471e-24  # neutron mass in g
        self.kboltz = 1.38064852e-16  # boltzmann constant in erg / K

    def decay_const(self, iso, temp, nele):
        """
        Returns decay constant in s^-1
        :return:    decay constant
        """
        # available temperatures and electron densities
        temp_av = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
        nele_av = [1.0, 3.0, 10.0, 30]

        # dictionaries
        isodict = self.isodict
        tmpdict = dict(zip(temp_av, range(len(temp_av))))
        neledict = dict(zip(nele_av, range(len(temp_av))))

        # data array
        # 1st layer: isotope
        # 2nd layer: temperature dependance (if length one: not dependent on T)
        # 3rd layer: electron density dependance (if length one: not dependent on n_ele)
        data = [
            # Zr93
            [
                [1.46e-14],
                [1.58e-14, 1.48e-14, 1.42e-14, 1.30e-14],
                [2.08e-14, 1.85e-14, 1.59e-14, 1.35e-14],
                [2.28e-14, 2.23e-14, 2.07e-14, 1.71e-14],
                [5.48e-14, 5.37e-14, 5.18e-14, 4.87e-14],
                [4.42e-13, 4.38e-13, 4.31e-13, 4.20e-13],
                [1.99e-12, 1.98e-12, 1.96e-12, 1.93e-12],
            ],
            # Zr95
            [[1.25e-7]],
            # W185
            [
                [1.07e-7],
                [1.18e-7, 1.18e-7, 1.18e-7, 1.16e-7],
                [1.20e-7, 1.19e-7, 1.16e-7, 1.16e-7],
                [1.58e-7, 1.35e-7, 1.19e-7, 1.10e-7],
                [1.84e-7, 1.74e-7, 1.51e-7, 1.25e-7],
                [1.95e-7, 1.88e-7, 1.78e-7, 1.57e-7],
                [2.05e-7, 2.02e-7, 1.96e-7, 1.82e-7],
            ],
        ]
        # get indexes
        # todo error catching on missing data entries
        isos_ind = isodict[iso]
        if len(data[isos_ind]) == 1:
            tmp_ind = 0
        else:
            tmp_ind = tmpdict[temp]
        if len(data[isos_ind][tmp_ind]) == 1:
            nele_ind = 0
        else:
            nele_ind = neledict[nele]

        return data[isos_ind][tmp_ind][nele_ind]

    def neutron_capture(self, na, iso, temp, macserr=None, cs=None):
        """
        Returns neutron capture rate dependent on neutron density, temperature, and maxwellian averaged cross section
        :param na:
        :param iso:
        :param temp:
        :param macserr:
        :param cs:
        :return:
        """
        # thermal energy
        if cs is None:
            readtmp = self.kadonisreader(iso)
        else:
            readtmp = [float(cs), 0.0]

        # thermal speed
        vth = np.sqrt(2.0 * self.kboltz * temp * 1e8 / self.mneutron)

        if macserr is "Min":
            macs = (readtmp[0] - readtmp[1]) * 1e-27
        elif macserr is "Max":
            macs = (readtmp[0] + readtmp[1]) * 1e-27
        else:
            macs = readtmp[0] * 1e-27  # in cm2

        return na * vth * macs

    def branching_ratio(self, na, iso, temp, nele, macserr=None, cs=None):
        """
        branching_ratio calculation
        :param na:
        :param iso:
        :param temp:
        :param nele:
        :param macserr:     Error from Kadonis, if 'Min', lower limit, if 'Max', upper limit
        :param cs:          Manual cross section: must be MACS @ 30keV. Kadonis is skipped
        :return:
        """
        lambda_n = self.neutron_capture(na, iso, temp, macserr=macserr, cs=cs)
        lambda_b = self.decay_const(iso, temp, nele)
        return lambda_n / (lambda_n + lambda_b)

    def kadonisreader(self, iso):
        """
        Returns maxwellian averaged cross section from iso input
        todo: incorporate full kadonis read
        :param iso:    isotope in standard form EleZZZ
        :return:       MACS from Kadonis, uncertainty
        """
        # all macs values
        macsvals = [[96.0, 9.0], [106.0, 26.0], [633.0, 142.0]]  # Zr93  # Zr95  # W185
        # todo: error catching
        return macsvals[self.isodict[iso]]
