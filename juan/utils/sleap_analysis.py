import h5py
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


## Sleap exports a h5 file.
## Here we open it and print some of the datasets features
def open_sleap_h5(filename):
    with h5py.File(filename, "r") as handle:
        dset_names = list(handle.keys())
        locations = handle["tracks"][:].T
        node_names = [n.decode() for n in handle["node_names"][:]]

    print("===filename===")
    print(filename)
    print()

    print("===HDF5 datasets===")
    print(dset_names)
    print()

    print("===locations data shape===")
    print(locations.shape)
    print()

    print("===nodes===")
    for frame, name in enumerate(node_names):
        print(f"{frame}: {name}")
    print()

    return locations


## This is through a lineal model replace the missing values
## missing values are instances not predicted by SLEAP
def fill_missing(Y, kind="linear"):
    """Fills missing values independently along each dimension after the first."""

    # Store initial shape.
    initial_shape = Y.shape

    # Flatten after first dim.
    Y = Y.reshape((initial_shape[0], -1))

    # Interpolate along each slice.
    for frame in range(Y.shape[-1]):
        y = Y[:, frame]

        # Build interpolant.
        x = np.flatnonzero(~np.isnan(y))
        handle = interp1d(x, y[x], kind=kind, fill_value=np.nan, bounds_error=False)

        # Fill missing
        xq = np.flatnonzero(np.isnan(y))
        y[xq] = handle(xq)

        # Fill leading or trailing NaNs with the nearest non-NaN values
        mask = np.isnan(y)
        y[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), y[~mask])

        # Save slice
        Y[:, frame] = y

    # Restore to initial shape.
    Y = Y.reshape(initial_shape)

    return Y


def animacion_mice(locations):
    ## Nodes
    ## array structure:
    # [Frames, Nodes, x/y coord, number animals ]
    HEAD_INDEX = 0
    BODY_INDEX = 1
    TAIL_INDEX = 2

    head_loc = locations[:, HEAD_INDEX, :, :]
    body_loc = locations[:, BODY_INDEX, :, :]
    tail_loc = locations[:, TAIL_INDEX, :, :]
    fig, ax = plt.subplots(figsize=(10, 4))
    head = ax.scatter(x=head_loc[0, 1], y=head_loc[0, 0])
    body = ax.scatter(x=body_loc[0, 1], y=body_loc[0, 0])
    tail = ax.scatter(x=tail_loc[0, 1], y=tail_loc[0, 0])
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 800)
    ax.legend([head, body, tail], ["head", "body", "tail"])
    # ax.invert_xaxis()
    # ax.invert_yaxis()

    def animate(frame):
        print("frames: ", frame)
        head.set_offsets((head_loc[frame, 1], head_loc[frame, 0]))
        body.set_offsets((body_loc[frame, 1], body_loc[frame, 0]))
        tail.set_offsets((tail_loc[frame, 1], tail_loc[frame, 0]))

        return (body,)

    ani = animation.FuncAnimation(
        fig, animate, repeat=True, frames=len(locations) - 1, interval=100
    )

    # To save the animation using Pillow as a gif
    # writer = animation.PillowWriter(fps=15,
    #                                 metadata=dict(artist='Me'),
    #                                 bitrate=1800)
    # ani.save('scatter.gif', writer=writer)

    plt.show()


locations = open_sleap_h5(
    "/Users/jjpc/Documents/SLEAP_data/coop026x027_20231016-1.simple.instance.2023-11-08.predictions.000_coop026x027_20231016-1.analysis.h5"
)
locations = fill_missing(locations)
animacion_mice(locations=locations[0:500])
