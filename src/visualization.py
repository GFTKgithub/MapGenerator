import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D projection
from typing import Optional

# Internal registry to store pending plots
_plot_registry = []

def show_noise_map(noise: list[list[float]]):
    _plot_registry.append(("2d", "Noise Map", lambda ax: _plot_noise_map(ax, noise)))

def show_tectonic_map(map: list[list[float]]):
    _plot_registry.append(("2d", "Tectonic Map", lambda ax: _plot_tectonic_map(ax, map)))

def show_heightmap_3d(heightmap: list[list[float]], z_range: Optional[tuple[float, float]] = None):
    _plot_registry.append(("3d", "Heightmap 3D", lambda ax: _plot_heightmap_3d(ax, heightmap, z_range)))

def _plot_noise_map(ax, noise):
    ax.imshow(noise, cmap='Greys')
    ax.set_title("Noise Map")
    ax.axis('off')

def _plot_tectonic_map(ax, map):
    arr = np.array(map)
    unique_vals = np.unique(arr)
    n_colors = len(unique_vals)
    cmap = ListedColormap(plt.cm.get_cmap('hsv', n_colors)(np.arange(n_colors)))
    val_to_idx = {val: i for i, val in enumerate(unique_vals)}
    color_indices = np.vectorize(val_to_idx.get)(arr)
    ax.imshow(color_indices, cmap=cmap, interpolation='nearest', vmin=0, vmax=n_colors - 1)
    ax.set_title("Tectonic Map")
    ax.axis('off')

def _plot_heightmap_3d(ax, heightmap, z_range):
    heightmap_np = np.array(heightmap)
    x = np.arange(heightmap_np.shape[1])
    y = np.arange(heightmap_np.shape[0])
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x, y, heightmap_np, cmap='terrain')
    if z_range:
        ax.set_zlim(*z_range)
    ax.set_title("Heightmap 3D")

def render_all():
    n = len(_plot_registry)
    if n == 0:
        return

    n_cols = 2
    n_rows = (n + 1) // n_cols
    fig = plt.figure(figsize=(6 * n_cols, 5 * n_rows))

    for i, (kind, title, plot_func) in enumerate(_plot_registry):
        if kind == "3d":
            ax = fig.add_subplot(n_rows, n_cols, i + 1, projection='3d')
        else:
            ax = fig.add_subplot(n_rows, n_cols, i + 1)
        plot_func(ax)

    plt.tight_layout()
    plt.show()
    _plot_registry.clear()  # clear after rendering