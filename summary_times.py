import sys
from contextlib import suppress

import numpy
import h5py
import pandas


FRAMEWORK_PENALTY = 1 / (1 + 1.08)


def get_serpent_time(g: h5py.Group) -> float:
    return numpy.sum(g["cpuTime"])


def get_hybrid_time(g: h5py.Group) -> float:
    times = g["cpuTime"][:]
    flags = g["hfFlags"][:]
    times[flags] *= FRAMEWORK_PENALTY
    return times.sum()


TIME_DATA = {}

with h5py.File("./data.h5", mode="r") as data:
    for step in [5, 10]:
        TIME_DATA["Predictor", step] = get_serpent_time(data[f"serpent/ce/{step}"])
    for step in [5, 10]:
        TIME_DATA["Hybrid", step] = get_hybrid_time(data[f"hybrid/{step}"])


times = pandas.Series(TIME_DATA, name="Time [CPU h]")
times.index.names = ["Scheme", "Step size [d]"]
times *= 28 / (60 * 60)

if len(sys.argv) == 1:
    print(times)
else:
    with suppress(ImportError):
        import warnings
        import tables

        warnings.filterwarnings("ignore", category=tables.NaturalNameWarning)
    times.to_hdf(sys.argv[1], "times")
