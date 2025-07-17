import numpy as np
from matplotlib.widgets import Button, Slider
import random
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

width = 512
height = 512
seed_count = 15 

start_x = random.randint(0, width-1)
start_y = random.randint(0, height-1)


import random
from collections import deque

def generate_plates_weighted(width, height, plate_count, growth_probs):
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

    return grid

def fill_holes(grid, width, height):
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

# ========== GUI setup ==========

width, height = 500, 300
plate_count = 15
major_count = 7
minor_count = plate_count - major_count

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)

colors = plt.cm.get_cmap('hsv', plate_count)
cmap = ListedColormap(colors(np.arange(plate_count)))

image = ax.imshow(np.zeros((height, width)), cmap=cmap, interpolation='nearest', vmin=0, vmax=plate_count-1)
ax.axis('off')

# Sliders

# Plate count sliders
ax_major_count = plt.axes([0.25, 0.3, 0.65, 0.03])
ax_minor_count = plt.axes([0.25, 0.275, 0.65, 0.03])

s_major_count = Slider(ax_major_count, 'Major Plates', 1, 30, valinit=major_count, valstep=1)
s_minor_count = Slider(ax_minor_count, 'Minor Plates', 1, 40, valinit=minor_count, valstep=1)

ax_major_min = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_major_max = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_minor_min = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_minor_max = plt.axes([0.25, 0.1, 0.65, 0.03])

s_major_min = Slider(ax_major_min, 'Major Min', 0.3, 1.0, valinit=0.95)
s_major_max = Slider(ax_major_max, 'Major Max', 0.3, 1.0, valinit=1.0)
s_minor_min = Slider(ax_minor_min, 'Minor Min', 0.3, 1.0, valinit=0.7)
s_minor_max = Slider(ax_minor_max, 'Minor Max', 0.3, 1.0, valinit=0.8)

# Button
ax_button = plt.axes([0.4, 0.025, 0.2, 0.05])
button = Button(ax_button, 'Regenerate')

# ========== Update function ==========

def regenerate(event=None):
    major_min = s_major_min.val
    major_max = s_major_max.val
    minor_min = s_minor_min.val
    minor_max = s_minor_max.val

    major_count = int(s_major_count.val)
    minor_count = int(s_minor_count.val)
    plate_count = major_count + minor_count

    growth_probs = (
        [random.uniform(major_min, major_max) for _ in range(major_count)] +
        [random.uniform(minor_min, minor_max) for _ in range(minor_count)]
    )
    random.shuffle(growth_probs)

    grid = generate_plates_weighted(width, height, plate_count, growth_probs)
    fill_holes(grid, width, height)

    arr = np.array(grid, dtype=int)
    image.set_data(arr)
    image.set_clim(0, plate_count - 1)  # update color range

# ========== Wire it up ==========

button.on_clicked(regenerate)
s_major_count.on_changed(lambda val: regenerate())
s_minor_count.on_changed(lambda val: regenerate())
s_major_min.on_changed(lambda val: regenerate())
s_major_max.on_changed(lambda val: regenerate())
s_minor_min.on_changed(lambda val: regenerate())
s_minor_max.on_changed(lambda val: regenerate())

regenerate()  # Initial draw
plt.show()