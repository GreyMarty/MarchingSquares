import numpy as np
import pygame as pg
from pygame.math import Vector2
from opensimplex.opensimplex import OpenSimplex
from random import random

from config import *


def lerp(a, b, k):
    return b * k + a * (k - 1)


def color_lerp(c1, c2, k):
    r = abs(min(int(lerp(c1[0], c2[0], k)), 255))
    g = abs(min(int(lerp(c1[1], c2[1], k)), 255))
    b = abs(min(int(lerp(c1[2], c2[2], k)), 255))
    return r, g, b


def random_func(x, y, z, noise_scales=[1]):
    values = []
    for i, scale in enumerate(noise_scales):
        values.append(noise.noise3d(x / 5 * scale, y / 5 * scale, z * (i + 1) / 10))
    
    val = sum(values) / len(values) + 0.5
    return min(val, 1) if val > 0 else 0


def apply_noise():
    global noise_z

    noise_z += 0.1
    for y in range(GRID_SIZE[1]):
        for x in range(GRID_SIZE[0]):
            grid[x, y] = random_func(x, y, noise_z, [1, 0.5])


def draw_lines(*points):
    for start, end in points:
        pg.draw.line(main_surface, WHITE, start * CELL_SIZE, end * CELL_SIZE, 2)


def draw_rects():
    for y in range(1, GRID_SIZE[1] - 1):
        for x in range(1, GRID_SIZE[0] - 1):
            color = color_lerp(BLACK, GREY, grid[x, y])
            rect = [
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            ]

            pg.draw.rect(main_surface, color, rect)


def process():
    for y in range(1, GRID_SIZE[1] - 1):
        for x in range(1, GRID_SIZE[0] - 1):
            p1, p2, p3, p4 = Vector2(x, y), Vector2(x + 1, y), Vector2(x + 1, y + 1),  Vector2(x, y + 1)
            c1 = (p1 + p4) / 2
            c2 = (p1 + p2) / 2
            c3 = (p2 + p3) / 2
            c4 = (p3 + p4) / 2
            corners = [round(grid[int(p.x), int(p.y)]) for p in (p1, p2, p3, p4)]

            if all(corners) or not any(corners):
                continue

            variants["".join(map(str, corners))](c1, c2, c3, c4)


noise = OpenSimplex(seed=int(random() * 1000))
noise_z = random()
grid = np.zeros(GRID_SIZE)
apply_noise()

pg.init()
pg.display.set_caption("Marching Squares")
main_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

variants = {
    "1000": lambda c1, c2, c3, c4: draw_lines((c1, c2)),
    "0111": lambda c1, c2, c3, c4: draw_lines((c1, c2)),
    "1100": lambda c1, c2, c3, c4: draw_lines((c1, c3)),
    "0011": lambda c1, c2, c3, c4: draw_lines((c1, c3)),
    "1110": lambda c1, c2, c3, c4: draw_lines((c1, c4)),
    "0001": lambda c1, c2, c3, c4: draw_lines((c1, c4)),
    "0100": lambda c1, c2, c3, c4: draw_lines((c2, c3)),
    "1011": lambda c1, c2, c3, c4: draw_lines((c2, c3)),
    "0110": lambda c1, c2, c3, c4: draw_lines((c2, c4)),
    "1001": lambda c1, c2, c3, c4: draw_lines((c2, c4)),
    "0010": lambda c1, c2, c3, c4: draw_lines((c3, c4)),
    "1101": lambda c1, c2, c3, c4: draw_lines((c3, c4)),
    "1010": lambda c1, c2, c3, c4: draw_lines((c1, c2), (c3, c4)),
    "0101": lambda c1, c2, c3, c4: draw_lines((c1, c4), (c2, c3)),
}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    main_surface.fill(BLACK)
    pg.draw.rect(main_surface, DARK_GREY, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 2 * CELL_SIZE)
    apply_noise()
    draw_rects()
    process()
    pg.display.update()
