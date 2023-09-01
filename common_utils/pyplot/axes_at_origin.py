from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.ticker import MaxNLocator
import numpy as np


class _CustomTickLocator(MaxNLocator):
    """
    Similar to matplotlib's AutoLocator
    (https://matplotlib.org/3.7.1/api/ticker_api.html#matplotlib.ticker.AutoLocator),
    but hides the ticks at (0, 0).
    """

    def __init__(self):
        # same as AutoLocator
        super().__init__(nbins="auto", steps=[1, 2, 2.5, 5, 10])

    def tick_values(self, vmin: float, vmax: float) -> np.ndarray:
        tick_locations = super().tick_values(vmin, vmax)
        # remove the tick at location 0
        tick_locations = tick_locations[tick_locations != 0]
        return tick_locations


def configure_axes_at_origin(ax: Axes, axes_behind_data: bool = True):
    """
    Instead of drawing a box around the plot, this configures the axes to be drawn through (0, 0).

    # Parameters

    - `ax`: The axes to be modified
    - `axes_behind_data`: If `True`, the axes are drawn behind the rest of the plot
    """

    # ticks are on both sides of the axis (instead of just below or just left of the axis)
    rc = {
        "xtick.direction": "inout",
        "ytick.direction": "inout",
        "xtick.major.size" : 5,
        "ytick.major.size" : 5,
    }

    with plt.rc_context(rc):
        # move axes to the center passing through (0, 0)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")

        if axes_behind_data:
            # draw the axes behind the rest of the plot
            # ax.set_axisbelow(True)  # this doesn't work for some reason
            for spine in ax.spines.values():
                spine.set_zorder(-1)

        # source: https://matplotlib.org/3.3.4/gallery/recipes/centered_spines_with_arrows.html
        # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
        # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
        # respectively) and the other one (1) is an axes coordinate (i.e., at the very
        # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
        # actually spills out of the axes.
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

        # remove ticks at (0, 0)
        ax.xaxis.set_major_locator(_CustomTickLocator())
        ax.yaxis.set_major_locator(_CustomTickLocator())
