from dataclasses import dataclass
from pathlib import Path

import json
config_path = Path(__file__).parent.parent / 'config' / 'default.json'
with open(config_path, 'r') as f:
    default_config = json.load(f)

import numpy as np
import random

from .noise import *
from .utils import generate_random_string, string_to_int_seed


@dataclass
class TerrainConfig:
    width: int
    height: int
    plates_counts: list[int]
    plates_growth_probs_ranges: list[list[float]]
    oceanic_fraction: float
    seed: int = string_to_int_seed(generate_random_string())

default_terrain_config = TerrainConfig(
    width = default_config['width'],
    height = default_config['height'],
    plates_counts = default_config['terrain']['plates_counts'],
    plates_growth_probs_ranges = default_config['terrain']['plates_growth_probs_ranges'],
    oceanic_fraction = default_config['terrain']['oceanic_fraction'],
    seed = string_to_int_seed(generate_random_string())
) 

def unwrap_growth_probs(ranges: list[list[float]], count: int) -> list[float]:
    return [random.uniform(*ranges[i * len(ranges) // count]) for i in range(count)]

#* Terrain generation
def generate_terrain(config: TerrainConfig = default_terrain_config) -> list[list[float]]:
    width, height = config.width, config.height
    seed = config.seed
    total_plates_count = sum(config.plates_counts)
    random.seed(seed)  # ensure deterministic randomness

    terrain = generate_fractal_noise(width=width, height=height, scale=0.02, octaves=7, seed=seed)
    tectonic_mask = [[0 for y in range(height)] for x in range(width)] # initiate mask map

    growth_probs = unwrap_growth_probs(config.plates_growth_probs_ranges, total_plates_count)
    tectonic_base = generate_plates_weighted(width=width, height=height, plate_count=total_plates_count, growth_probs=growth_probs, seed=seed)
    
    tectonic_types = [1 if random.random() > config.oceanic_fraction else 0 for _ in range(total_plates_count)] 
    tectonic_densities = [
        random.uniform(0, 0.5) if tectonic_types[i] == 1 else random.uniform(0.5, 1) 
        for i in range(len(tectonic_types))
    ]

    for x in range(len(tectonic_base)):
        for y in range(len(tectonic_base[0])):
            tectonic_mask[x][y] = (1.0 - tectonic_densities[tectonic_base[x][y]]) * 2 - 1 # Fill the tectonic_mask based on `high density = low elevation`
                
                
    tectonic_mask = box_blur(tectonic_mask, 9)
    terrain = mask_and_normalize(terrain, tectonic_mask)

    terrain = np.array(terrain) * 0.25

    return terrain