#!/usr/bin/env python3

import numpy
from matplotlib import pyplot
import h5py

# Need one extra so that each node has upper and lower
# edges in the mesh plot. Avoids dropping the highest row
# Will do similar when updating the days
HEIGHTS = numpy.linspace(0, 360, 101)
UPPER = 311


def plot_flux(g: h5py.Group, ax: pyplot.Axes):
    dayvec = numpy.empty(g["days"].size + 1, dtype=g["days"].dtype)
    g["days"].read_direct(dayvec, dest_sel=numpy.s_[: dayvec.size - 1])
    dayvec[-1] = UPPER
    flux = numpy.divide(g["flux"], numpy.max(g["flux"]))
    ax.pcolormesh(dayvec, HEIGHTS, flux.T, rasterized=True)


def main() -> pyplot.Figure:
    fig, axes = pyplot.subplots(2, 2, sharex=True, sharey=True, figsize=(8, 4))
    with h5py.File("./data.h5", "r") as data:
        for col, title, fmt in zip(
            (axes[:, 0], axes[:, 1]),
            ("Hybrid", "Serpent predictor"),
            ("hybrid/{}", "serpent/ce/{}"),
        ):
            for step, ax in zip((5, 10), col):
                plot_flux(data[fmt.format(step)], ax)
                ax.set_title(f"{title} - {step} day step")
    axes[0, 0].set(
        ylabel="Axial height [cm]",
    )
    axes[1, 0].set(
        ylabel=axes[0, 0].get_ylabel(),
        xlabel="Time [d]",
    )
    axes[1, 1].set_xlabel(axes[1, 0].get_xlabel())

    return fig


if __name__ == "__main__":
    import sys

    fig = main()
    if len(sys.argv) == 1:
        pyplot.show()
    else:
        fig.savefig(sys.argv[1])
