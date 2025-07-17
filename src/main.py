import numpy as np
# import biome 
from src.visualization import show_noise_map, show_tectonic_map
from src.terrain import generate_terrain, unwrap_growth_probs
from src.noise import generate_plates_weighted

terrain_map = generate_terrain()
# show_noise_map(terrain_map)
show_tectonic_map(terrain_map)