import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def show_noise_map(noise: list[list[float]]):
    plt.imshow(noise, cmap='Greys')
    plt.title("Noise Map")
    plt.axis('off')
    plt.show()

def show_tectonic_map(map: list[list[float]]):
    # Convert input map to numpy array
    arr = np.array(map)
    unique_vals = np.unique(arr)
    n_colors = len(unique_vals)
    
    # Create a colormap with n_colors distinct colors
    colors = plt.cm.get_cmap('hsv', n_colors)
    cmap = ListedColormap(colors(np.arange(n_colors)))
    
    # Map each unique value in arr to an index 0..n_colors-1
    val_to_idx = {val: i for i, val in enumerate(unique_vals)}
    color_indices = np.vectorize(val_to_idx.get)(arr)

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.35)
    
    # Display the color indexed data
    image = ax.imshow(color_indices, cmap=cmap, interpolation='nearest', vmin=0, vmax=n_colors-1)
    plt.title("Tectonic Map")
    plt.axis('off')
    plt.show()