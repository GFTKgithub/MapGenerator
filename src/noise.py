from noise import pnoise2
from queue import deque
import random
import math


#~ Noise generation functions
def generate_noise(width, height, scale=0.1, offset_x=0, offset_y=0, seed=0) -> list[list[float]]:
    seed = seed % 256

    # Hashed offset based on seed
    new_offset_x = (seed * 37) % 1000 + offset_x
    new_offset_y = (seed * 73) % 1000 + offset_y

    return [[pnoise2((x + new_offset_x) * scale, (y + new_offset_y) * scale, base=seed)
            for x in range(width)] for y in range(height)]

def generate_fractal_noise(width, height, scale=0.1, offset_x=0, offset_y=0, octaves=1, persistence=0.5, lacunarity=2, seed=0) -> list[list[float]]:
    seed = seed % 256

    # Hashed offset based on seed
    new_offset_x = (seed * 37) % 1000 + offset_x
    new_offset_y = (seed * 73) % 1000 + offset_y
    
    return [[pnoise2((x + new_offset_x) * scale, (y + new_offset_y) * scale, base=seed, 
                     octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            for x in range(width)] for y in range(height)]

def fill_holes(grid, width, height) -> list[list[float]]:
    for y in range(height):
        for x in range(width):
            if grid[y][x] == -1:
                neighbors = []
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx = (x + dx) % width  # horizontal wrap
                    ny = y + dy
                    if 0 <= ny < height and grid[ny][nx] != -1:
                        neighbors.append(grid[ny][nx])
                if neighbors:
                    # Assign the most common neighbor plate
                    grid[y][x] = max(set(neighbors), key=neighbors.count)       
            
def generate_plates_weighted(width, height, plate_count, growth_probs, seed) -> list[list[float]]:
    if seed is not None:
        random.seed(seed)
    
    grid = [[-1 for _ in range(width)] for _ in range(height)]
    queues = []
    starts = []

    chosen = set()
    while len(chosen) < plate_count:
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        if (x, y) not in chosen:
            chosen.add((x, y))
            starts.append((x, y))

    for i, (x, y) in enumerate(starts):
        grid[y][x] = i
        q = deque()
        q.append((x, y))
        queues.append(q)

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    active = True
    while active:
        active = False
        for i, q in enumerate(queues):
            next_frontier = deque()
            while q:
                x, y = q.popleft()

                neighbors = directions[:]
                random.shuffle(neighbors)

                for dx, dy in neighbors:
                    nx = (x + dx) % width
                    ny = y + dy
                    if ny < 0 or ny >= height:
                        continue
                    if grid[ny][nx] == -1:
                        if random.random() < growth_probs[i]:
                            grid[ny][nx] = i
                            next_frontier.append((nx, ny))
            if next_frontier:
                active = True
                queues[i] = next_frontier
            else:
                queues[i] = deque()

    fill_holes(grid, width=width, height=height)
    return grid

#~ Blur functions

def convolve2d(image, kernel):
    h, w = len(image), len(image[0])
    kh, kw = len(kernel), len(kernel[0])
    ph, pw = kh // 2, kw // 2

    output = [[0.0 for _ in range(w)] for _ in range(h)]

    for i in range(h):
        for j in range(w):
            acc = 0.0
            for ki in range(kh):
                for kj in range(kw):
                    ii = i + ki - ph
                    jj = j + kj - pw
                    if 0 <= ii < h and 0 <= jj < w:
                        acc += image[ii][jj] * kernel[ki][kj]
            output[i][j] = acc
    return output

def box_blur(image, kernel_size):
    weight = 1.0 / (kernel_size * kernel_size)
    kernel = [[weight for _ in range(kernel_size)] for _ in range(kernel_size)]
    return convolve2d(image, kernel)

def gaussian_kernel(size, sigma):
    kernel = [[0.0 for _ in range(size)] for _ in range(size)]
    center = size // 2
    total = 0.0

    for i in range(size):
        for j in range(size):
            x, y = i - center, j - center
            val = math.exp(-(x*x + y*y) / (2 * sigma * sigma))
            kernel[i][j] = val
            total += val

    for i in range(size):
        for j in range(size):
            kernel[i][j] /= total

    return kernel

def gaussian_blur(image, size, sigma):
    kernel = gaussian_kernel(size, sigma)
    return convolve2d(image, kernel)