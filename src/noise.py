from noise import pnoise2

def generate_noise(width, height, scale=0.1, offset_x=0, offset_y=0, seed=0):
    seed = seed % 256

    # Hashed offset based on seed
    new_offset_x = (seed * 37) % 1000 + offset_x
    new_offset_y = (seed * 73) % 1000 + offset_y

    return [[pnoise2((x + new_offset_x) * scale, (y + new_offset_y) * scale, base=seed)
            for x in range(width)] for y in range(height)]

def generate_fractal_noise(width, height, scale=0.1, offset_x=0, offset_y=0, octaves=1, persistence=0.5, lacunarity=2, seed=0):
    seed = seed % 256

    # Hashed offset based on seed
    new_offset_x = (seed * 37) % 1000 + offset_x
    new_offset_y = (seed * 73) % 1000 + offset_y
    
    return [[pnoise2((x + new_offset_x) * scale, (y + new_offset_y) * scale, base=seed, 
                     octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            for x in range(width)] for y in range(height)]