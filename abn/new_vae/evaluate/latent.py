"""Provide summary plots with the results.

This file provides plots that can be generated during training
to evaluate the efficiency of the methods.
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # NOQA
import seaborn as sns
import pandas as pd
sns.set_style("darkgrid")

CMAP = {
    # Color maps for angles related to position
    "angles": "hsv",
    "angles_tracked": "twilight",
    # Color maps for angles related to head direction
    "angles_head": "hsv",
    "rx_head": "hsv",
    "ry_head": "hsv",
    "rz_head": "hsv",
    # Experiments
    "times": "winter",
    "gains": "cool",
    # Position color maps
    "velocities": "viridis",
    "radius2": "viridis",
    "x": "viridis",
    "y": "viridis",
    "z": "viridis",
    "scalars": "viridis",
    # Uncertainty / Success colormaps
    "var": "magma",
    "success": "afmhot",
    "kappa": "magma",
}
plt.rcParams.update({"figure.max_open_warning": 0})


def plot_save_latent_space(fname, z, labels):
    """Plot the data projected in the latent space.

    Parameters
    ----------
    fname : str
        Filename where to save the plot.
    points : array-like, shape=[n_samples, latent_dim]
        Points, typically corresponding to the means mus of the
        latent variables.
    labels : pd.DataFrame, shape=[n_samples, n_cols]
        Labels used to color the plotted points.
        The columns are the different labels
    """
    assert len(z) == len(labels)

    latent_dim = z.shape[-1]
    label_names = list(labels.columns)
    if "Unnamed: 0" in label_names:
        label_names.remove("Unnamed: 0")
    n_labels = len(label_names)
    nrows = 1
    ncols = n_labels // 2 + 1

    if latent_dim == 1:
        fig = plt.figure(figsize=(5 * ncols, 4 * nrows))
        for i, label_name in enumerate(label_names):
            ax = fig.add_subplot(nrows, ncols, i + 1)
            sc = ax.scatter(
                z[:, 0],
                np.ones(len(z[:, 0])),
                s=10,
                c=labels[label_name],
                cmap=CMAP[label_name],
            )
            ax.set_title(label_name, fontsize=30)
            fig.colorbar(sc, ax=ax)

    if latent_dim == 2:
        fig = plt.figure(figsize=(10 * ncols, 10 * nrows))
        for i, label_name in enumerate(label_names):
            # ax = fig.add_subplot(nrows, ncols, i + 1)

            # sc = ax.scatter(
            #     z[:, 0],
            #     z[:, 1],
            #     s=5,
            #     c=labels[label_name],
            #     cmap=CMAP[label_name],
            # )

            df = pd.DataFrame({"z0": z[:, 0], 
                    "z1": z[:, 1], 
                    "pos": labels[label_name] 
                    })
                    
            sc = sns.scatterplot(x="z0", y="z1", hue="pos", data=df, palette="rainbow")
            plt.title(label_name, fontsize=14)



    elif latent_dim == 3:
        fig = plt.figure(figsize=(10 * ncols, 8 * nrows))
        for i, label_name in enumerate(label_names):
            ax = fig.add_subplot(nrows, ncols, i + 1, projection="3d")
            sc = ax.scatter(
                z[:, 0],
                z[:, 1],
                z[:, 2],
                s=10,
                c=labels[label_name],
                cmap=CMAP[label_name],
            )
            ax.set_title(label_name, fontsize=30)
            fig.colorbar(sc, ax=ax)

    plt.tight_layout()
    plt.savefig(fname)
    plt.close()
