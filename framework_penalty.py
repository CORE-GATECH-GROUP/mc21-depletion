import math
import sys

import numpy
import h5py
import pandas
from uncertainties import ufloat, UFloat

with h5py.File("./data.h5", mode="r") as data:
    cedata = []
    for step in [5, 10]:
        group = data[f"/serpent/ce/{step}"]
        cedata.extend(group["cpuTime"])

    hdata = []
    for step in [5, 10]:
        group = data[f"hybrid/{step}"]
        hdata.extend(group["cpuTime"][group["hfFlags"][:]])

    framework_time = numpy.multiply(2, data["reference/hybrid/cpuTime"])

cedata = numpy.array(cedata)
hdata = numpy.array(hdata)

times = pandas.Series(
    [
        ufloat(cedata.mean(), cedata.std()),
        ufloat(framework_time.mean(), framework_time.std()),
        ufloat(hdata.mean(), hdata.std()),
    ],
    index=["Base", "Depletion", "SFV"],
)
times *= 28 / (60 * 60)
times.name = "Time [CPU h]"
times.index.name = "Case"

penalties = times.copy()
penalties.name = "Penalty"
penalties["Base"] = numpy.nan
penalties["Depletion"] = times["Depletion"] / times["Base"] - 1
penalties["SFV"] = times["SFV"] / times["Depletion"] - 1

frame = pandas.concat([times, penalties], axis="columns")


def prefmt(u) -> float:
    if isinstance(u, UFloat):
        return u.n
    return u


if len(sys.argv) == 1:
    print(frame)
else:
    frame.applymap(prefmt).to_latex(sys.argv[1], float_format="%.4f", na_rep="-")
