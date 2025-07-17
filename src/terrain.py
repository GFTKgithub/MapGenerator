from dataclasses import dataclass
from pathlib import Path

import json
config_path = Path(__file__).parent.parent / 'config' / 'default.json'
with open(config_path, 'r') as f:
    default_config = json.load(f)

import numpy as np
import random

from .noise import generate_fractal_noise, generate_plates_weighted
from .utils import generate_random_string, string_to_int_seed


@dataclass
class TerrainConfig:
    width: int
    height: int
    plates_counts: list[int]
    plates_growth_probs_ranges: list[list[float]]
    seed: int = string_to_int_seed(generate_random_string())

default_terrain_config = TerrainConfig(
    width = default_config['width'],
    height = default_config['height'],
    seed = string_to_int_seed(generate_random_string()),
    plates_counts = default_config['terrain']['plates_counts'],
    plates_growth_probs_ranges = default_config['terrain']['plates_growth_probs_ranges']
) 

def unwrap_growth_probs(ranges: list[list[float]], count: int) -> list[float]:
    return [random.uniform(*ranges[i * len(ranges) // count]) for i in range(count)]

#* Terrain generation
def generate_terrain(config: TerrainConfig = default_terrain_config) -> list[list[float]]:
    width, height = config.width, config.height
    seed = config.seed
    total_plates_count = sum(config.plates_counts)

    random.seed(seed)  # ensure reproducible growth_probs
    growth_probs = unwrap_growth_probs(config.plates_growth_probs_ranges, total_plates_count)

    terrain = generate_fractal_noise(width=width, height=height, scale=0.02, octaves=4, seed=seed)
    tectonic_plates = generate_plates_weighted(width=width, height=height, plate_count=total_plates_count, growth_probs=growth_probs, seed=seed)

    return tectonic_plates