import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.widgets import Button
from noise import pnoise2


# Settings
width, height = 512, 512
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

# Biome colors (expanded)
biomeColors = {
    "Rock": (160, 160, 160),                               # Darker neutral gray
    "Highlands": (199, 196, 187),
    "Ice Sheet and Polar Desert": (225, 245, 255),         # Brighter ice blue
    "Tundra": (190, 215, 225),                             # Colder, slightly bluish-gray
    "Alpine Tundra": (180, 215, 225),                      # More cyan-tinted
    "Taiga": (120, 160, 120),                              # Cooler green
    "Temperate Broadleaf Forest": (75, 135, 60),           # Richer forest green
    "Temperate Steppe and Savanna": (200, 170, 90),        # Slightly warmer
    "Subtropical Evergreen Forest": (60, 120, 95),         # Deeper forest green
    "Mediterranean": (175, 155, 85),            # Warmer earth tone
    "Monsoon Forests and Mosaic": (50, 140, 80),           # More saturated green
    "Arid Desert": (245, 220, 160),                        # Brighter sand
    "Xeric Shrubland": (225, 195, 145),                    # Slightly redder than desert
    "Dry Steppe and Thorn Forest": (215, 185, 125),        # Balanced ochre
    "Semiarid Desert": (245, 230, 170),                    # Light yellow-beige
    "Grass Savanna": (165, 205, 100),                      # Slightly lime-toned
    "Tree Savanna": (110, 170, 80),                        # Deeper green than grass savanna
    "Dry Forest and Woodland Savanna": (90, 145, 65),      # Darker olive
    "Tropical Rainforest": (20, 110, 40),                  # Dark lush green
    "Montane Forests and Grasslands": (105, 125, 107),      # Cooler muted green
    "Deep Water": (0, 0, 70),                              # Dark navy
    "Shallow Water": (0, 115, 160),                        # Clearer cyan
    "Beach": (240, 220, 180)                               # Warmer sandy beige
}


def normalize(data):
    min_val, max_val = np.min(data), np.max(data)
    return (data - min_val) / (max_val - min_val)

def generate_noise_map(seed_offset=0, scale=100.0):
    return np.array([
        [pnoise2((x + seed_offset) / scale,
                 (y + seed_offset) / scale,
                 octaves=octaves,
                 persistence=persistence,
                 lacunarity=lacunarity,
                 repeatx=1024,
                 repeaty=1024,
                 base=seed)
         for x in range(width)]
        for y in range(height)
    ])

def tectonic_noise():
    base = generate_noise_map(scale=300.0)
    detail = generate_noise_map(scale=50.0)
    ridges = generate_noise_map(scale=20.0)
    tectonics = base * 0.6 + detail * 0.3 + np.abs(ridges) * 0.4
    return normalize(tectonics)

def generate_maps():
    global seed 

    global elevation
    global temperature
    global moisture


    seed = np.random.randint(0, 100)
    elevation = tectonic_noise()

    # Equatorial land bias
    equator_weight = np.cos(np.linspace(-np.pi / 2, np.pi / 2, height)) ** 2
    elevation = normalize(elevation * (1 + 0.4 * equator_weight[:, np.newaxis]))

    # Accurate cosine-based Earth-like temperature (no squish)
    latitudes = np.linspace(-np.pi / 2, np.pi / 2, height)
    temperature = np.cos(latitudes * 1.5)
    temperature = (temperature + 1) / 2
    temperature = np.tile(temperature, (width, 1)).T

    # Add slight noise for realism
    temp_noise = normalize(generate_noise_map(seed_offset=3000, scale=300.0))
    temperature = np.clip(temperature + (temp_noise - 0.5) * 0.4, 0, 1)

    moisture = normalize(generate_noise_map(seed_offset=2000, scale=150.0))
    moisture = np.clip(moisture + (temperature - 0.5) * 0.5, 0, 1)


def get_biome(e, m, t): 
    # Water and shoreline
    if e < 0.3:
        return biomeColors["Deep Water"]
    elif e < 0.4:
        return biomeColors["Shallow Water"]
    elif e < 0.45:
        return biomeColors["Beach"]

    # Super high elevation: rock
    if e > 0.85:
        return biomeColors["Rock"]

    # Montane belt
    elif e > 0.75:
        if t < 0.3:
            return biomeColors["Ice Sheet and Polar Desert"] 
        elif m < 0.5:
            return biomeColors["Highlands"]  # Assuming "Dry Highlands" fits here
        else:
            return biomeColors["Montane Forests and Grasslands"]

    # Rest: based on temperature and moisture
    if t < 0.2:
        return biomeColors["Ice Sheet and Polar Desert"]
    elif t < 0.3:
        return biomeColors["Tundra"]
    elif t < 0.4:
        return biomeColors["Taiga"]
    elif t < 0.5:
        return biomeColors["Temperate Broadleaf Forest"] if m > 0.5 else biomeColors["Temperate Steppe and Savanna"]
    elif t < 0.6:
        return biomeColors["Subtropical Evergreen Forest"] if m > 0.5 else biomeColors["Mediterranean"]
    elif t < 0.7:
        if m < 0.3:
            return biomeColors["Semiarid Desert"]
        elif m < 0.5:
            return biomeColors["Xeric Shrubland"]
        else:
            return biomeColors["Monsoon Forests and Mosaic"]
    else:
        if m < 0.2:
            return biomeColors["Arid Desert"]
        elif m < 0.4:
            return biomeColors["Dry Steppe and Thorn Forest"]
        elif m < 0.6:
            return biomeColors["Grass Savanna"]
        elif m < 0.725:
            return biomeColors["Tree Savanna"]
        elif m < 0.85:
            return biomeColors["Dry Forest and Woodland Savanna"]
        else:
            return biomeColors["Tropical Rainforest"]


def plot():
    color_to_biome = {tuple(v): k for k, v in biomeColors.items()}

    # Generate initial data
    generate_maps()

    # Create biome label map
    biome_labels = np.empty((height, width), dtype=object)
    biome_map = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            color = get_biome(elevation[y, x], moisture[y, x], temperature[y, x])
            biome_map[y, x] = color
            biome_labels[y, x] = color_to_biome[tuple(color)]

    # Create figure and axes once
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    ax_button = plt.axes([0.8, 0.01, 0.1, 0.075])
    button = Button(ax_button, 'Regenerate')

    # Initial plots
    elevation_im = axs[0, 0].imshow(elevation, cmap='terrain')
    axs[0, 0].set_title("Elevation")
    axs[0, 0].axis('off')

    temperature_im = axs[0, 1].imshow(temperature, cmap='coolwarm')
    axs[0, 1].set_title("Temperature")
    axs[0, 1].axis('off')

    moisture_im = axs[1, 0].imshow(moisture, cmap='Blues')
    axs[1, 0].set_title("Moisture")
    axs[1, 0].axis('off')

    biome_ax = axs[1, 1]
    biome_im = biome_ax.imshow(biome_map)
    biome_ax.set_title("Biome Map (Hover for Info)")
    biome_ax.axis('off')

    # Legend
    legend_elements = [Patch(facecolor=np.array(color) / 255.0, label=name) for name, color in biomeColors.items()]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize='small')

    def on_button_click(event):
        generate_maps()
        for y in range(height):
            for x in range(width):
                color = get_biome(elevation[y, x], moisture[y, x], temperature[y, x])
                biome_map[y, x] = color
                biome_labels[y, x] = color_to_biome[tuple(color)]

        elevation_im.set_data(elevation)
        temperature_im.set_data(temperature)
        moisture_im.set_data(moisture)
        biome_im.set_data(biome_map)
        fig.canvas.draw_idle()

    button.on_clicked(on_button_click)

    def on_move(event):
        if event.inaxes == biome_ax and event.xdata and event.ydata:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < width and 0 <= y < height:
                biome = biome_labels[y, x]
                biome_ax.set_title(f"Biome Map — ({x}, {y}): {biome}")
                fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_move)

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    fig.subplots_adjust(bottom=0.15, hspace=0.14)
    plt.get_current_fig_manager().window.state('zoomed')  # Optional depending on your environment
    plt.show()

generate_maps();
plot()