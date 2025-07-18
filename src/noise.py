from noise import pnoise2
from queue import deque
import random

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