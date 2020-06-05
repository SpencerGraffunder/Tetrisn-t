import client.globals as g
import pygame

tile_colors = {0: (255, 255, 0),
               1: (255, 0, 0),
               2: (80, 240, 60),
               3: (0, 255, 255),
               4: (255, 0, 255),
               5: (0, 0, 0)}

# darken edges by (essentially put a black pixel with the corresponding opacity over top of)
EDGE_DARKEN_0 = 0.95
EDGE_DARKEN_1 = 0.85
EDGE_DARKEN_2 = 0.75

# [0][1][1][2][2][1][1][0]
# [1][-][-][-][-][-][-][1]
# [1][-][-][-][-][-][-][1]
# [2][-][-][-][-][-][-][2]
# [2][-][-][-][-][-][-][2]
# [1][-][-][-][-][-][-][1]
# [1][-][-][-][-][-][-][1]
# [0][1][1][2][2][1][1][0]

# brighten middle by (essentially put a white pixel with the corresponding opacity over top of)
MIDDLE_BRIGHTEN_0 = 0.40
MIDDLE_BRIGHTEN_1 = 0.25
MIDDLE_BRIGHTEN_2 = 0.10

# [-][-][-][-][-][-][-][-]
# [-][-][-][2][2][-][-][-]
# [-][-][2][1][1][2][-][-]
# [-][2][1][0][0][1][2][-]
# [-][2][1][0][0][1][2][-]
# [-][-][2][1][1][2][-][-]
# [-][-][-][2][2][-][-][-]
# [-][-][-][-][-][-][-][-]

def get_tile_surface(color):
    # do stuff
    pixels = pygame.Surface((8, 8))
    pixels.fill((color[0], color[1], color[2]))

    # darken corners
    for i in [0, 7]:  # For every corner pixel:
        for j in [0, 7]:
            pixels.set_at((i, j), (int(color[0] * (1 - EDGE_DARKEN_0)), int(color[1] * (1 - EDGE_DARKEN_0)), int(color[2] * (1 - EDGE_DARKEN_0))))

    # darken around corners on the edges
    for i in [1, 2, 5, 6]:
        for j in [0, 7]:
            pixels.set_at((i, j), (int(color[0] * (1 - EDGE_DARKEN_1)), int(color[1] * (1 - EDGE_DARKEN_1)), int(color[2] * (1 - EDGE_DARKEN_1))))
    for i in [0, 7]:
        for j in [1, 2, 5, 6]:
            pixels.set_at((i, j), (int(color[0] * (1 - EDGE_DARKEN_1)), int(color[1] * (1 - EDGE_DARKEN_1)), int(color[2] * (1 - EDGE_DARKEN_1))))

    # darken the middle of the edges
    for i in [3, 4]:
        for j in [0, 7]:
            pixels.set_at((i, j), (int(color[0] * (1 - EDGE_DARKEN_2)), int(color[1] * (1 - EDGE_DARKEN_2)), int(color[2] * (1 - EDGE_DARKEN_2))))
    for i in [0, 7]:
        for j in [3, 4]:
            pixels.set_at((i, j), (int(color[0] * (1 - EDGE_DARKEN_2)), int(color[1] * (1 - EDGE_DARKEN_2)), int(color[2] * (1 - EDGE_DARKEN_2))))

    # brighten the center 2x2
    for i in [3, 4]:
        for j in [3, 4]:
            pixels.set_at((i, j), (int(color[0] * (1 - MIDDLE_BRIGHTEN_0) + 255 * MIDDLE_BRIGHTEN_0), int(color[1] * (1 - MIDDLE_BRIGHTEN_0) + 255 * MIDDLE_BRIGHTEN_0), int(color[2] * (1 - MIDDLE_BRIGHTEN_0) + 255 * MIDDLE_BRIGHTEN_0)))

    # brighten around the center 2x2
    for i in [2, 5]:
        for j in [3, 4]:
            pixels.set_at((i, j), (int(color[0] * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1), int(color[1] * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1), int(color[2] * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1)))
    for i in [3, 4]:
        for j in [2, 5]:
            pixels.set_at((i, j), (int(color[0] * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1), int(color[1] * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1), int(color[2] * (1 - MIDDLE_BRIGHTEN_1) + 255 * MIDDLE_BRIGHTEN_1)))

    # brighten near the middle of the edge
    for i in [2, 5]:
        for j in [2, 5]:
            pixels.set_at((i, j), (int(color[0] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), int(color[1] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), int(color[2] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2)))
    for i in [1, 6]:
        for j in [3, 4]:
            pixels.set_at((i, j), (int(color[0] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), int(color[1] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), int(color[2] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2)))
    for i in [3, 4]:
        for j in [1, 6]:
            pixels.set_at((i, j), (int(color[0] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), int(color[1] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2), int(color[2] * (1 - MIDDLE_BRIGHTEN_2) + 255 * MIDDLE_BRIGHTEN_2)))

    return pixels


for tile_index in range(len(tile_colors.keys())):
    g.tile_surfaces[tile_index] = get_tile_surface(tile_colors[tile_index])
