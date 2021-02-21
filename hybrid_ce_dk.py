from typing import Tuple

import numpy
import h5py
from matplotlib import pyplot


def compute_dk(
    ref: h5py.Group,
    act: h5py.Group,
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    rdays = ref["days"]
    adays = act["days"]
    akeff = act["keff"]
    if numpy.isnan(akeff).any():
        mask = act["hfFlags"][:]
        adays = adays[mask]
        akeff = akeff[mask]
    ix = numpy.searchsorted(rdays, adays)
    delta = numpy.divide(akeff, ref["keff"][ix])
    delta -= 1
    delta *= 1e5
    return adays[:], delta


def main() -> pyplot.Figure:
    fig, axes = pyplot.subplots(1, 2, sharex=True, sharey=False, figsize=(8, 3))

    with h5py.File("./data.h5", "r") as data:
        rgroup = data["reference/serpent"]
        for ax, agroup, title in zip(
            axes,
            ("/hybrid/{step}/", "/serpent/ce/{step}/"),
            ("Hybrid", "Predictor"),
        ):
            for step, mark in zip(
                (5, 10),
                ("o", "x"),
            ):
                days, dk = compute_dk(rgroup, data[agroup.format(step=step)])
                ax.plot(days, dk, marker=mark, linestyle="", label=step)
            ax.set(
                xlabel="Time [d]",
                ylabel=r"$\Delta k$ [pcm]",
                title=title,
            )
    axes[1].legend(title="Time step [d]")
    return fig


if __name__ == "__main__":
    import sys

    fig = main()
    if len(sys.argv) == 1:
        pyplot.show()
    else:
        fig.savefig(sys.argv[1])
