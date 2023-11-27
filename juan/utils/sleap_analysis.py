# %%
import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


# %%
## Sleap exports a h5 file.
## Here we open it and print some of the datasets features
def open_sleap_h5(filename):
    with h5py.File(filename, "r") as handle:
        dset_names = list(handle.keys())
        locations_perf = handle["tracks"][:].T
        node_names = [n.decode() for n in handle["node_names"][:]]

    print("===filename===")
    print(filename)
    print()

    print("===HDF5 datasets===")
    print(dset_names)
    print()

    print("===locations_perf data shape===")
    print(locations_perf.shape)
    print()

    print("===nodes===")
    for i, name in enumerate(node_names):
        print(f"{i}: {name}")
    print()

    return locations_perf


# %%
## This is through a lineal model replace the missing values
## missing values are instances not predicted by SLEAP
def fill_missing(Y, kind="linear"):
    """Fills missing values independently along each dimension after the first."""

    # Store initial shape.
    initial_shape = Y.shape

    # Flatten after first dim.
    Y = Y.reshape((initial_shape[0], -1))

    # Interpolate along each slice.
    for i in range(Y.shape[-1]):
        y = Y[:, i]

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
        Y[:, i] = y

    # Restore to initial shape.
    Y = Y.reshape(initial_shape)

    return Y


# %%
locations_perf = open_sleap_h5(
    "/Users/jjpc/Documents/SLEAP_data/top-down/coop026x027_20231016-1.simple.instance.greedy.2023-11-15.predictions.000_coop026x027_20231016-1.analysis.h5"
)
locations_perf = fill_missing(locations_perf)
locations_solid = open_sleap_h5(
    "/Users/jjpc/Documents/SLEAP_data/top-down/coop026x027_20231017-1.simple.instance.greedy.2023-11-16.predictions.000_coop026x027_20231017-1.analysis.h5"
)
locations_solid = fill_missing(locations_solid)

# %%
## array structure:
# [Frames, Nodes, x/y coord, number animals ]
HEAD_INDEX = 0
BODY_INDEX = 1
TAIL_INDEX = 2

head_loc_perf = locations_perf[:, HEAD_INDEX, :, :]
body_loc_perf = locations_perf[:, BODY_INDEX, :, :]
tail_loc_perf = locations_perf[:, TAIL_INDEX, :, :]

head_loc_solid = locations_solid[:, HEAD_INDEX, :, :]
body_loc_solid = locations_solid[:, BODY_INDEX, :, :]
tail_loc_solid = locations_solid[:, TAIL_INDEX, :, :]

# %%
head_loc_perf[0]

# %%
## Get x position of the body
## Is it representing the pattern of synchronization?
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 4), sharex=True)

ax[0].set_title("Perforated")
ax[0].plot(body_loc_perf[10000:20000, 0, 0], label="mice-1-x")
ax[0].plot(body_loc_perf[10000:20000, 0, 1], label="mice-2-x")
ax[1].set_title("Solid")
ax[1].plot(body_loc_solid[10000:20000, 0, 0], label="mice-1-x")
ax[1].plot(body_loc_solid[10000:20000, 0, 1], label="mice-2-x")
plt.xlabel("Frames")
plt.ylabel("x coords")
plt.tight_layout()
# plt.plot(body_loc_perf[10000:20000,1,0] * -1, label='mice-1-y')
# plt.plot(body_loc_perf[10000:20000,1,1] * -1, label='mice-2-y')

# %%
## Get x position of the body
## Is it representing the pattern of synchronization?
plt.figure(figsize=(12, 4))

plt.plot(body_loc_solid[10000:20000, 0, 0], label="mice-1-x")
plt.plot(body_loc_solid[10000:20000, 0, 1], label="mice-2-x")
# plt.plot(body_loc_solid[10000:20000,1,0] * -1, label='mice-1-y')
# plt.plot(body_loc_solid[10000:20000,1,1] * -1, label='mice-2-y')
plt.xlabel("Frames")
plt.ylabel("x coords")
