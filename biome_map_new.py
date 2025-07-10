import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.widgets import Button
from noise import pnoise2

# Biome colors (expanded)
biomesColors = {
    # Cold & Polar
    "Ice Sheet and Polar Desert": (178, 178, 178),
    "Tundra": (140, 204, 189),
    "Alpine Tundra": (149, 174, 210),
    "Montane Forests and Grasslands": (41, 131, 132),

    # Boreal
    "Taiga": (0, 87, 78),

    # Temperate
    "Temperate Broadleaf Forest": (146, 216, 71),
    "Temperate Steppe and Savanna": (245, 231, 89),
    "Mediterranean": (124, 96, 134),

    # Subtropical
    "Subtropical Evergreen Forest": (6, 104, 6),
    "Monsoon Forests and Mosaic": (89, 129, 89),

    # Tropical
    "Dry Steppe and Thorn Forest": (136, 111, 51),
    "Xeric Shrubland": (170, 95, 61),
    "Arid Desert": (129, 66, 41),
    "Semiarid Desert": (214, 169, 114),
    "Grass Savanna": (193, 189, 62),
    "Tree Savanna": (155, 149, 14),
    "Dry Forest and Woodland Savanna": (96, 122, 34),
    "Tropical Rainforest": (0, 70, 0),

    # Non-vegetated & Water
    "Rock": (160, 160, 160),
    "Highlands": (199, 196, 187),
    "Beach": (240, 220, 180),
    "Shallow Water": (0, 115, 160),
    "Deep Water": (0, 0, 70)
}