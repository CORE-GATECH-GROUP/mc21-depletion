from typing import Tuple, Union
import numpy
import h5py
from matplotlib import pyplot


def compute_axial_offset(
    group: h5py.Group,
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    days = group["days"][:]
    flux = group["flux"][:]
    break_ix = flux.shape[1] // 2
    upper = flux[:, break_ix:].sum(axis=1)
    ao = upper / flux.sum(axis=1)
    ao -= 0.5
    return days, ao


def main() -> pyplot.Figure:
    fig, axes = pyplot.subplots(2, 1, sharex=True, sharey=False, figsize=(8, 4))
    with h5py.File("./data.h5", "r") as data:
        for ax, agroup, title in zip(
            axes,
            ("/hybrid/{step}/", "/serpent/ce/{step}/"),
            ("Hybrid", "Predictor"),
        ):
            ax.axhline(0, color="k", linestyle="--", alpha=0.5)
            for (step,) in zip(
                (5, 10),
            ):
                days, ao = compute_axial_offset(data[agroup.format(step=step)])
                ax.plot(days, ao, label=step, drawstyle="steps-post")
            ax.set(
                ylabel="Axial offset",
                title=title,
            )
    axes[1].set_xlabel("Time [d]")
    axes[1].legend(title="Time step [d]", ncol=2, loc="lower left")
    return fig


if __name__ == "__main__":
    import sys

    fig = main()
    if len(sys.argv) == 1:
        pyplot.show()
    else:
        fig.savefig(sys.argv[1])
