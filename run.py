import numpy as np
from src.visualiziation import show_noise_map
from src.noise import generate_noise, generate_fractal_noise
from src.utils import generate_random_string, string_to_int_seed

width = 512
height = 512

seed = string_to_int_seed(generate_random_string)
noise = generate_noise(width=width, height=height, seed=seed)
frac_noise = generate_fractal_noise(width=width, height=height, scale=0.02, octaves=4, seed=seed)

# show_noise_map(noise)
show_noise_map(frac_noise)